import pandas as pd

def prepare_dataframe(data, fields, nested_fields, repeatable_fields):
    for item in data:
        for field in repeatable_fields:
            if field in item:
                for sub_item in item[field]:
                    for key in sub_item.keys():
                        sub_item[key] = str(sub_item[key])

    meta_fields = fields + repeatable_fields
    df = pd.json_normalize(data, sep='__', meta=meta_fields)
    all_fields = fields + nested_fields + repeatable_fields
    column_names = [col.replace('.', '__') for col in all_fields]
    existing_columns = [col for col in column_names if col in df.columns]
    df = df[existing_columns]
    return df
