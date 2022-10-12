import unittest
from pathlib import Path
import pandas as pd
import datetime
from date_format_test import date_format_test
from talent_txt import TalentTXT


class TestTalentTXT(unittest.TestCase):
    def setUp(self) -> None:
        self.TalentTXT = TalentTXT()
        self.pickle_jar_path = Path(__file__).resolve().parent.parent / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / "talent_txt_v2.pkl")
        self.filenames = pd.read_pickle(self.pickle_jar_path / "talent_txt_filenames.pkl")


    def test_remove_word_column(self):
        df = pd.DataFrame({'words': ['Sparta Day Hi', 'Sparta Day Hello']})
        expected = pd.DataFrame({'words': [' Hi', ' Hello']})
        actual = self.TalentTXT.remove_word(df, 'words','Sparta Day')
        self.assertEqual(expected['words'][1],actual['words'][1])

    def test_transform_date(self):
        df = pd.DataFrame({'date': ['3 May 2015','2 March 2016']})
        expected_df = pd.DataFrame({'date': [[3,5,2015], [2,3,2016]]})
        actual = self.TalentTXT.transform_date(df, 'date')
        self.assertEqual(expected_df['date'][0], actual['date'][0])

    def test_rename_column(self):
        df = pd.DataFrame({'words': ['Sparta Day Hi', 'Sparta Day Hello'], 'year' : [2015,2016]})
        expected = pd.DataFrame({'stuff': ['Sparta Day Hi', 'Sparta Day Hello'], 'year' : [2015,2016]})
        actual = self.TalentTXT.rename_column(df, 'words', 'stuff')
        self.assertEqual(expected.columns[0],actual.columns[0])

    def test_reorder_column(self):
        df = pd.DataFrame({'words': ['Sparta Day Hi', 'Sparta Day Hello'], 'year' : [2015,2016]})
        expected = pd.DataFrame({'year':[2015,2016], 'words':['Sparta Day Hi', 'Sparta Day Hello']})
        actual = self.TalentTXT.reorder_columns(df, ['year','words'])
        self.assertEqual(expected.columns[0],actual.columns[0])

    def test_lower_case(self):
        df = pd.DataFrame({'words': ['SPARTA Day Hi', 'Sparta Day Hello'], 'year': [2015, 2016]})
        expected = pd.DataFrame({'words': ['Sparta Day Hi', 'Sparta Day Hello'], 'year': [2015, 2016]})
        actual = self.TalentTXT.lower_case(df, 'words')
        self.assertEqual(expected['words'][0],actual['words'][0])

    def test_del_duplicates(self):
        df = pd.DataFrame({'words': ['Sparta Day Hi','Sparta Day Hi', 'Sparta Day Hello'], 'year': [2015,2015, 2016]})
        expected = pd.DataFrame({'words': ['Sparta Day Hi', 'Sparta Day Hello'], 'year': [2015, 2016]})
        actual = self.TalentTXT.del_duplicates(df)
        self.assertEqual(len(expected.columns),len(actual.columns))


class TestTransformAcademyCSV(unittest.TestCase):
    def setUp(self) -> None:
        self.pickle_jar_path = Path(__file__).resolve().parent.parent / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / "talent_txt_v2.pkl")
        self.talent_txt_transform = TalentTXT()
        self.test_score_df = self.talent_txt_transform.transform_talent_txt(self.raw_df)

    ############################
    #   TESTING COLUMN NAMES   #
    ############################

    def test_transform_talent_txt_test_score_df_col_names(self) -> None:
        expected = {"student_name", "date", "psychometrics", "presentation"}
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
