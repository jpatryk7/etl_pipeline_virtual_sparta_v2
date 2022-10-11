import unittest
from pathlib import Path
import pandas as pd
from .talent_txt import TalentTXT
from .date_format_test import date_format_test


class TestTalentTXT(unittest.TestCase):
    def setUp(self) -> None:
        self.TalentTXT = TalentTXT()
        self.pickle_jar_path = Path(__file__).resolve().parent.parent / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / "talent_txt.pkl")
        self.filenames = pd.read_pickle(self.pickle_jar_path / "talent_txt_filenames.pkl")

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


class TestTransformAcademyCSV(unittest.TestCase):
    def setUp(self) -> None:
        self.pickle_jar_path = Path(__file__).resolve().parent.parent / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / "talent_txt.pkl")
        self.talent_txt_transform = TalentTXT()
        self.test_score_df = self.talent_txt_transform.transform_talent_txt(self.raw_df)

    ############################
    #   TESTING COLUMN NAMES   #
    ############################

    def test_transform_talent_txt_test_score_df_col_names(self) -> None:
        expected = {"student_name", "date", "psychometrics", "presentations"}
        actual = set(self.test_score_df.columns.tolist())
        self.assertEqual(expected, actual)

    ################################
    #   TESTING COLUMN DATATYPES   #
    ################################

    def test_transform_talent_txt_test_score_df_datatype(self) -> None:
        expected = {str, list, str, str}
        actual = set(self.test_score_df.dtypes.tolist())
        self.assertEqual(expected, actual)

    ###############################
    #   CHECKING FOR DUPLICATES   #
    ###############################

    def test_transform_talent_txt_test_score_df_duplicates(self) -> None:
        actual = self.test_score_df.duplicated().tolist()
        self.assertTrue(all(actual))

    #########################################
    #   TESTING FORMATTING OF EACH COLUMN   #
    #########################################

    def test_transform_talent_txt_col_format_person_name(self) -> None:
        actual = self.test_score_df["student_name"].tolist()

        self.assertTrue(all([a.istitle() for a in actual if not pd.isnull(a)]))
        self.assertTrue(all([a.count('  ') == 0 for a in actual if not pd.isnull(a)]))

    def test_transform_talent_txt_col_format_date(self) -> None:
        actual = self.test_score_df["date"].tolist()
        date_format_test(actual)

    def test_transform_talent_txt_format_test_results(self) -> None:
        actual_list = [self.test_score_df[key] for key in ["psychometrics", "presentation"]]
        for actual in actual_list:
            self.assertTrue(all(['/' in a for a in actual if not pd.isnull(a)]))
            self.assertTrue(all([a.split('/')[0].isdigit() and a.split('/')[1].isdigit() for a in actual if not pd.isnull(a)]))
            self.assertTrue(all([' ' not in a for a in actual if not pd.isnull(a)]))
            self.assertTrue(all([int(a.split('/')[0]) < int(a.split('/')[1]) for a in actual if not pd.isnull(a)]))


if __name__ == "__main__":
    unittest.main()
