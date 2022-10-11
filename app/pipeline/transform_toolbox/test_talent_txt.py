import unittest
from pathlib import Path
import pandas as pd
from .talent_txt import TalentTXT


class TestTalentTXT(unittest.TestCase):
    def setUp(self) -> None:
        self.TalentTXT = TalentTXT()
        self.pickle_jar_path = Path(__file__).resolve().parent.parent / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / "talent_txt.pkl")
        self.filenames = pd.read_pickle(self.pickle_jar_path / "talent_txt_filenames.pkl")

    ##########################
    #   YOUR TESTS GO HERE   #
    ##########################

    def test_replace_hyphens(self):
        expected = "DUN PEACHMENT ,  Psychometrics: 45/100, Presentation: 19/32"
        actual = self.TalentTXT.replace_hyphens("DUN PEACHMENT -  Psychometrics: 45/100, Presentation: 19/32")
        self.assertEqual(actual,expected)

    def test_replace_colon(self):
        expected = "DUN PEACHMENT -  Psychometrics, 45/100, Presentation, 19/32"
        actual = self.TalentTXT.replace_colon("DUN PEACHMENT -  Psychometrics: 45/100, Presentation: 19/32")
        self.assertEqual(actual,expected)

    def test_delete_spaces(self):
        expected = ""
    def test_transform_talent_txt(self):
        ##############################
        #   DON'T DO ANYTHING HERE   #
        ##############################
        pass

if __name__ == "__main__":
    unittest.main()