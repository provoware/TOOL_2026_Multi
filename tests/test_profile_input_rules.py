"""Neue Profileingaben sicher normalisieren, ohne Altbestände zu migrieren."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.profile_store import (
    CATEGORIES, add_profile, add_value, add_values, load_profiles,
    save_profiles, split_input_values, store_path,
)
from app.genre_random import archive_export, archive_import, rename_value


class ProfileInputRulesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.target = save_profiles(self.root, {'Test': {'Genres': ['düster']}})
        self.original = self.target.read_bytes()

    def import_data(self, data):
        file = self.root / 'import.json'
        file.write_text(json.dumps({'schema': 1, 'profiles': data}), encoding='utf-8')
        return archive_import(self.root, file)

    def test_quoted_commas_escaped_quotes_empty_fields_and_order(self):
        values = split_input_values(' "warm, dunkel", ruhig, "Stimme ""nah"", weich",, RUHIG')
        self.assertEqual(values, ['warm, dunkel', 'ruhig', 'Stimme "nah", weich'])
        self.assertEqual(split_input_values('Stimme "nah", weich'), ['Stimme "nah"', 'weich'])
        self.assertEqual(split_input_values('ruhig,\t"warm, dunkel"'), ['ruhig', 'warm, dunkel'])
        self.assertEqual(split_input_values('"warm, dunkel" \t, ruhig'), ['warm, dunkel', 'ruhig'])
        self.assertEqual(split_input_values('"Stimme ""nah"" , weich" , ruhig'),
                         ['Stimme "nah" , weich', 'ruhig'])

    def test_unicode_casefold_and_whitespace_are_deduplicated(self):
        self.assertEqual(split_input_values(' du\u0308ster, DÜSTER,  sehr\t  ruhig, SEHR RUHIG'),
                         ['düster', 'sehr ruhig'])
        self.assertEqual(split_input_values('schön, schon'), ['schön', 'schon'])

    def test_bad_input_never_writes_or_partially_saves(self):
        for text in ['neu, "offen', 'neu, "fertig"x', 'neu\nzweite Zeile',
                     'neu\r', 'neu\0', 'neu\x7f', '', ', ,', '""', None, 123,
                     '"warm" "dunkel", ruhig', 'neu, "warm" \t"dunkel"']:
            with self.subTest(text=text), patch('app.profile_store.save_profiles') as save:
                with self.assertRaises(ValueError):
                    add_values(self.root, 'Test', 'Genres', text)
                save.assert_not_called()
                self.assertEqual(self.target.read_bytes(), self.original)

    def test_batch_is_atomic_and_scoped_to_profile_and_category(self):
        add_profile(self.root, 'Zweites')
        with patch('app.profile_store.save_profiles', wraps=save_profiles) as save:
            self.assertEqual(add_values(self.root, 'Test', 'Genres',
                                       'DU\u0308STER, "warm, dunkel", ruhig'),
                             ['warm, dunkel', 'ruhig'])
            self.assertEqual(save.call_count, 1)
        add_value(self.root, 'Zweites', 'Genres', 'düster')
        add_value(self.root, 'Test', 'Stil', 'düster')
        self.assertEqual(load_profiles(self.root)['Zweites']['Genres'], ['düster'])
        self.assertEqual(load_profiles(self.root)['Test']['Stil'], ['düster'])

    def test_single_value_rejects_canonical_duplicate(self):
        with self.assertRaises(ValueError):
            add_value(self.root, 'Test', 'Genres', 'DU\u0308STER')
        self.assertEqual(self.target.read_bytes(), self.original)

    def test_new_profile_name_matches_legacy_unicode_without_renaming_it(self):
        self.target = save_profiles(self.root, {'Du\u0308ster': {'Genres': ['Alt']}})
        before = self.target.read_bytes()
        with self.assertRaises(ValueError):
            add_profile(self.root, 'DÜSTER')
        self.assertEqual(self.target.read_bytes(), before)
        self.assertIn('Du\u0308ster', load_profiles(self.root))

    def test_legacy_canonical_duplicates_stay_readable_and_byte_identical(self):
        old = {'Test': {'Genres': ['düster', 'du\u0308ster']}}
        self.target.write_text(json.dumps(old, ensure_ascii=False), encoding='utf-8')
        before = self.target.read_bytes()
        self.assertEqual(load_profiles(self.root)['Test']['Genres'], old['Test']['Genres'])
        with patch('app.profile_store.save_profiles') as save:
            self.assertEqual(add_values(self.root, 'Test', 'Genres', 'DÜSTER'), [])
            save.assert_not_called()
        self.assertEqual(self.target.read_bytes(), before)
        add_values(self.root, 'Test', 'Genres', 'neu')
        self.assertEqual(load_profiles(self.root)['Test']['Genres'], old['Test']['Genres'] + ['neu'])

    def test_failed_write_preserves_original(self):
        with patch('app.atomic_io.os.replace', side_effect=OSError('Schreibprobe')):
            with self.assertRaises(OSError):
                add_values(self.root, 'Test', 'Genres', '"warm, dunkel", ruhig')
        self.assertEqual(self.target.read_bytes(), self.original)

    def test_import_skips_unicode_duplicates_and_roundtrips_literal_comma(self):
        self.assertEqual(self.import_data({'Test': {'Genres': ['du\u0308ster']}}),
                         {'profiles': 0, 'values': 0})
        self.assertEqual(self.target.read_bytes(), self.original)
        add_values(self.root, 'Test', 'Genres', '"warm, dunkel"')
        file = archive_export(self.root, self.root / 'export.json')
        before = self.target.read_bytes()
        self.assertEqual(archive_import(self.root, file), {'profiles': 0, 'values': 0})
        self.assertEqual(self.target.read_bytes(), before)
        self.assertIn('warm, dunkel', load_profiles(self.root)['Test']['Genres'])

    def test_ambiguous_import_rejects_everything_before_write(self):
        for incoming in [
            {'Neu': {'Genres': ['neu']}, 'Test': {'Genres': ['düster', 'du\u0308ster']}},
            {'Du\u0308ster': {}, 'Düster': {}},
            {'Neu': {'Genres': ['gültig', 'ungültig\n']}},
        ]:
            with self.subTest(incoming=incoming):
                with self.assertRaises(ValueError):
                    self.import_data(incoming)
                self.assertEqual(self.target.read_bytes(), self.original)

    def test_import_matches_legacy_profile_and_preserves_existing_spelling(self):
        self.target = save_profiles(self.root, {'Du\u0308ster': {'Genres': ['Altwärt']}})
        self.assertEqual(self.import_data({'DÜSTER': {'Genres': ['Neu']}}),
                         {'profiles': 0, 'values': 1})
        data = load_profiles(self.root)
        self.assertEqual(list(data), ['Du\u0308ster'])
        self.assertEqual(data['Du\u0308ster']['Genres'], ['Altwärt', 'Neu'])

    def test_rename_obeys_same_duplicate_and_quoting_rules(self):
        add_values(self.root, 'Test', 'Genres', 'anderer')
        before = self.target.read_bytes()
        with self.assertRaises(ValueError):
            rename_value(self.root, 'Test', 'Genres', 'anderer', 'DU\u0308STER')
        self.assertEqual(self.target.read_bytes(), before)
        rename_value(self.root, 'Test', 'Genres', 'anderer', '"warm, dunkel"')
        self.assertEqual(load_profiles(self.root)['Test']['Genres'], ['düster', 'warm, dunkel'])

    def test_ambiguous_legacy_target_profiles_are_not_chosen_arbitrarily(self):
        self.target = save_profiles(self.root, {'Düster': {}, 'Du\u0308ster': {}})
        before = self.target.read_bytes()
        with self.assertRaises(ValueError):
            self.import_data({'DÜSTER': {'Genres': ['Neu']}})
        self.assertEqual(self.target.read_bytes(), before)

    def test_new_profile_and_single_value_are_saved_as_nfc(self):
        name = add_profile(self.root, 'Wa\u0308rme')
        self.assertEqual(name, 'Wärme')
        self.assertEqual(add_value(self.root, name, 'Genres', 'gru\u0308n'), 'grün')
        self.assertEqual(load_profiles(self.root)[name]['Genres'], ['grün'])

    def test_new_unicode_import_can_be_repeated_without_changes(self):
        incoming = {'Wa\u0308rme': {'Genres': ['gru\u0308n', 'warm, weich']}}
        self.assertEqual(self.import_data(incoming), {'profiles': 1, 'values': 2})
        before = self.target.read_bytes()
        self.assertEqual(self.import_data(incoming), {'profiles': 0, 'values': 0})
        self.assertEqual(self.target.read_bytes(), before)
        self.assertEqual(load_profiles(self.root)['Wärme']['Genres'], ['grün', 'warm, weich'])
