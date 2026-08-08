# ==========================================================
# Solar PV Designer Pro Africa™
# Data Loading Module
# Version 2.0
# ==========================================================


import pandas as pd



def load_solar_database():

    """
    Load solar location database.

    Returns:
        pandas dataframe containing:
        - Location
        - Country
        - Peak Sun Hours
        - Average Temperature
    """


    file_path = (
        "data/solar_locations.csv"
    )


    try:

        data = pd.read_csv(
            file_path
        )

        return data


    except Exception as error:


        raise Exception(
            f"Solar database loading failed: {error}"
        )




def get_location_data(
        data,
        location):

    """
    Retrieve information
    for selected location.
    """


    result = data[
        data["Location"]
        ==
        location
    ]


    if result.empty:

        return None


    return result.iloc[0]
