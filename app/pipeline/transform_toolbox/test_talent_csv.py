import unittest
from pathlib import Path
import pandas as pd
from .talent_csv import TalentCSV
from .date_format_test import date_format_test
import re


class TestTalentCSV(unittest.TestCase):
    def setUp(self) -> None:
        self.pickle_jar_path = Path(__file__).resolve().parent.parent / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / "talent_csv_v2.pkl")
        self.talent_csv_transform = TalentCSV()

    def test__get_date_column(self) -> None:
        expected = [1, 8, 2015]
        actual = self.talent_csv_transform._get_date_from_string("SomeDir/August2015Whatever.txt")
        self.assertEqual(expected, actual)

    def test__transform_dob(self) -> None:
        expected = [5, 9, 1995]
        actual = self.talent_csv_transform._transform_dob("05/09/1995")
        self.assertEqual(expected, actual)

    def test__transform_invited_date(self) -> None:
        expected = [5, 9, 2019]
        actual = self.talent_csv_transform._transform_invited_date(5.0, "September 2019")
        self.assertEqual(expected, actual)

    def test__normalise_string_upper_case_input(self) -> None:
        expected = "Daniel Storm"
        actual = self.talent_csv_transform._normalise_string("DANIEL STORM")
        self.assertEqual(expected, actual)

    def test__normalise_string_lower_case_input(self) -> None:
        expected = "Daniel Storm"
        actual = self.talent_csv_transform._normalise_string("daniel storm")
        self.assertEqual(expected, actual)

    def test__normalise_string_multiple_spaces(self) -> None:
        expected = "Daniel Storm"
        actual = self.talent_csv_transform._normalise_string("  Daniel   Storm ")
        self.assertEqual(expected, actual)

    def test__normalise_string_just_spaces(self) -> None:
        expected = ""
        actual = self.talent_csv_transform._normalise_string("  ")
        self.assertEqual(expected, actual)


class TestTransformTalentCSV(unittest.TestCase):
    def setUp(self) -> None:
        self.pickle_jar_path = Path(__file__).resolve().parent.parent / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / "talent_csv_v2.pkl")
        self.filenames = pd.read_pickle(self.pickle_jar_path / "talent_csv_filenames.pkl")
        self.talent_csv_transform = TalentCSV()
        self.student_information_df, self.invitation_df = self.talent_csv_transform.transform_talent_csv(self.raw_df)
        self.dt = pd.DataFrame({
            'float': [1.0],
            'int': [1],
            'other': ['foo'],
            'bool': [True]
        })

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
        expected = {self.dt['other'].dtype}
        actual = set(self.student_information_df.dtypes.tolist())
        self.assertEqual(expected, actual)

    def test_transform_talent_csv_invitation_df_datatype(self) -> None:
        expected = {self.dt['other'].dtype}
        actual = set(self.invitation_df.dtypes.tolist())
        self.assertEqual(expected, actual)

    ###############################
    #   CHECKING FOR DUPLICATES   #
    ###############################

    def test_transform_talent_csv_student_information_df_duplicates(self) -> None:
        actual = self.student_information_df
        # lists are not hashable -> convert to tuple
        for key in ["date", "dob"]:
            actual[key] = actual[key].apply(lambda x: tuple(x))
        actual = actual.duplicated().tolist()
        self.assertTrue(not all(actual))

    def test_transform_talent_csv_invitation_df_duplicates(self) -> None:
        actual = self.invitation_df
        # lists are not hashable -> convert to tuple
        for key in ["date", "invited_date"]:
            actual[key] = actual[key].apply(lambda x: tuple(x))
        actual = actual.duplicated().tolist()
        self.assertTrue(not all(actual))

    #########################################
    #   TESTING FORMATTING OF EACH COLUMN   #
    #########################################

    def test_transform_talent_csv_col_format_person_name(self) -> None:
        list_actual = [
            self.student_information_df["student_name"],
            self.invitation_df["student_name"],
            self.invitation_df["invited_by"],
            self.student_information_df["city"],
            self.student_information_df["uni"]
        ]
        for actual in list_actual:
            for row in actual:
                if row:
                    self.assertTrue(row.count('  ') == 0, f"Duplicate spaces in entry {row} in {actual.name}. row.count('  ') = {row.count('  ')}")
                    for word in row.split(' '):
                        if len(word) > 2:
                            self.assertTrue(
                                (word[0].isupper() or word[1].isupper())
                                and not (word[0].isupper() and word[1].isupper()),
                                f"Word '{word}' in entry '{row}' in {actual.name}."
                            )

    def test_transform_talent_csv_col_format_date(self) -> None:
        actual_list = [
            self.student_information_df["date"],
            self.student_information_df["dob"],
            self.invitation_df["date"],
            self.invitation_df["invited_date"]
        ]
        for actual in actual_list:
            date_format_test(actual)

    def test_transform_talent_csv_col_format_gender(self) -> None:
        actual = self.student_information_df["gender"].tolist()
        self.assertTrue(all([a.istitle() for a in actual if not pd.isnull(a)]))

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
        actual = self.student_information_df["postcode"]
        # check for double spaces
        self.assertTrue(all([' ' not in a for a in actual if not pd.isnull(a)]))
        self.assertTrue(all([2 <= len(a) <= 4 for a in actual if not pd.isnull(a)]))

    def test_transform_talent_csv_col_format_degree(self) -> None:
        actual = self.student_information_df["degree"].tolist()


if __name__ == '__main__':
    unittest.main()
