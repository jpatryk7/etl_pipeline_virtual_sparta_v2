import unittest
from pathlib import Path
import pandas as pd
from talent_json import TalentJSON


class TestTalentJSON(unittest.TestCase):
    def setUp(self) -> None:
        self.pickle_jar_path = Path(__file__).parent.parent.resolve() / "pickle_jar"
        self.raw_df = pd.read_pickle(self.pickle_jar_path / 'talent_json.pkl')
        self.filenames = pd.read_pickle(self.pickle_jar_path / "talent_json_filenames.pkl")

    ##########################
    #   YOUR TESTS GO HERE   #
    ##########################

    def test_transform_talent_txt(self):
        ##############################
        #   DON'T DO ANYTHING HERE   #
        ##############################
        pass

    def test_get_strengths(self):
        expected = {'Stillmann Castano': ['Charisma']}
        actual = TalentJSON(self.raw_df.head(1)).get_strengths()
        self.assertEqual(expected, actual)

    def test_get_strengths_instance(self):
        actual = TalentJSON(self.raw_df.head(1)).get_strengths()
        self.assertIsInstance(actual, dict)

    def test_get_weaknesses(self):
        expected = {'Stillmann Castano': ['Distracted', 'Impulsive', 'Introverted']}
        actual = TalentJSON(self.raw_df.head(1)).get_weaknesses()
        self.assertEqual(expected, actual)

    def test_get_weaknesses_instance(self):
        actual = TalentJSON(self.raw_df.head(1)).get_weaknesses()
        self.assertIsInstance(actual, dict)

    def test_tech_score(self):
        expected = {'Stillmann Castano': {'C#': 6, 'Java': 5, 'R': 2, 'JavaScript': 2}}
        actual = TalentJSON(self.raw_df.head(1)).get_tech_score()
        self.assertEqual(expected, actual)

    def test_get_tech_score_instance(self):
        actual = TalentJSON(self.raw_df.head(1)).get_tech_score()
        self.assertIsInstance(actual, dict)

    def test_remove_columns(self):
        expected = pd.DataFrame({'name': ['Stillmann Castano'],
                                 'date': ['22/08/2019'],
                                 'self_development': ['Yes'],
                                 'geo_flex': ['Yes'],
                                 'financial_support_self': ['Yes'],
                                 'result': ['Pass'],
                                 'course_interest': ['Business']})
        actual = TalentJSON(self.raw_df.head(1)).remove_columns()
        pd.testing.assert_frame_equal(expected, actual)

    def test_remove_columns_instance(self):
        actual = TalentJSON(self.raw_df.head(1)).remove_columns()
        self.assertIsInstance(actual, pd.DataFrame)

    def test_attributes_to_df(self):
        expected = pd.DataFrame({0: ['Charisma']}).set_index(pd.Series(['Stillmann Castano']))
        actual = TalentJSON(self.raw_df.head(1)).attributes_to_df(TalentJSON(self.raw_df.head(1)).get_strengths())
        pd.testing.assert_frame_equal(expected, actual)

    def test_attributes_to_df_instance(self):
        actual = TalentJSON(self.raw_df.head(1)).attributes_to_df(TalentJSON(self.raw_df.head(1)).get_strengths())
        self.assertIsInstance(actual, pd.DataFrame)

    def test_tech_to_df(self):
        expected = pd.DataFrame({'C#': [6],
                                 'Java': [5],
                                 'JavaScript': [2],
                                 'R': [2]}).set_index(pd.Series(['Stillmann Castano']))
        actual = TalentJSON(self.raw_df.head(1)).tech_to_df(TalentJSON(self.raw_df.head(1)).get_tech_score())
        pd.testing.assert_frame_equal(expected, actual)

    def test_tech_to_df_instance(self):
        actual = TalentJSON(self.raw_df.head(1)).tech_to_df(TalentJSON(self.raw_df.head(1)).get_tech_score())
        self.assertIsInstance(actual, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
