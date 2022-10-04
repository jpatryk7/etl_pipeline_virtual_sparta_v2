
import boto3
from pprint import pprint
import pandas as pd
import json



# This is a function which gets the s3 files you need
#
# Enter the arguments of files you need
#
# Prefix i.e Academy or Talent
#
# datatype i.e json or csv or txt




def get_s3_files(prefix: str, datatype: str): # A function which gets the s3 files you need.

    json_content = []
    csv_content = []
    txt_content = []
    academy_contents = []

    bucket_name = "data32-final-project-files"
    s3_client = boto3.client('s3')
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix= prefix)
    for page in pages:
        for obj in page["Contents"]:
            if '.json' in obj["Key"] :
                json_content.append(json.loads(s3_client.get_object(Bucket=bucket_name, Key=obj["Key"])["Body"].read()))
            elif '.csv' in obj["Key"] :
                if prefix == 'Talent':
                    csv_content.append(pd.read_csv(s3_client.get_object(Bucket=bucket_name, Key=obj["Key"])["Body"]))
                else:
                    academy_contents.append(pd.read_csv(s3_client.get_object(Bucket=bucket_name, Key=obj["Key"])["Body"]))
            elif '.txt' in obj["Key"] :
                txt_content.append(s3_client.get_object(Bucket=bucket_name, Key=obj["Key"])["Body"].readlines())

    if datatype == 'json':
        return pd.DataFrame(json_content)
    elif datatype == 'csv' and prefix == 'Talent':
        return pd.concat(csv_content)
    elif datatype == 'csv' and prefix == 'Academy':
        return pd.concat(academy_contents)
    elif datatype == 'txt':
        return txt_content

