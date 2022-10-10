import unittest
from pathlib import Path
import pandas as pd
from .talent_txt import TalentTXT


class TestTalentTXT(unittest.TestCase):
    def setUp(self) -> None:
        self.pickle_jar_path = Path(__file__).resolve().parent.parent / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / "talent_txt.pkl")
        self.filenames = pd.read_pickle(self.pickle_jar_path / "talent_txt_filenames.pkl")

    ##########################
    #   YOUR TESTS GO HERE   #
    ##########################

    def test_transform_talent_txt(self):
        ##############################
        #   DON'T DO ANYTHING HERE   #
        ##############################
        pass
