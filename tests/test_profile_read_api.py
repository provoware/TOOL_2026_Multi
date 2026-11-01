"""Gemeinsame Leser dürfen Profilgrenzen, Altbytes und Schreibschutz nicht verletzen."""
import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from app.profile_store import (
    CATEGORIES, DEFAULT_PROFILES, add_values, profile_names, read_profile,
    save_profiles, store_path,
)
from app.genre_random import generate, history_load
from app.genre_favorites import favorite_values


class ProfileReadApiTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path = save_profiles(self.root, {
            'Test': {'Genres': ['Düster', 'warm, dunkel', 'Dark Ambient'],
                     'Stimmungen': ['Düster', 'gelassen']},
            'Leer': {}, 'Anderes': {'Genres': ['Fremdwert']},
        })
        self.original = self.path.read_bytes()

    def test_defaults_and_names_do_not_create_a_store(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(profile_names(root), sorted(DEFAULT_PROFILES, key=str.casefold))
            self.assertEqual(read_profile(root, 'HardTechno'), DEFAULT_PROFILES['HardTechno'])
            self.assertFalse(store_path(root).exists())

    def test_profile_category_and_unicode_substring_boundaries(self):
        result = read_profile(self.root, 'Test', query=' DU\u0308ST ')
        self.assertEqual(result['Genres'], ['Düster'])
        self.assertEqual(result['Stimmungen'], ['Düster'])
        self.assertEqual(result['Stimme'], [])
        self.assertEqual(list(result), list(CATEGORIES))
        self.assertEqual(read_profile(self.root, 'Test', category='Genres', query=' DARK\tAMBI '),
                         {'Genres': ['Dark Ambient']})
        self.assertEqual(read_profile(self.root, 'Test', category='Genres', query='warm, dunkel'),
                         {'Genres': ['warm, dunkel']})
        self.assertEqual(read_profile(self.root, 'Test', category='Genres', query='Fremdwert'),
                         {'Genres': []})
        self.assertEqual(self.path.read_bytes(), self.original)

    def test_empty_profile_and_no_matches_have_complete_expected_shape(self):
        empty = {cat: [] for cat in CATEGORIES}
        self.assertEqual(read_profile(self.root, 'Leer'), empty)
        self.assertEqual(read_profile(self.root, 'Test', query='kein Treffer'), empty)
        self.assertEqual(read_profile(self.root, 'Test', category='Genres', query=' \t '),
                         {'Genres': ['Düster', 'warm, dunkel', 'Dark Ambient']})

    def test_unknown_names_and_invalid_filter_types_never_fall_back_or_write(self):
        for profile in ['Fehlt', 'test', ' Test ', '', None, True, [], {}]:
            with self.subTest(profile=profile), self.assertRaises(ValueError):
                read_profile(self.root, profile)
        for category in ['Fehlt', '', False, [], {}]:
            with self.subTest(category=category), self.assertRaises(ValueError):
                read_profile(self.root, 'Test', category=category)
        for query in [None, 42, [], {}, 'neu\n', '\r', '\0', '\x7f']:
            with self.subTest(query=query), self.assertRaises(ValueError):
                read_profile(self.root, 'Test', query=query)
        self.assertEqual(self.path.read_bytes(), self.original)

    def test_returned_containers_and_later_writes_are_isolated(self):
        result = read_profile(self.root, 'Test')
        result['Genres'].clear()
        result['Stimmungen'].append('Nur im Aufrufer')
        result.clear()
        names = profile_names(self.root)
        names.clear()
        self.assertEqual(self.path.read_bytes(), self.original)
        self.assertEqual(read_profile(self.root, 'Test', category='Genres')['Genres'],
                         ['Düster', 'warm, dunkel', 'Dark Ambient'])
        add_values(self.root, 'Test', 'Genres', 'Neu')
        self.assertEqual(read_profile(self.root, 'Test', query='neu')['Genres'], ['Neu'])

    def test_legacy_unicode_spelling_duplicates_and_order_survive_queries(self):
        raw = {'Test': {'Genres': ['du\u0308ster', 'Düster', 'später']}}
        self.path.write_text(json.dumps(raw, ensure_ascii=False), encoding='utf-8')
        before = self.path.read_bytes()
        self.assertEqual(read_profile(self.root, 'Test', category='Genres', query='DÜSTER'),
                         {'Genres': ['du\u0308ster', 'Düster']})
        self.assertEqual(self.path.read_bytes(), before)

    def test_damaged_store_is_not_hidden_by_defaults_or_empty_search(self):
        for damaged in [b'{kaputt', b'\xff', b'{"Test": {"Genres": [42]}}']:
            self.path.write_bytes(damaged)
            for reader in [lambda: profile_names(self.root),
                           lambda: read_profile(self.root, 'Test', query='kein Treffer')]:
                with self.assertRaises((ValueError, UnicodeError)):
                    reader()
                self.assertEqual(self.path.read_bytes(), damaged)

    def test_generator_and_favorites_keep_profile_scope_and_empty_category_errors(self):
        amounts = {cat: 0 for cat in CATEGORIES}
        amounts['Genres'] = 1
        entry = generate(self.root, 'Test', amounts, rng=random.Random(3))
        self.assertIn(entry['categories']['Genres'][0], read_profile(self.root, 'Test')['Genres'])
        self.assertNotIn('Fremdwert', entry['output'])
        before_history = history_load(self.root)
        with self.assertRaises(ValueError):
            generate(self.root, 'Fehlt', amounts)
        self.assertEqual(history_load(self.root), before_history)
        with self.assertRaises(ValueError):
            favorite_values(self.root, 'Test', None)
        self.assertEqual(self.path.read_bytes(), self.original)

    def test_read_api_runs_without_loading_qt(self):
        code = '''import sys, tempfile
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from app.profile_store import profile_names, read_profile
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    assert profile_names(root)
    assert read_profile(root, 'HardTechno', category='Genres', query='techno')
assert not any(n.startswith(('PySide6', 'PyQt', 'shiboken')) for n in sys.modules)
'''
        completed = subprocess.run([sys.executable, '-I', '-c', code,
                                    str(Path(__file__).resolve().parents[1])],
                                   capture_output=True, text=True, timeout=15)
        self.assertEqual(completed.returncode, 0, completed.stderr)
