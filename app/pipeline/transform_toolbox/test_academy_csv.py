import unittest
from pathlib import Path
import pandas as pd


class TestAcademyCSV(unittest.TestCase):
    def setUp(self) -> None:
        self.pickle_jar_path = Path(__file__).resolve().parent.parent / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / "academy_csv.pkl")
        self.filenames = pd.read_pickle(self.pickle_jar_path / "academy_csv_filenames.pkl")

    ##########################
    #   YOUR TESTS GO HERE   #
    ##########################

    def test_transform_academy_csv(self):
        ##############################
        #   DON'T DO ANYTHING HERE   #
        ##############################
        pass
