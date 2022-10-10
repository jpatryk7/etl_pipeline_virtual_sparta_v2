import random
import unittest
from app.pipeline.extract_files import *


class TestExtractFiles(unittest.TestCase):

    # speeds up running tests
    all_items_in_s3 = [obj.key for obj in boto3.resource('s3').Bucket("data32-final-project-files").objects.all()]

    def setUp(self) -> None:
        self.bucket_name = "data32-final-project-files"
        self.extract = ExtractFiles(self.bucket_name)
        self.json_filename = "Talent/10397.json"
        self.csv_filename = "Talent/March2019Applicants.csv"
        self.txt_filename = "Talent/Sparta Day 6 February 2019.txt"

    def test__txt_line_to_list(self) -> None:
        """
        E.g.
        input: "ROLLINS DALGARDNO -  Psychometrics: 50/100, Presentation: 22/32"
        expected output: ["ROLLINS DALGARDNO", "50/100", "22/32"]
        """
        expected = ["ROLLINS DALGARDNO", "50/100", "22/32"]
        actual = txt_line_to_list("ROLLINS DALGARDNO -  Psychometrics: 50/100, Presentation: 22/32")
        self.assertEqual(expected, actual)

    def test__get_file_json(self) -> None:
        """
        check if the returned file is a dict type
        """
        actual = self.extract._get_file(self.json_filename)[0]
        print(actual.columns)
        self.assertIsInstance(actual, pd.DataFrame)

    def test__get_file_csv(self) -> None:
        """
        check if the returned file is a dataframe type
        """
        actual = self.extract._get_file(self.csv_filename)[0]
        self.assertIsInstance(actual, pd.DataFrame)

    def test__get_file_txt(self) -> None:
        """
        check if the returned file is a nested list
        """
        actual = self.extract._get_file(self.txt_filename)[0]
        self.assertIsInstance(actual, pd.DataFrame)

    def test__get_file_unknown_type(self) -> None:
        """
        Check if the function returns None when provided with unexpected filetype.
        """
        expected = None
        actual = self.extract._get_file("some_filename.png")
        self.assertEqual(expected, actual)

    def test__get_all_files_df_dataframe(self) -> None:
        """
        check if the returned type is matching the specified
        """
        actual = self.extract._get_all_filenames_df(dtype=pd.DataFrame)
        self.assertIsInstance(actual, pd.DataFrame)

    def test__get_all_files_df_list(self) -> None:
        """
        check if the returned type is matching the specified
        """
        actual = self.extract._get_all_filenames_df(dtype=list)
        self.assertIsInstance(actual, list)

    def test__get_all_files_df_list_len(self) -> None:
        """
        check if the number of elements is correct
        """
        expected = len(self.all_items_in_s3)
        actual = len(self.extract._get_all_filenames_df(dtype=list))
        self.assertEqual(expected, actual)

    def test__get_all_files_df_dataframe_len(self) -> None:
        """
        check if the number of elements is correct
        """
        expected = len(self.all_items_in_s3)
        actual = len(self.extract._get_all_filenames_df(dtype=pd.DataFrame))
        self.assertEqual(expected, actual)

    def test_get_files_as_df_new_file(self) -> None:
        """
        Check if the function returns all 4 dataframes /w one entry in new_filenames_df when provided recorded_files
        having one less file than all_items_in_s3
        """
        expected = self.all_items_in_s3[0]
        _, filenames = self.extract.get_files_as_df(self.all_items_in_s3[1:])
        actual = '/'.join(filenames.values.tolist()[0])
        self.assertEqual(expected, actual)

    def test_get_files_as_df_no_recorder_files(self) -> None:
        """
        Check if the function returns all_items_in_s3 when provided empty recorded_files
        """
        # create subset
        recorded_files = []
        expected = 15
        actual = 0
        for ext in ['.json', '.csv', '.txt']:
            # all files of given type
            ext_files = [fname for fname in self.all_items_in_s3 if ext in fname]
            actual += len(self.extract.get_files_as_df(ext_files[0:5], ext=ext)[0])

        self.assertEqual(expected, actual)

    def test_get_files_as_df_all_files_recorded(self) -> None:
        """
        Check if the function returns None when provided recorded_files same as all_items_in_s3
        """
        expected = None
        actual = self.extract.get_files_as_df(self.all_items_in_s3)
        self.assertEqual(expected, actual)
