"""Beschädigte Farbangaben dürfen keine Textbausteine überschreiben."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from app import module_archive as archive
from app import snippet_store as snippets


class SnippetColorValidationTests(unittest.TestCase):
    def test_unhashable_color_is_rejected_without_writing(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            snippets.put(root, {
                'workflow': 'Coding', 'category': 'Tests', 'title': 'Baustein',
                'content': 'Beispiel', 'color': 'Blau', 'size': 'Mittel',
            })
            target = archive.state_path(root, snippets.MODULE)
            before = target.read_bytes()
            for color in ([], {'rgb': '#244a73'}):
                with self.subTest(color=color):
                    damaged = deepcopy(snippets.load(root))
                    damaged['snippets'][0]['color'] = color
                    with self.assertRaisesRegex(ValueError, 'Workflow, Farbe oder Größe'):
                        snippets.save(root, damaged)
                    self.assertEqual(before, target.read_bytes())

    def test_valid_colors_remain_accepted(self):
        state = snippets.empty_state()
        state['snippets'].append({
            'id': 'valid', 'group': 'valid', 'version': 1,
            'title': 'Test', 'category': 'Tests', 'content': 'Text',
            'workflow': 'Coding', 'color': 'Blau', 'size': 'Mittel', 'monthly': {},
        })
        self.assertEqual('Blau', snippets.validate(state)['snippets'][0]['color'])


if __name__ == '__main__':
    unittest.main()
