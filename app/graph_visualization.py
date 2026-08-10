# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# GRAPH VISUALIZATION ENGINE
# Version: 2.3
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# Purpose:
# Create interactive solar-resource and temperature graphs
# from NASA POWER / solar analytics data.
#
# ==========================================================

import pandas as pd
import plotly.express as px


# ==========================================================
# SECTION 1 - INTERNAL DATA CONVERTER
# ==========================================================

def _to_dataframe(data):
    """
    Convert different NASA POWER / analytics data structures
    into a pandas DataFrame.

    Supported formats include:

    - pandas DataFrame
    - list of dictionaries
    - dictionary
    - dictionary containing monthly data
    """

    if data is None:
        return pd.DataFrame()

    # ------------------------------------------------------
    # Already a DataFrame
    # ------------------------------------------------------

    if isinstance(data, pd.DataFrame):

        return data.copy()


    # ------------------------------------------------------
    # List / tuple
    # ------------------------------------------------------

    if isinstance(data, (list, tuple)):

        try:

            return pd.DataFrame(data)

        except Exception:

            return pd.DataFrame()


    # ------------------------------------------------------
    # Dictionary
    # ------------------------------------------------------

    if isinstance(data, dict):

        # ----------------------------------------------
        # Look for common nested monthly-data keys
        # ----------------------------------------------

        possible_keys = [
            "monthly",
            "monthly_data",
            "monthly_solar",
            "monthly_temperature",
            "data",
            "values",
            "results"
        ]

        for key in possible_keys:

            if key in data:

                nested = data[key]

                if isinstance(
                    nested,
                    (list, tuple, dict)
                ):

                    try:

                        return pd.DataFrame(
                            nested
                        )

                    except Exception:

                        pass


        # ----------------------------------------------
        # Try direct dictionary conversion
        # ----------------------------------------------

        try:

            return pd.DataFrame(data)

        except Exception:

            return pd.DataFrame()


    return pd.DataFrame()


# ==========================================================
# SECTION 2 - FIND COLUMN
# ==========================================================

def _find_column(
    dataframe,
    possible_names
):
    """
    Find a column using several possible names.
    """

    if dataframe is None:
        return None

    if dataframe.empty:
        return None

    # Exact match
    for name in possible_names:

        if name in dataframe.columns:

            return name

    # Case-insensitive match
    normalized = {
        str(column).strip().lower():
            column
        for column in dataframe.columns
    }

    for name in possible_names:

        key = str(name).strip().lower()

        if key in normalized:

            return normalized[key]

    return None


# ==========================================================
# SECTION 3 - PREPARE SOLAR DATA
# ==========================================================

def _prepare_solar_dataframe(data):

    dataframe = _to_dataframe(data)

    if dataframe.empty:

        return pd.DataFrame(
            columns=[
                "Month",
                "Solar Resource"
            ]
        )

    # ------------------------------------------------------
    # Identify month column
    # ------------------------------------------------------

    month_column = _find_column(
        dataframe,
        [
            "Month",
            "month",
            "MONTH",
            "Date",
            "date",
            "YearMonth",
            "year_month",
            "period"
        ]
    )

    # ------------------------------------------------------
    # Identify solar column
    # ------------------------------------------------------

    solar_column = _find_column(
        dataframe,
        [
            "Solar Resource",
            "solar_resource",
            "solar",
            "Solar",
            "ALLSKY_SFC_SW_DWN",
            "ALLSKY",
            "GHI",
            "ghi",
            "irradiance",
            "Irradiance",
            "Peak_Sun_Hours",
            "peak_sun_hours"
        ]
    )

    if solar_column is None:

        # Try to find a numeric column
        numeric_columns = (
            dataframe
            .select_dtypes(
                include="number"
            )
            .columns
        )

        if len(numeric_columns) > 0:

            solar_column = numeric_columns[0]

    if solar_column is None:

        return pd.DataFrame(
            columns=[
                "Month",
                "Solar Resource"
            ]
        )

    # ------------------------------------------------------
    # Create month values
    # ------------------------------------------------------

    if month_column is not None:

        months = dataframe[
            month_column
        ]

    else:

        months = list(
            range(
                1,
                len(dataframe) + 1
            )
        )

    result = pd.DataFrame({

        "Month":
            months,

        "Solar Resource":
            pd.to_numeric(
                dataframe[
                    solar_column
                ],
                errors="coerce"
            )

    })

    result = result.dropna(
        subset=[
            "Solar Resource"
        ]
    )

    return result


# ==========================================================
# SECTION 4 - PREPARE TEMPERATURE DATA
# ==========================================================

