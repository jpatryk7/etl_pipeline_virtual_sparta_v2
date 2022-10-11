"""
Class helps to clean data. Input raw data, output is 4 tables with column names:
    1. student name, date, self-dev, geo-flex, financial support, result, course interest
    2. student name, date, strength
    3. student name, date, weakness
    4. student name, date, tech self score, tech score value
"""

import pandas as pd
from typing import Tuple


class TalentJSON:
    def __init__(self) -> None:

    def get_strengths(self) -> dict:
        """
        Create a dictionary with key: name and values: strengths
        :return: dictionary with key: name and values: strength
        :rtype: dict
        """
        strengths = {}
        for i in range(len(self.dataframe)):
            name = self.dataframe.iloc[i, 0]
            strength = self.dataframe.iloc[i, 3]
            strengths[name] = strength
        return strengths

    def get_weaknesses(self) -> dict:
        """
        Create a dictionary with key: name and values: weaknesses
        :return: dictionary with key: name and values: weakness
        :rtype: dict
        """
        weaknesses = {}
        for i in range(len(self.dataframe)):
            name = self.dataframe.iloc[i, 0]
            weakness = self.dataframe.iloc[i, 4]
            weaknesses[name] = weakness
        return weaknesses

    def get_tech_score(self) -> dict:
        """
        Create a dictionary with key: name and values: tech_score
        :return: dictionary with key: name and values: tech_score
        :rtype: dict
        """
        tech_score = {}
        for i in range(len(self.dataframe)):
            name = self.dataframe.iloc[i, 0]
            tech = self.dataframe.iloc[i, 2]
            tech_score[name] = tech
        return tech_score

    def remove_columns(self) -> pd.DataFrame:
        """
        Remove columns tech_self_score, strengths, weaknesses from the main dataframe
        :return: dataframe with removed columns tech_self_score, strengths, weaknesses
        :rtype: pd.DataFrame
        """
        new_dataframe = self.dataframe.drop(columns=['tech_self_score', 'strengths', 'weaknesses'])
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

    def transform_talent_json(self, raw_df: pd.DataFrame) -> Tuple[
        pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Takes raw data and returns tuple with 4 tables:
        1. student name, date, self-dev, geo-flex, financial support, result, course interest
        2. student name, date, strength
        3. student name, date, weakness
        4. student name, date, tech self score, tech score value
        """
        self.dataframe = raw_df
        stre = self.get_strengths()
        weak = self.get_weaknesses()
        tech = self.get_tech_score()

        emp = self.remove_columns()
        strengths = self.attributes_to_df(stre)
        weakness = self.attributes_to_df(weak)
        technic = self.tech_to_df(tech)
        return emp, strengths, weakness, technic


if __name__ == '__main__':
    # run your code here for sanity checks
    pass
