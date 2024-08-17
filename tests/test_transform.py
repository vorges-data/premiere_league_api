import pandas as pd
from src.transform.transform import prepare_dataframe

def test_prepare_dataframe():
    data = [
        {"field1": "value1", "nested": {"field2": "value2"}}
    ]
    fields = ["field1"]
    nested_fields = ["nested.field2"]
    repeatable_fields = []

    df = prepare_dataframe(data, fields, nested_fields, repeatable_fields)
    assert df.shape[1] == 2
    assert "field1" in df.columns
    assert "nested__field2" in df.columns
