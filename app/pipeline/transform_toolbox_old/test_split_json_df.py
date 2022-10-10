import unittest
import pandas as pd
from split_json_df import SplitJSONFrame


class TestSplitJSONFrame(unittest.TestCase):
    def setUp(self) -> None:
        self.json_df = pd.read_pickle('./pickle_jar/talent_json.pkl')
        self.split_json = SplitJSONFrame(self.json_df)

    def test_get_trainee_performance_df(self) -> None:
        pass

    def test_get_weakness_df(self) -> None:
        pass

    def test_get_strength_df(self) -> None:
        pass

    def test_get_tech_score_df(self) -> None:
        pass
