"""
Note:
    Generate four tables:
        1. student name, date, self-dev, geo-flex, financial support, result, course interest
        2. student name, date, weakness
        3. student name, date, strength
        4. student name, date, tech self score, tech score value
"""
import pandas as pd


class TalentJSON:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.dataframe = pd.DataFrame(dataframe)


    # def transform_talent_json(self, raw_df: pd.DataFrame) -> tuple[
    #     pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    #     """
    #     Describe what the function does here
    #     """
    #     #################################
    #     #   YOUR OTHER CODE GOES HERE   #
    #     #################################
    #     pass

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


if __name__ == '__main__':
    # run your code here for sanity checks
    pass
