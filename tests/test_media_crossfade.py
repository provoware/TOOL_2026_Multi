import tempfile
from pathlib import Path
import unittest
from app import media_jobs as jobs

class CrossfadeTests(unittest.TestCase):
    def test_real_transition_command_and_guards(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            pictures=[root/"one.png", root/"two.jpg", root/"three.png"]
            for pic in pictures: pic.write_bytes(b"test")
            args,target,total=jobs.crossfade_command(
                root,[str(p) for p in pictures],str(root/"output.mp4"),
                seconds=4,transition="wipeleft",intensity=80)
            joined=" ".join(args)
            self.assertIn("xfade=transition=wipeleft",joined)
            self.assertEqual(joined.count("xfade=transition="),2)
            self.assertTrue(9 < total < 12)
            self.assertIn("-n",args)
            self.assertNotIn("-y",args)
            self.assertEqual(target.name,"output.mp4")
            with self.assertRaises(ValueError):
                jobs.crossfade_command(root,[str(p) for p in pictures],str(root/"bad.mp4"),
                                       transition="custom=evil")
            with self.assertRaises(ValueError):
                jobs.crossfade_command(root,[str(p) for p in pictures],str(root/"bad.mp4"),
                                       intensity=101)
