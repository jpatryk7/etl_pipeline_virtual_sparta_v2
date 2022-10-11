"""
Note:
    Use both content of the file and the name of each to generate one table:
        1. student name, date (the one in the filename), psychometrics, presentation
"""
import pandas as pd


class TalentTXT:
    def __init__(self) -> None:
        pass

    ##############################
    #   YOUR FUNCTIONS GO HERE   #
    ##############################

    def transform_talent_txt(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        """
        Describe what the function does here
        """
        #################################
        #   YOUR OTHER CODE GOES HERE   #
        #################################
        pass

    def replace_hyphens(self, text: str):
        ''' Replaces Hyphens in a text file with a comma. Useful to transform messy text files '''

        return text.replace("-", ",")

    def replace_colon(self, text: str):
        ''' Replaces all instances of a colon with a comma'''
        return text.replace(":",",")

if __name__ == '__main__':
    # run your code here for sanity checks
    pass
