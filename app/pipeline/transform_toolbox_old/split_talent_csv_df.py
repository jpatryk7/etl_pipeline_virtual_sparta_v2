import pandas as pd


class SplitTalentCSVFrame:
    # ['id', 'name', 'gender', 'dob', 'email', 'city', 'address', 'postcode',
    #  'phone_number', 'uni', 'degree', 'invited_date', 'month', 'invited_by']
    def __init__(self, talent_csv_df: pd.DataFrame):
        pass

    def get_student_performance_df(self,
                                   test_score_df: pd.DataFrame,
                                   course_df: pd.DataFrame,
                                   academy_performance_df: pd.DataFrame,
                                   trainee_performance_df: pd.DataFrame) -> pd.DataFrame:
        pass

    def get_invitation_df(self) -> pd.DataFrame:
        pass
