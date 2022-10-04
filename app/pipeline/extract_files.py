from typing import Any, Union, Type
import boto3
import pandas as pd
import json


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

    def _txt_line_to_list(self, line: str) -> list[str]:
        """
        Convert a line of text into a list. Specifically designed to deal with the known text files in the bucket of
        interest.

        :param str line: line of text
        :return: list of elements in one row
        :rtype: list[str]
        """
        semi_row = line.split('-')
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

    def _get_file(self, key: str) -> tuple[Any, str]:
        """
        Extracts a file from the S3 bucket with given filename.

        :param str key: name of the file to extract
        :return: dictionary / dataframe / nested list that contains data from the file
        :rtype: tuple[Any, str]
        """
        # use different methods depending on the filetype
        if '.json' in key:
            return json.loads(self.s3_client.get_object(Bucket=self.bucket_name, Key=key)["Body"].read()), '.json'
        elif '.csv' in key:
            return pd.read_csv(self.s3_client.get_object(Bucket=self.bucket_name, Key=key)["Body"]), '.csv'
        elif '.txt' in key:
            file_bytes = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)["Body"].readlines()
            # convert bytes to string and clean it using _txt_line_to_list
            file_list = [self._txt_line_to_list(line.decode("utf-8")) for line in file_bytes]
            return file_list, '.txt'

    def _get_all_files_df(self, *, dtype: Union[Type[pd.DataFrame], Type[list]]) -> Union[pd.DataFrame, list[list[str]]]:
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
        bucket_files = self.s3_resource.Bucket(self.bucket_name).objects.all()
        files_list = [[filename.split('/')[0], filename.split('/')[1]] for filename in bucket_files]
        if dtype == list:
            return files_list
        else:
            return pd.DataFrame(files_list, columns=["prefix", "filename"])

    def get_files_as_dataframe(self, recorded_files: list[str]) -> tuple:
        """
        Gather any files that are in S3 that were not recorded before.

        :param list[str] recorded_files: list of files that were recorded previously
        :return: tuple of dataframes containing all .json, .csv, .txt files and dataframe with newly discovered files
        :rtype: tuple
        """
        file_dict = self._get_all_files_df(dtype=list)

        files_dict = {'.json': [], '.csv': [], '.txt': []}
        new_filenames = []

        for _, row in file_dict.iterrows():
            if f"{row['prefix']}/{row['filename']}" not in recorded_files:
                file, ftype = self._get_file(row["filename"])
                files_dict[ftype].append(file)
                new_filenames.append([row['prefix'], row['filename']])

        return (
            pd.DataFrame(files_dict['.json']),
            pd.DataFrame(pd.concat(files_dict['.csv'])),
            pd.DataFrame(files_dict['.txt'], columns=["Name", "Psychometrics", "Presentation"]),
            pd.DataFrame(new_filenames, columns=["prefix", "filename"])
        )
