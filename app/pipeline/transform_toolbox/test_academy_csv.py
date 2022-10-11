import unittest
from pathlib import Path
import pandas as pd
from .academy_csv import AcademyCSV
from .date_format_test import date_format_test


class TestAcademyCSV(unittest.TestCase):
    def setUp(self) -> None:
        self.pickle_jar_path = Path(__file__).resolve().parent.parent / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / "academy_csv.pkl")
        self.filenames = pd.read_pickle(self.pickle_jar_path / "academy_csv_filenames.pkl")

    ##########################
    #   YOUR TESTS GO HERE   #
    ##########################


class TestTransformAcademyCSV(unittest.TestCase):
    def setUp(self) -> None:
        self.pickle_jar_path = Path(__file__).resolve().parent.parent / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / "academy_csv.pkl")
        self.academy_csv_transform = AcademyCSV()
        self.trainer_df, self.course_df, self.academy_performance_df = self.academy_csv_transform.transform_academy_csv(self.raw_df)

    ############################
    #   TESTING COLUMN NAMES   #
    ############################

    def test_transform_academy_csv_trainer_df_col_names(self) -> None:
        expected = {"trainer_name"}
        actual = set(self.trainer_df.columns.tolist())
        self.assertEqual(expected, actual)

    def test_transform_academy_csv_course_df_col_names(self) -> None:
        expected = {"course_name", "trainer_name", "date"}
        actual = set(self.course_df.columns.tolist())
        self.assertEqual(expected, actual)

    def test_transform_academy_csv_academy_performance_df_col_names(self) -> None:
        expected = {"student_name", "date", "course_name", "analytic", "independent", "determined", "professional",
                    "studious", "imaginative"}
        actual = set(self.academy_performance_df.columns.tolist())
        self.assertEqual(expected, actual)

    ################################
    #   TESTING COLUMN DATATYPES   #
    ################################

    def test_transform_academy_csv_trainer_df_datatype(self) -> None:
        expected = {str}
        actual = set(self.trainer_df.dtypes.tolist())
        self.assertEqual(expected, actual)

    def test_transform_academy_csv_course_df_datatype(self) -> None:
        expected = {str, str, list[int]}
        actual = set(self.course_df.dtypes.tolist())
        self.assertEqual(expected, actual)

    def test_transform_academy_csv_academy_performance_df_datatype(self) -> None:
        expected = {str, list, str, int, int, int, int, int, int}
        actual = set(self.academy_performance_df.dtypes.tolist())
        self.assertEqual(expected, actual)

    ###############################
    #   CHECKING FOR DUPLICATES   #
    ###############################

    def test_transform_academy_csv_trainer_df_duplicates(self) -> None:
        actual = self.trainer_df.duplicated().tolist()
        self.assertTrue(all(actual))

    def test_transform_academy_csv_course_df_duplicates(self) -> None:
        actual = self.course_df.duplicated().tolist()
        self.assertTrue(all(actual))

    def test_transform_academy_csv_academy_performance_df_duplicates(self) -> None:
        actual = self.academy_performance_df.duplicated().tolist()
        self.assertTrue(all(actual))

    #########################################
    #   TESTING FORMATTING OF EACH COLUMN   #
    #########################################

    def test_transform_academy_csv_col_format_person_name(self) -> None:
        list_actual = [
            self.trainer_df["trainer_name"].tolist(),
            self.course_df["trainer_name"].tolist(),
            self.academy_performance_df["student_name"].tolist()
        ]
        for actual in list_actual:
            self.assertTrue(all([a.istitle() for a in actual if not pd.isnull(a)]))
            self.assertTrue(all([a.count('  ') == 0 for a in actual if not pd.isnull(a)]))

    def test_transform_academy_csv_col_format_course_name(self) -> None:
        list_actual = [
            self.course_df["course_name"].tolist(),
            self.academy_performance_df["course_name"].tolist()
        ]
        for actual in list_actual:
            self.assertTrue(all([a.count('  ') == 0 for a in actual if not pd.isnull(a)]))
            self.assertTrue(all([a.split(' ')[0].istitle() for a in actual if not pd.isnull(a)]))
            self.assertTrue(all([a.split(' ')[1].isdigit() for a in actual if not pd.isnull(a)]))

    def test_transform_academy_csv_col_format_date(self) -> None:
        actual_list = [self.course_df["date"].tolist(), self.academy_performance_df["date"].tolist()]
        for actual in actual_list:
            date_format_test(actual)

    def test_transform_academy_csv_academy_performance_df_scores_cols_format(self) -> None:
        actual_list = [self.academy_performance_df[key] for key in ["course_name", "analytic", "independent", "determined", "professional", "studious", "imaginative"]]
        for actual in actual_list:
            self.assertTrue(all([0 <= a <= 10 for a in actual if not pd.isnull(a)]))


if __name__ == '__main__':
    unittest.main()
