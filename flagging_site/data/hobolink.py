"""
This file handles connections to the HOBOlink API, including cleaning and
formatting of the data that we receive from it.
"""
# TODO:
#  Pandas is inefficient. It should go to SQL, not to Pandas. I am currently
#  using pandas because we do not have any cron jobs or any caching or SQL, but
#  I think in future versions we should not be using Pandas at all.
import io
import requests
import pandas as pd
from flask import abort
from .keys import get_keys
from .keys import offline_mode
from .keys import get_data_store_file_path

# Constants

HOBOLINK_URL = 'http://webservice.hobolink.com/restv2/data/custom/file'
EXPORT_NAME = 'code_for_boston_export'
# Each key is the original column name; the value is the renamed column.
HOBOLINK_COLUMNS = {
    'Time, GMT-04:00': 'time',
    'Pressure, inHg, Charles River Weather Station': 'pressure',
    'PAR, uE, Charles River Weather Station': 'par',
    'Rain, in, Charles River Weather Station': 'rain',
    'RH, %, Charles River Weather Station': 'rh',
    'DewPt, *F, Charles River Weather Station': 'dew_point',
    'Wind Speed, mph, Charles River Weather Station': 'wind_speed',
    'Gust Speed, mph, Charles River Weather Station': 'gust_speed',
    'Wind Dir, *, Charles River Weather Station': 'wind_dir',
    'Water Temp, *F, Charles River Weather Station': 'water_temp',
    'Temp, *F, Charles River Weather Station Air Temp': 'air_temp',
    # 'Batt, V, Charles River Weather Station': 'battery'
}
STATIC_FILE_NAME = 'hobolink.pickle'
# ~ ~ ~ ~


def get_hobolink_data(export_name: str = EXPORT_NAME) -> pd.DataFrame:
    """This function runs through the whole process for retrieving data from
    HOBOlink: first we perform the request, and then we clean the data.

    Args:
        export_name: (str) Name of the "export." On the Hobolink web dashboard,
                     go to Data > Exports and choose a name off the list.

    Returns:
        Pandas Dataframe containing the cleaned-up Hobolink data.
    """
    if offline_mode():
        df = pd.read_pickle(get_data_store_file_path(STATIC_FILE_NAME))
    else:
        res = request_to_hobolink(export_name=export_name)
        df = parse_hobolink_data(res.text)
    return df


def request_to_hobolink(
        export_name: str = EXPORT_NAME,
) -> requests.models.Response:
    """
    Get a request from the Hobolink server.

    Args:
        export_name: (str) Name of the "export." On the Hobolink web dashboard,
                     go to Data > Exports and choose a name off the list.

    Returns:
        Request Response containing the data from the request.
    """
    data = {
        'query': export_name,
        'authentication': get_keys()['hobolink']
    }

    res = requests.post(HOBOLINK_URL, json=data)
    # handle HOBOLINK errors by checking HTTP status code
    # status codes in 400's are client errors, in 500's are server errors
    if res.status_code // 100 in [4, 5]:
        error_message = "link has failed with error # " + str(res.status_code)  
        return abort(res.status_code, error_message)
    return res


def parse_hobolink_data(res: str) -> pd.DataFrame:
    """
    Clean the response from the HOBOlink API.

    Args:
        res: (str) A string of the text received from the post request to the
             HOBOlink API from a successful request.
    Returns:
        Pandas DataFrame containing the HOBOlink data.
    """
    # TODO:
    #  The first half of the output is a yaml-formatted text stream. Is there
    #  anything useful in it? Can we store it and make use of it somehow?
    if isinstance(res, requests.models.Response):
        res = res.text

    # Turn the text from the API response into a Pandas DataFrame.
    split_by = '------------'
    str_table = res[res.find(split_by) + len(split_by):]
    df = pd.read_csv(io.StringIO(str_table), sep=',')

    # Remove all unnecessary columns
    df = df[HOBOLINK_COLUMNS.keys()]

    # Rename the columns to have shorter, friendlier names.
    df = df.rename(columns=HOBOLINK_COLUMNS)

    # Remove rows with missing data (i.e. the 05, 15, 25, 35, 45, and 55 min
    # timestamps, which only include the battery status.)
    df = df.loc[df['water_temp'].notna(), :]

    # Convert time column to Pandas datetime
    df['time'] = pd.to_datetime(df['time'])

    return df
