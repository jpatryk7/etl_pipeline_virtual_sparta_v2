import pandas as pd
from .academy_csv_transpose import merge_dataframes


class SplitAcademyCSVFrame:
    def __init__(self, academy_csv_df) -> None:
        self.academy_csv_df = merge_dataframes(academy_csv_df)
        # drop duplicates
        self.academy_csv_df = self.academy_csv_df.T.drop_duplicates().T
        # convert float to int
        self.academy_csv_df = self.academy_csv_df.convert_dtypes()
        # drop rows with just <NA>
        self.academy_csv_df = self.academy_csv_df.dropna(thresh=6)
        # change "week" column values from Wn to n
        self.academy_csv_df["week"] = self.academy_csv_df["week"].apply(lambda x: int(x[1:]))

    def get_trainer_df(self) -> pd.DataFrame:
        return self.academy_csv_df[['trainer']].copy().drop_duplicates()

    def get_academy_performance_df(self) -> pd.DataFrame:
        return self.academy_csv_df


if __name__ == "__main__":
    s = SplitAcademyCSVFrame(pd.read_pickle("../pickle_jar/academy_csv.pkl"))
    trainer_df = s.get_trainer_df()
    a_perf_df = s.get_academy_performance_df()
    print(trainer_df)
    print(a_perf_df)