def _prepare_temperature_dataframe(data):

    dataframe = _to_dataframe(data)

    if dataframe.empty:

        return pd.DataFrame(
            columns=[
                "Month",
                "Temperature"
            ]
        )

    # ------------------------------------------------------
    # Month
    # ------------------------------------------------------

    month_column = _find_column(
        dataframe,
        [
            "Month",
            "month",
            "MONTH",
            "Date",
            "date",
            "YearMonth",
            "year_month",
            "period"
        ]
    )

    # ------------------------------------------------------
    # Temperature
    # ------------------------------------------------------

    temperature_column = _find_column(
        dataframe,
        [
            "Temperature",
            "temperature",
            "TEMP",
            "T2M",
            "T2M_AVG",
            "Average_Temperature",
            "average_temperature",
            "Avg_Temperature",
            "temperature_2m"
        ]
    )

    if temperature_column is None:

        numeric_columns = (
            dataframe
            .select_dtypes(
                include="number"
            )
            .columns
        )

        if len(numeric_columns) > 0:

            # In many cases temperature is the second
            # numeric column.
            if len(numeric_columns) > 1:

                temperature_column = (
                    numeric_columns[1]
                )

            else:

                temperature_column = (
                    numeric_columns[0]
                )

    if temperature_column is None:

        return pd.DataFrame(
            columns=[
                "Month",
                "Temperature"
            ]
        )

    # ------------------------------------------------------
    # Month
    # ------------------------------------------------------

    if month_column is not None:

        months = dataframe[
            month_column
        ]

    else:

        months = list(
            range(
                1,
                len(dataframe) + 1
            )
        )

    result = pd.DataFrame({

        "Month":
            months,

        "Temperature":
            pd.to_numeric(
                dataframe[
                    temperature_column
                ],
                errors="coerce"
            )

    })

    result = result.dropna(
        subset=[
            "Temperature"
        ]
    )

    return result


# ==========================================================
# SECTION 5 - SOLAR RESOURCE LINE CHART
# ==========================================================

def create_solar_resource_chart(
    monthly_solar
):
    """
    Create an interactive monthly solar-resource chart.
    """

    dataframe = _prepare_solar_dataframe(
        monthly_solar
    )

    if dataframe.empty:

        return None

    figure = px.line(
        dataframe,
        x="Month",
        y="Solar Resource",
        markers=True,
        title="Monthly Solar Resource"
    )

    figure.update_layout(
        xaxis_title="Month",
        yaxis_title="Solar Resource",
        hovermode="x unified"
    )

    return figure


# ==========================================================
# SECTION 6 - TEMPERATURE LINE CHART
# ==========================================================

def create_temperature_chart(
    monthly_temperature
):
    """
    Create an interactive monthly temperature chart.
    """

    dataframe = _prepare_temperature_dataframe(
        monthly_temperature
    )

    if dataframe.empty:

        return None

    figure = px.line(
        dataframe,
        x="Month",
        y="Temperature",
        markers=True,
        title="Monthly Average Temperature"
    )

    figure.update_layout(
        xaxis_title="Month",
        yaxis_title="Temperature (°C)",
        hovermode="x unified"
    )

    return figure


# ==========================================================
# SECTION 7 - SOLAR BAR CHART
# ==========================================================

def create_solar_bar_chart(
    monthly_solar
):
    """
    Create an interactive monthly solar-resource bar chart.
    """

    dataframe = _prepare_solar_dataframe(
        monthly_solar
    )

    if dataframe.empty:

        return None

    figure = px.bar(
        dataframe,
        x="Month",
        y="Solar Resource",
        title="Monthly Solar Resource"
    )

    figure.update_layout(
        xaxis_title="Month",
        yaxis_title="Solar Resource"
    )

    return figure


# ==========================================================
# SECTION 8 - COMBINED DATAFRAME
# ==========================================================

def create_combined_dataframe(
    monthly_solar,
    monthly_temperature
):
    """
    Combine solar and temperature data into one DataFrame.
    """

    solar_df = _prepare_solar_dataframe(
        monthly_solar
    )

    temperature_df = _prepare_temperature_dataframe(
        monthly_temperature
    )

    if solar_df.empty and temperature_df.empty:

        return pd.DataFrame()

    if solar_df.empty:

        return temperature_df

    if temperature_df.empty:

        return solar_df

    # ------------------------------------------------------
    # Combine
    # ------------------------------------------------------

    try:

        combined = pd.merge(
            solar_df,
            temperature_df,
            on="Month",
            how="outer"
        )

        return combined

    except Exception:

        # Fallback if month formats differ
        combined = pd.concat(
            [
                solar_df.reset_index(
                    drop=True
                ),
                temperature_df[
                    "Temperature"
                ].reset_index(
                    drop=True
                )
            ],
            axis=1
        )

        return combined


# ==========================================================
# SECTION 9 - SIMPLE TEST
# ==========================================================

if __name__ == "__main__":

    test_data = [

        {
            "Month": "January",
            "Solar Resource": 5.2,
            "Temperature": 24.1
        },

        {
            "Month": "February",
            "Solar Resource": 5.5,
            "Temperature": 25.0
        },

        {
            "Month": "March",
            "Solar Resource": 5.7,
            "Temperature": 25.8
        },

        {
            "Month": "April",
            "Solar Resource": 5.1,
            "Temperature": 25.2
        },

        {
            "Month": "May",
            "Solar Resource": 4.9,
            "Temperature": 24.7
        },

        {
            "Month": "June",
            "Solar Resource": 4.8,
            "Temperature": 23.9
        }
    ]

    solar_chart = (
        create_solar_resource_chart(
            test_data
        )
    )

    temperature_chart = (
        create_temperature_chart(
            test_data
        )
    )

    solar_bar = (
        create_solar_bar_chart(
            test_data
        )
    )

    print(
        "Graph visualization module loaded successfully."
    )

    print(
        f"Solar chart: {solar_chart is not None}"
    )

    print(
        f"Temperature chart: {temperature_chart is not None}"
    )

    print(
        f"Solar bar chart: {solar_bar is not None}"
    )

