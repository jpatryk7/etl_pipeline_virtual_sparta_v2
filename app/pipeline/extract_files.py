from typing import Union, Type
import boto3
import pandas as pd
import json


def txt_line_to_list(line: str) -> list[str]:
    """
    Convert a line of text into a list. Specifically designed to deal with the known text files in the bucket of
    interest.

    :param str line: line of text
    :return: list of elements in one row
    :rtype: list[str]
    """
    semi_row = line.split(' - ')
    # first few lines have less than three parts - they are describing the file, and we don't need them
    if len(semi_row) == 2:
        # first part is the name of the test participant
        name = semi_row[0].strip(" ,\r\n")
        # second part describes scores
        tests = semi_row[1].split(',')
        # split scores and remove names of each test
        psychometrics_val = tests[0].split(':')[1].strip(" ,\r\n")
        presentation_val = tests[1].split(':')[1].strip(" ,\r\n")
        # column names are hard-coded later to reduce complexity of the code
        return [name, psychometrics_val, presentation_val]


class ExtractFiles:
    def __init__(self, bucket_name: str) -> None:
        """
        Set up client and resource for S3 connection.

        :param str bucket_name: name of the S3 bucket
        """
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')
        self.paginator = self.s3_client.get_paginator('list_objects_v2')

    def _get_json_file(self, key: str) -> pd.DataFrame:
        """
        Extracts a json file from the S3 bucket with given filename.

        :param str key: name of the file to extract
        :return: single-row dataframe with json file content
        :rtype: pd.DataFrame
        """
        s3_obj_body = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)["Body"]
        return pd.DataFrame([json.loads(s3_obj_body.read())])

    def _get_csv_file(self, key: str) -> pd.DataFrame:
        """
        Extracts a csv file from the S3 bucket with given filename.

        :param str key: name of the file to extract
        :return: single-row dataframe with csv file content
        :rtype: pd.DataFrame
        """
        return pd.read_csv(self.s3_client.get_object(Bucket=self.bucket_name, Key=key)["Body"])

    def _get_txt_file(self, key: str) -> pd.DataFrame:
        """
        Extracts a txt file from the S3 bucket with given filename and converts its content to appropriate row-like
        structure.

        :param str key: name of the file to extract
        :return: single-row dataframe with txt file content
        :rtype: pd.DataFrame
        """
        file_bytes = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)["Body"].readlines()
        # convert bytes to string and clean it using _txt_line_to_list
        file_list = []
        for i, line in enumerate(file_bytes):
            if i > 2:
                file_list.append(txt_line_to_list(line.decode("utf-8")))
        return pd.DataFrame(file_list, columns=["Name", "Psychometrics", "Presentation"])

    def _get_file(self, key: str) -> Union[tuple[pd.DataFrame, int], None]:
        """
        Extracts a file from the S3 bucket with given filename.

        :param str key: name of the file to extract
        :return: dictionary / dataframe / nested list that contains data from the file
        :rtype: Union[tuple[Any, str], None]
        """
        # use different methods depending on the filetype
        if '.json' in key:
            return self._get_json_file(key), 0
        elif '.csv' in key:
            return self._get_csv_file(key), 1
        elif '.txt' in key:
            return self._get_txt_file(key), 2
        else:
            return None

    def _get_all_filenames_df(self, *, dtype: Union[Type[pd.DataFrame], Type[list]]) -> Union[pd.DataFrame, list[list[str]]]:
        """
        Returns all files in the bucket in one of the following formats:
            prefix      filename
        1   <prefix1>   <filename1>
        2   <prefix1>   <filename2>
        3   <prefix2>   <filename3>
        ...

        [
            [<prefix1>, <filename1>],
            [<prefix1>, <filename2>],
            [<prefix2>, <filename3>],
            ...
        ]

        :param Union[Type[pd.DataFrame], Type[list]] dtype: pd.DataFrame or list keywords
        :return: dataframe with all prefixes and filenames in the S3 bucket
        :rtype: pd.DataFrame
        """
        bucket_files = [obj.key for obj in self.s3_resource.Bucket(self.bucket_name).objects.all()]
        files_list = [[filename.split('/')[0], filename.split('/')[1]] for filename in bucket_files]
        if dtype == list:
            return files_list
        else:
            return pd.DataFrame(files_list, columns=["prefix", "filename"])

    def get_files_as_df(self, recorded_files: list[str]) -> Union[tuple[list[pd.DataFrame], pd.DataFrame], None]:
        """
        Gather any files that are in S3 that were not recorded before.

        :param list[str] recorded_files: list of files that were recorded previously
        :return: tuple of list of dataframes containing all .json, .csv, .txt files and a dataframe with newly
        discovered files; it may return none if no new files present in the s3
        :rtype: Union[tuple[list[pd.DataFrame], pd.DataFrame], None]
        """
        filenames = self._get_all_filenames_df(dtype=list)

        files = [[], [], []]
        new_filenames = []

        for i, row in enumerate(filenames):
            fname = f"{row[0]}/{row[1]}"
            if fname not in recorded_files:
                file_df, ftype_index = self._get_file(fname)
                files[ftype_index].append(file_df)
                new_filenames.append([row[0], row[1]])

        if new_filenames:
            return (
                *[pd.concat(df_list, ignore_index=True) for df_list in files if df_list],
                pd.DataFrame(new_filenames, columns=["prefix", "filename"])
            )
        else:
            return None
