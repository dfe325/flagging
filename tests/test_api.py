"""
Basically just run the client fixture, do a get request, and assert that the inputs and
outputs are what you expect them to be.

"""

from flagging_site.blueprints.api import model_api
from flagging_site.data.model import reach_2_model
from flagging_site.data.model import process_data
from flagging_site.data.usgs import get_live_usgs_data
from flagging_site.data.hobolink import get_live_hobolink_data

def test_model_output_api_schema(app):
    """test_model_output_api_schema() should test that the keys are a particular way and the
    values are of a particular type."""
    with app.app_context():
        schema = {
            str: list
        }
        res = model_api()
        for key, value in res.items():
            assert type(key) is list(schema.keys())[0]
            assert isinstance(value, list)

def test_model_output_api_parameters(app):
    pass
    """test_model_output_api_parameters() should test that hours=10 returns 10 rows of data,
    that setting the reach returns only that reach."""
    df = reach_2_model(process_data(df_usgs=get_live_usgs_data(), df_hobolink=get_live_hobolink_data('code_for_boston_export_21d')), 10)
    row_count = len(df)
    assert row_count is 10
    #assert <setting the reach returns only that reach>

