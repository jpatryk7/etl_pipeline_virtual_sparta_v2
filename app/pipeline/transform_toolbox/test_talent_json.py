import unittest
from pathlib import Path
import pandas as pd
from .talent_json import TalentJSON
from .date_format_test import date_format_test


class TestTalentJSON(unittest.TestCase):
    def setUp(self) -> None:
        self.pickle_jar_path = Path(__file__).resolve().parent.parent / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / "talent_json.pkl")
        self.filenames = pd.read_pickle(self.pickle_jar_path / "talent_json_filenames.pkl")

    ##########################
    #   YOUR TESTS GO HERE   #
    #########################


class TestTransformTalentJSON(unittest.TestCase):
    def setUp(self) -> None:
        self.pickle_jar_path = Path(__file__).resolve().parent.parent / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / "talent_json.pkl")
        self.talent_json_transform = TalentJSON()
        (
            self.trainee_performance_df,
            self.weakness_junction_df,
            self.strength_junction_df,
            self.tech_self_score_junction_df
        ) = self.talent_json_transform.transform_talent_json(self.raw_df)

    ############################
    #   TESTING COLUMN NAMES   #
    ############################

    def test_transform_talent_json_trainee_performance_df_col_names(self) -> None:
        expected = {"student_name", "date", "self_development", "geo_flex", "financial_support", "result", "course_interest"}
        actual = set(self.trainee_performance_df.columns.tolist())
        self.assertEqual(expected, actual)

    def test_transform_talent_json_weakness_junction_df_col_names(self) -> None:
        expected = {"student_name", "date", "weakness"}
        actual = set(self.weakness_junction_df.columns.tolist())
        self.assertEqual(expected, actual)

    def test_transform_talent_json_strength_junction_df_col_names(self) -> None:
        expected = {"student_name", "date", "strength"}
        actual = set(self.strength_junction_df.columns.tolist())
        self.assertEqual(expected, actual)

    def test_transform_talent_json_tech_self_score_junction_df_col_names(self) -> None:
        expected = {"student_name", "date", "tech_self_score", "value"}
        actual = set(self.tech_self_score_junction_df.columns.tolist())
        self.assertEqual(expected, actual)

    ################################
    #   TESTING COLUMN DATATYPES   #
    ################################

    def test_transform_talent_json_trainee_performance_df_datatypes(self) -> None:
        expected = {str, list, bool, bool, bool, str, str}
        actual = set(self.trainee_performance_df.dtypes.tolist())
        self.assertEqual(expected, actual)

    def test_transform_talent_json_weakness_junction_df_datatypes(self) -> None:
        expected = {str, list, str}
        actual = set(self.weakness_junction_df.dtypes.tolist())
        self.assertEqual(expected, actual)

    def test_transform_talent_json_strength_junction_df_datatypes(self) -> None:
        expected = {str, list, str}
        actual = set(self.strength_junction_df.dtypes.tolist())
        self.assertEqual(expected, actual)

    def test_transform_talent_json_tech_self_score_junction_df_datatypes(self) -> None:
        expected = {str, list, str, int}
        actual = set(self.tech_self_score_junction_df.dtypes.tolist())
        self.assertEqual(expected, actual)

    ###############################
    #   CHECKING FOR DUPLICATES   #
    ###############################

    def test_transform_talent_json_trainee_performance_df_duplicates(self) -> None:
        actual = self.trainee_performance_df.duplicated().tolist()
        self.assertTrue(all(actual))

    def test_transform_talent_json_weakness_junction_df_duplicates(self) -> None:
        actual = self.weakness_junction_df.duplicated().tolist()
        self.assertTrue(all(actual))

    def test_transform_talent_json_strength_junction_df_duplicates(self) -> None:
        actual = self.strength_junction_df.duplicated().tolist()
        self.assertTrue(all(actual))

    def test_transform_talent_json_tech_self_score_junction_df_duplicates(self) -> None:
        actual = self.tech_self_score_junction_df.duplicated().tolist()
        self.assertTrue(all(actual))

    #########################################
    #   TESTING FORMATTING OF EACH COLUMN   #
    #########################################

    def test_transform_talent_json_col_format_person_name(self) -> None:
        list_actual = [
            self.trainee_performance_df["student_name"].tolist(),
            self.trainee_performance_df["course_interest"].tolist(),
            self.weakness_junction_df["student_name"].tolist(),
            self.weakness_junction_df["weakness"].tolist(),
            self.strength_junction_df["student_name"].tolist(),
            self.strength_junction_df["strength"].tolist(),
            self.tech_self_score_junction_df["student_name"].tolist(),
            self.tech_self_score_junction_df["tech_self_score"].tolist()
        ]
        for actual in list_actual:
            self.assertTrue(all([a.istitle() for a in actual if not pd.isnull(a)]))
            self.assertTrue(all([a.count('  ') == 0 for a in actual if not pd.isnull(a)]))

    def test_transform_talent_json_col_format_date(self) -> None:
        actual_list = [
            self.trainee_performance_df["date"].tolist(),
            self.weakness_junction_df["date"].tolist(),
            self.strength_junction_df["date"].tolist(),
            self.tech_self_score_junction_df["date"].tolist()
        ]
        for actual in actual_list:
            date_format_test(actual)

    def test_transform_talent_json_col_format_result(self) -> None:
        actual = self.trainee_performance_df["result"].tolist()
        self.assertTrue(all([a == "Pass" or "Fail" for a in actual if not pd.isnull(a)]))

    def test_transform_talent_json_col_format_tech_self_score_value(self) -> None:
        actual = self.trainee_performance_df["value"].tolist()
        self.assertTrue(all([0 <= a for a in actual]))


if __name__ == '__main__':
    unittest.main()
