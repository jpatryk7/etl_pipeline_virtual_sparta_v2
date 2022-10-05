from get_s3_files import *
import pandas as pd



def text_to_csv():
    txt_files = get_s3_files('Talent', 'txt')
    rows = []
    for file in txt_files:
        for line in file:
            semi_row = line.decode("utf-8").split('-')
            if len(semi_row) == 2:
                name = semi_row[0].strip(" ,\r\n")
                tests = semi_row[1].split(',')
                psychometrics_val = tests[0].split(':')[1].strip(" ,\r\n")
                presentation_val = tests[1].split(':')[1].strip(" ,\r\n")
                rows.append([name, psychometrics_val, presentation_val])
    txt_df = pd.DataFrame(rows, columns=["Name", "Psychometrics", "Presentation"])
    txt_df['Name'] = txt_df['Name'].str.title()
    return txt_df

def convert_fraction(df,col,col2):
    for num in range(len(df)):
        df[col][num] = eval(df[col][num]) * 100
        df[col2][num] = eval(df[col2][num]) * 100
    return df
