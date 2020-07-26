'''
Basically just run the client fixture, do a get request, and assert that the inputs and
outputs are what you expect them to be.

'''

import pytest
from flagging_site.blueprints.api import model_api
from flagging_site.blueprints.flagging import output_model
import pandas as pd

def test_model_output_api_schema(app):
    '''test_model_output_api_schema() should test that the keys are a particular way and the
    values are of a particular type.'''
    with app.app_context():
        list_keys = list(model_api().keys())
        list_values = list(model_api().values())
        for item in list_keys:
            pass
        for item in list_values:
            assert type(item) is str

def test_model_output_api_parameters(app):
    '''test_model_output_api_parameters() should test that hours=10 returns 10 rows of data,
    that setting the reach returns only that reach.'''
    df = output_model()
    row_count = df.shape[0]
    assert row_count == 10

