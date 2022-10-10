import pandas as pd


def filter_col_names(df: pd.DataFrame) -> list[str]:
    headers = []
    for col_name in df.columns.to_list():
        if '_' in col_name and col_name not in headers:
            headers.append(col_name.split("_")[0])
    return headers


def make_individual_dataframes(big_df):
    """ Returns a list of small dataframes, each corresponding to the repeating columns in the previous table"""
    headers_list = filter_col_names(big_df)
    list_of_datafr = []
    for column_name in headers_list:
        small_df = big_df[
            ["name", "trainer", f"{column_name}_W1", f"{column_name}_W2", f"{column_name}_W3", f"{column_name}_W4",
             f"{column_name}_W5", f"{column_name}_W6", f"{column_name}_W7", f"{column_name}_W8", f"{column_name}_W9",
             f"{column_name}_W10"]].copy()
        small_df = pd.wide_to_long(small_df, stubnames=f"{column_name}", i=['name', 'trainer'], j='week', sep='_',
                                   suffix=r'\w+')
        small_df = small_df.reset_index(level=2, drop=False).reset_index()
        list_of_datafr.append(small_df)

    return list_of_datafr


def merge_dataframes(df: pd.DataFrame) -> pd.DataFrame:
    """ The function returns a dataframe which merges the previous,smaller dataframes, having identical "name" and "week" columns  """

    list_of_dataframes = make_individual_dataframes(df)

    return pd.concat(list_of_dataframes, axis=1)  # concatenates the dataframes within the list
