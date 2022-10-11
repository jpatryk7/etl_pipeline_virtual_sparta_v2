import unittest
from pathlib import Path
import pandas as pd
from .talent_csv import TalentCSV
from .date_format_test import date_format_test
import re


class TestTalentCSV(unittest.TestCase):
    def setUp(self) -> None:
        self.pickle_jar_path = Path(__file__).resolve().parent.parent / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / "talent_csv.pkl")
        self.filenames = pd.read_pickle(self.pickle_jar_path / "talent_csv_filenames.pkl")

    ##########################
    #   YOUR TESTS GO HERE   #
    ##########################


class TestTransformTalentCSV(unittest.TestCase):
    def setUp(self) -> None:
        self.pickle_jar_path = Path(__file__).resolve().parent.parent / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / "talent_csv.pkl")
        self.talent_csv_transform = TalentCSV()
        self.student_information_df, self.invitation_df = self.talent_csv_transform.transform_talent_csv(self.raw_df)

    ############################
    #   TESTING COLUMN NAMES   #
    ############################

    def test_transform_talent_csv_student_information_df_col_names(self) -> None:
        expected = {"student_name", "date", "gender", "dob", "email", "city", "address", "postcode", "phone_number", "uni", "degree"}
        actual = set(self.student_information_df.columns.tolist())
        self.assertEqual(expected, actual)

    def test_transform_talent_csv_invitation_df_col_names(self) -> None:
        expected = {"student_name", "date", "invited_date", "invited_by"}
        actual = set(self.invitation_df.columns.tolist())
        self.assertEqual(expected, actual)

    ################################
    #   TESTING COLUMN DATATYPES   #
    ################################

    def test_transform_talent_csv_student_information_df_datatype(self) -> None:
        expected = {str, list, str, list, str, str, str, str, str, str, str}
        actual = set(self.student_information_df.dtypes.tolist())
        self.assertEqual(expected, actual)

    def test_transform_talent_csv_invitation_df_datatype(self) -> None:
        expected = {str, list, list, str}
        actual = set(self.invitation_df.dtypes.tolist())
        self.assertEqual(expected, actual)

    ###############################
    #   CHECKING FOR DUPLICATES   #
    ###############################

    def test_transform_talent_csv_student_information_df_duplicates(self) -> None:
        actual = self.student_information_df.duplicated().tolist()
        self.assertTrue(all(actual))

    def test_transform_talent_csv_invitation_df_duplicates(self) -> None:
        actual = self.invitation_df.duplicated().tolist()
        self.assertTrue(all(actual))

    #########################################
    #   TESTING FORMATTING OF EACH COLUMN   #
    #########################################

    def test_transform_talent_csv_col_format_person_name(self) -> None:
        list_actual = [
            self.student_information_df["student_name"].tolist(),
            self.invitation_df["student_name"].tolist(),
            self.invitation_df["invited_by"].tolist()
        ]
        for actual in list_actual:
            self.assertTrue(all([a.istitle() for a in actual if not pd.isnull(a)]))
            self.assertTrue(all([a.count('  ') == 0 for a in actual if not pd.isnull(a)]))

    def test_transform_talent_csv_col_format_date(self) -> None:
        actual_list = [
            self.student_information_df["date"].tolist(),
            self.student_information_df["dob"].tolist(),
            self.invitation_df["date"].tolist(),
            self.invitation_df["invited_date"].tolist(),
            self.student_information_df["city"].tolist(),
            self.student_information_df["uni"].tolist()
        ]
        for actual in actual_list:
            date_format_test(actual)

    def test_transform_talent_csv_col_format_gender(self) -> None:
        actual = self.student_information_df["gender"].tolist()
        self.assertTrue(all([a.islower() for a in actual if not pd.isnull(a)]))

    def test_transform_talent_csv_col_format_email(self) -> None:
        actual = self.student_information_df["email"].tolist()
        self.assertTrue(all(['@' in a for a in actual if not pd.isnull(a)]))
        self.assertTrue(all(['.' in a.split('@')[1] for a in actual if not pd.isnull(a)]))

    def test_transform_talent_csv_col_format_address(self) -> None:
        actual = self.student_information_df["address"].tolist()
        is_correct_format = []
        for a in actual:
            if not pd.isnull(a):
                is_correct_format_part = []
                for part in a.split(' '):
                    if not bool(re.search(r'\d', a)):
                        is_correct_format_part.append(a.istitle())
                is_correct_format.append(all(is_correct_format_part))
        self.assertTrue(all(is_correct_format))

    def test_transform_talent_csv_col_format_postcode(self) -> None:
        # valid formats: AA9A 9AA, A9A 9AA, A9 9AA, A99 9AA, AA9 9AA, AA99 9AA
        actual = self.student_information_df["postcode"].tolist()
        re_format = r"^[A-Z]{1,2}[0-9]{1,2}[A-Z]?(\\s*[0-9][A-Z]{1,2})?$"
        self.assertTrue(all([' ' in a for a in actual if not pd.isnull(a)]))
        self.assertTrue(all([re.search(re_format, a) for a in actual if not pd.isnull(a)]))

    def test_transform_talent_csv_col_format_degree(self) -> None:
        actual = self.student_information_df["degree"].tolist()


if __name__ == '__main__':
    unittest.main()
