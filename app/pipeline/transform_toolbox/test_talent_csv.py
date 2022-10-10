import unittest
from pathlib import Path
import pandas as pd
from .talent_csv import TalentCSV


class TestAcademyCSV(unittest.TestCase):
    def setUp(self) -> None:
        self.pickle_jar_path = Path(__file__).resolve().parent.parent / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / "talent_csv.pkl")
        self.filenames = pd.read_pickle(self.pickle_jar_path / "talent_csv_filenames.pkl")

    ##########################
    #   YOUR TESTS GO HERE   #
    ##########################

    def test_transform_talent_csv(self):
        ##############################
        #   DON'T DO ANYTHING HERE   #
        ##############################
        pass
