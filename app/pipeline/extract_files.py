from typing import Any
import boto3
import pandas as pd
import json


class ExtractFiles:
    def __init__(self, bucket_name: str) -> None:
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')
        self.paginator = self.s3_client.get_paginator('list_objects_v2')

    def _txt_line_to_list(self, line: str) -> list[str]:
        semi_row = line.split('-')
        if len(semi_row) == 2:
            name = semi_row[0].strip(" ,\r\n")
            tests = semi_row[1].split(',')
            psychometrics_val = tests[0].split(':')[1].strip(" ,\r\n")
            presentation_val = tests[1].split(':')[1].strip(" ,\r\n")
            return [name, psychometrics_val, presentation_val]

    def _get_file(self, key: str) -> tuple[Any, str]:
        if '.json' in key:
            return json.loads(self.s3_client.get_object(Bucket=self.bucket_name, Key=key)["Body"].read()), '.json'
        elif '.csv' in key:
            return pd.read_csv(self.s3_client.get_object(Bucket=self.bucket_name, Key=key)["Body"]), '.csv'
        elif '.txt' in key:
            file_bytes = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)["Body"].readlines()
            file_list = [self._txt_line_to_list(line.decode("utf-8")) for line in file_bytes]
            return file_list, '.txt'

    def check_for_new_files(self) -> list[str]:
        pass

    def get_files_as_dataframe(self, prefix: str) -> list[pd.DataFrame]:
        pages = self.paginator.paginate(Bucket=self.bucket_name, Prefix="Talent")

        files_dict = {
            '.json': [],
            '.csv': [],
            '.txt': []
        }

        for page in pages:
            for obj in page["Contents"]:
                file, ftype = self._get_file(obj["Key"])
                files_dict[ftype].append(file)

        return [
            pd.DataFrame(files_dict['.json']),
            pd.concat(files_dict['.csv']),
            pd.DataFrame(files_dict['.txt'], columns=["Name", "Psychometrics", "Presentation"])
        ]

