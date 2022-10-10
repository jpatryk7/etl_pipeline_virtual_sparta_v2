import pandas as pd


class SplitJSONFrame:
    # ['name', 'date', 'tech_self_score', 'strengths', 'weaknesses',
    #        'self_development', 'geo_flex', 'financial_support_self', 'result',
    #        'course_interest']
    def __init__(self, json_df: pd.DataFrame) -> None:
        self.df = json_df

    def get_trainee_performance_df(self) -> pd.DataFrame:
        pass

    def get_weakness_df(self) -> pd.DataFrame:
        pass

    def get_strength_df(self) -> pd.DataFrame:
        pass

    def get_tech_score_df(self) -> pd.DataFrame:
        pass
