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
    def __init__(self, raw_df: pd.DataFrame) -> None:
        self.dataframe = raw_df

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

    def remove_columns_for_weaknesses(self):
        """
        Create dataframe with name, date and weakness.
        :return: dataframe with name, date and weakness.
        :rtype: pd.DataFrame
        """
        new_dataframe = self.dataframe.drop(columns=['tech_self_score', 'strengths', 'self_development',
                                                     'geo_flex', 'financial_support_self', 'result', 'course_interest'])
        return new_dataframe

    def make_junction_weaknesses(self):
        """
        Splits weakness column to weakness_1, weakness_2, weakness_3.
        :return: dataframe with name, date and weakness_1, weakness_2, weakness_3.
        :rtype: pd.DataFrame
        """
        data = self.remove_columns_for_weaknesses()
        data[['weakness_1', 'weakness_2', 'weakness_3']] = pd.DataFrame(data.weaknesses.tolist(), index=data.index)
        data = data.drop(columns='weaknesses')
        return data

    def normalise_weaknesses(self):
        """
        Merge weaknesses to one column.
        :return: dataframe with columns: student_name, date, weakness.
        :rtype: pd.DataFrame
        """
        headers = ["weakness_1", "weakness_2", "weakness_3"]
        list_of_weaknesses = []
        for column_name in headers:
            small_df = self.make_junction_weaknesses()[['name', 'date', column_name]].copy()
            small_df = (pd.wide_to_long(small_df.reset_index(), stubnames="weakness", i=['index'], j='weaknesses',
                                        sep='_', suffix=r'\w+')).reset_index(level=[0, 1], drop=True)
            list_of_weaknesses.append(small_df)
        result = pd.concat(list_of_weaknesses)
        result = result.rename(columns={"name": "student_name"})
        return result
    def remove_columns_for_strengths(self):
        """
        Create dataframe with name, date and strengths.
        :return: dataframe with name, date and strengths.
        :rtype: pd.DataFrame
        """
        new_dataframe = self.dataframe.drop(columns=['tech_self_score', 'weaknesses', 'self_development',
                                                     'geo_flex', 'financial_support_self', 'result', 'course_interest'])
        return new_dataframe

    def make_junction_strengths(self):
        """
        Splits weakness column to strength_1, strength_2, strength_3.
        :return: dataframe with name, date and strength_1, strength_2, strength_3.
        :rtype: pd.DataFrame
        """
        data = self.remove_columns_for_strengths()
        data[['strength_1', 'strength_2', 'strength_3']] = pd.DataFrame(data.strengths.tolist(), index=data.index)
        data = data.drop(columns='strengths')
        return data

    def normalise_strengths(self):
        """
        Merge weaknesses to one column.
        :return: dataframe with columns: student_name, date, strength.
        :rtype: pd.DataFrame
        """
        headers = ['strength_1', 'strength_2', 'strength_3']
        list_of_strengths = []
        for column_name in headers:
            small_df = self.make_junction_strengths()[['name', 'date', column_name]].copy()
            small_df = (pd.wide_to_long(small_df.reset_index(), stubnames="strength", i=['index'], j='strengths',
                                        sep='_', suffix=r'\w+')).reset_index(level=[0, 1], drop=True)
            list_of_strengths.append(small_df)
        result = pd.concat(list_of_strengths)
        result = result.rename(columns={"name": "student_name"})
        return result

    def remove_columns_for_tech(self):
        """
        Create dataframe with name, date and strengths.
        :return: dataframe with name, date and strengths.
        :rtype: pd.DataFrame
        """
        new_dataframe = self.dataframe.drop(columns=['strengths', 'weaknesses', 'self_development',
                                                     'geo_flex', 'financial_support_self', 'result', 'course_interest'])
        return new_dataframe

    def make_junction_tech(self):
        """
        Splits weakness column to strength_1, strength_2, strength_3.
        :return: dataframe with name, date and strength_1, strength_2, strength_3.
        :rtype: pd.DataFrame
        """
        data = self.remove_columns_for_tech()
        self_score = pd.json_normalize(data['tech_self_score'])
        data = data.drop(columns='tech_self_score')
        data3 = pd.concat([data, self_score], axis=1)
        data3 = data3.rename(columns={'C#':'tech_1', 'Java':'tech_2', 'R':'tech_3', 'JavaScript':'tech_4', 'Python':'tech_5', 'C++':'tech_6', 'Ruby':'tech_7', 'SPSS':'tech_8', 'PHP':'tech_9'})
        return data3

    def normalise_tech(self):
        """
        Merge weaknesses to one column.
        :return: dataframe with columns: student_name, date, strength.
        :rtype: pd.DataFrame
        """
        # headers = ['C#', 'Java', 'R', 'JavaScript', 'Python', 'C++', 'Ruby', 'SPSS', 'PHP']
        headers = ['tech_1', 'tech_2', 'tech_3', 'tech_4', 'tech_5', 'tech_6', 'tech_7', 'tech_8', 'tech_9']
        list_of_tech = []
        for column_name in headers:
            small_df = self.make_junction_tech()[['name', 'date', column_name]].copy()
            small_df = (pd.wide_to_long(small_df.reset_index(), stubnames='tech', i=['index'], j='skill',
                                        suffix=r'\w+')).reset_index(level=1, drop=False)
            list_of_tech.append(small_df)
        result = pd.concat(list_of_tech)
        result = result.rename(columns={"name": "student_name", 'tech':'value'})
        result = result.replace(['_1', '_2', '_3', '_4', '_5','_6','_7','_8','_9'], ['C#', 'Java', 'R', 'JavaScript', 'Python', 'C++', 'Ruby', 'SPSS', 'PHP'])
        return result

    def remove_columns(self) -> pd.DataFrame:
        """
        Remove columns tech_self_score, strengths, weaknesses from the main dataframe
        :return: dataframe with removed columns tech_self_score, strengths, weaknesses
        :rtype: pd.DataFrame
        """
        new_dataframe = self.dataframe.drop(columns=['tech_self_score', 'strengths', 'weaknesses'])
        new_dataframe = new_dataframe.rename(columns={"name": "student_name",
                                                      "financial_support_self": "financial_support"})
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

    def transform_talent_json(self) -> Tuple[
        pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Takes raw data and returns tuple with 4 tables:
        1. student name, date, self-dev, geo-flex, financial support, result, course interest
        2. student name, date, strength
        3. student name, date, weakness
        4. student name, date, tech self score, tech score value
        """
        # stre = self.get_strengths()
        # weak = self.get_weaknesses()
        tech = self.get_tech_score()

        emp = self.remove_columns()
        # strengths = self.attributes_to_df(stre)
        strengths = self.normalise_strengths()
        # weakness = self.attributes_to_df(weak)
        weakness = self.normalise_weaknesses()
        technic = self.tech_to_df(tech)
        return emp, weakness, strengths, technic


from pathlib import Path

if __name__ == '__main__':
    pickle_jar_path = Path(__file__).parent.parent.resolve() / "pickle_jar"
    raw = pd.read_pickle(pickle_jar_path / 'talent_json.pkl')
    check = TalentJSON(raw)
    # pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    # tech = check.get_tech_score()
    # tech2 = check.tech_to_df(tech)
    # print(tech2.head(2))
    # weak = check.get_weaknesses()
    # weak2 = check.attributes_to_df(weak)
    # print(weak2.head(2))
    # weak = check.normalise_weaknesses()
    # print(weak.head(2))

    # aaa = check.make_junction_strengths()
    # print(aaa.head(3))
    # bbb = check.make_junction_tech()
    # print(bbb.head(3))
    tech = check.normalise_tech()
    print(tech)

    # work = check.get_weaknesses()
    # work_df = check.attributes_to_df(work)
    # weak = check.remove_columns_for_weaknesses()
    # print(weak.head(1))
    # weak = check.norma
    # print(work_df)
    # colu = set(check.remove_columns_for_weaknesses().columns.tolist())
    # print(colu)
    pass
