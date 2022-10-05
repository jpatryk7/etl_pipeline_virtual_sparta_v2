from get_s3_files import *
import boto3
import pandas as pd
import json


class TraineePerformance:

    def __init__(self, file_location: str, file_type: str):
        self.file_location = file_location
        self.file_type = file_type

    def read_json_from_s3(self, file_location: str, file_type: str) -> pd.DataFrame:
        """
        Use function from get_s3_files to read json files. Return dataframe with raw data.
        :param str file_location: location of the file
        :param str file_type: extension of file to be read
        :return: dataframe with raw data
        :rtype: pd.DataFrame
        """
        json_files = get_s3_files(self.file_location, self.file_type)
        dataframe = pd.DataFrame(json_files)
        return dataframe

    def get_strengths(self, df: pd.DataFrame) -> dict:
        """
        Create a dictionary with key: name and values: strengths
        :param pd.DataFrame df: dataframe with all raw data
        :return: dictionary with key: name and values: strength
        :rtype: dict
        """
        strengths = {}
        for i in range(len(df)):
            name = df.iloc[i, 0]
            strength = df.iloc[i, 3]
            strengths[name] = strength
        return strengths

    def get_weaknesses(self, df: pd.DataFrame) -> dict:
        """
        Create a dictionary with key: name and values: weaknesses
        :param pd.DataFrame df: dataframe with all raw data
        :return: dictionary with key: name and values: weakness
        :rtype: dict
        """
        weaknesses = {}
        for i in range(len(df)):
            name = df.iloc[i, 0]
            weakness = df.iloc[i, 4]
            weaknesses[name] = weakness
        return weaknesses

    def get_tech_score(self, df: pd.DataFrame) -> dict:
        """
        Create a dictionary with key: name and values: tech_score
        :param pd.DataFrame df: dataframe with all raw data
        :return: dictionary with key: name and values: tech_score
        :rtype: dict
        """
        tech_score = {}
        for i in range(len(df)):
            name = df.iloc[i, 0]
            tech = df.iloc[i, 2]
            tech_score[name] = tech
        return tech_score

    def remove_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove columns tech_self_score, strengths, weaknesses from the main dataframe
        :param pd.DataFrame df: dataframe with all raw data
        :return: dataframe with removed columns tech_self_score, strengths, weaknesses
        :rtype: pd.DataFrame
        """
        new_dataframe = df.drop(columns=['tech_self_score', 'strengths', 'weaknesses'])
        return new_dataframe

    def attributes_to_df(self, attribute: dict) -> pd.DataFrame:
        """
        Converts a dictionary with attributes to a dataframe
        :param dict attribute: takes a dictionary with key: name and values: attribute
        :return: dataframe with key: name and columns: attribute
        :rtype: pd.DataFrame
        """
        df = pd.DataFrame.from_dict(attribute, orient='index')
        return df

    def tech_to_df(self, tech: dict) -> pd.DataFrame:
        """
        Converts a dictionary with dictionary to a dataframe
        :param dict tech: takes a dictionary with key: name and values: tech_score
        :return:
        :rtype: pd.DataFrame
        """
        tech_score = pd.DataFrame.from_dict(tech)
        tech_score = tech_score.transpose()
        return tech_score
