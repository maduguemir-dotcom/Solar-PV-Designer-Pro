# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Solar Analytics Test Page
# Version: 2.3.0
#
# Purpose:
# Test the solar_analytics.py module before integrating
# it into the main Solar PV Designer Pro application.
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# ==========================================================


# ==========================================================
# SECTION 1 - IMPORTS
# ==========================================================

import streamlit as st

from solar_analytics import (
    analyze_solar_resource
)


# ==========================================================
# SECTION 2 - PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Solar Analytics Test",
    page_icon="☀️",
    layout="wide"
)


# ==========================================================
# SECTION 3 - HEADER
# ==========================================================

st.title(
    "☀️ Solar PV Designer Pro Africa™"
)

st.subheader(
    "Solar Analytics Module Test"
)

st.write(
    """
    This page tests the Solar Analytics module before
    it is integrated into the main application.

    The test uses sample NASA POWER-style data.
    """
)


# ==========================================================
# SECTION 4 - SAMPLE NASA POWER DATA
# ==========================================================

sample_data = {

    "properties": {

        "parameter": {

            "ALLSKY_SFC_SW_DWN": {

                "01": 5.21,
                "02": 5.48,
                "03": 5.72,
                "04": 5.91,
                "05": 5.63,
                "06": 5.31,
                "07": 5.08,
                "08": 5.19,
                "09": 5.47,
                "10": 5.68,
                "11": 5.51,
                "12": 5.29

            },

            "T2M": {

                "01": 25.1,
                "02": 25.8,
                "03": 26.4,
                "04": 26.8,
                "05": 26.2,
                "06": 25.1,
                "07": 24.7,
                "08": 24.9,
                "09": 25.3,
                "10": 25.7,
                "11": 25.4,
                "12": 24.9

            }

        }

    }

}


# ==========================================================
# SECTION 5 - RUN ANALYTICS
# ==========================================================

try:

    analytics = analyze_solar_resource(
        sample_data
    )

    st.success(
        "✅ Solar Analytics module loaded successfully."
    )

except Exception as error:

    st.error(
        f"❌ Solar Analytics test failed: {error}"
    )

    st.stop()


# ==========================================================
# SECTION 6 - SOLAR RESOURCE STATISTICS
# ==========================================================

st.header(
    "☀️ Solar Resource Statistics"
)


solar_stats = analytics[
    "solar_statistics"
]


solar_col1, solar_col2, solar_col3, solar_col4 = (
    st.columns(4)
)


# ----------------------------------------------------------
# Annual Average
# ----------------------------------------------------------

if solar_stats["annual_average"] is not None:

    solar_col1.metric(
        "Annual Average",
        f"{solar_stats['annual_average']:.2f}"
    )

else:

    solar_col1.metric(
        "Annual Average",
        "Unavailable"
    )


# ----------------------------------------------------------
# Maximum
# ----------------------------------------------------------

if solar_stats["maximum"] is not None:

    solar_col2.metric(
        "Maximum",
        f"{solar_stats['maximum']:.2f}"
    )

else:

    solar_col2.metric(
        "Maximum",
        "Unavailable"
    )


# ----------------------------------------------------------
# Best Month
# ----------------------------------------------------------

solar_col3.metric(
    "Best Solar Month",
    solar_stats["best_month"]
    or
    "Unavailable"
)


# ----------------------------------------------------------
# Lowest Month
# ----------------------------------------------------------

solar_col4.metric(
    "Lowest Solar Month",
    solar_stats["lowest_month"]
    or
    "Unavailable"
)


# ==========================================================
# SECTION 7 - TEMPERATURE STATISTICS
# ==========================================================

st.header(
    "🌡️ Temperature Statistics"
)


temperature_stats = analytics[
    "temperature_statistics"
]


temperature_col1, temperature_col2, temperature_col3, temperature_col4 = (
    st.columns(4)
)


# ----------------------------------------------------------
# Annual Average
# ----------------------------------------------------------

if temperature_stats[
    "annual_average"
] is not None:

    temperature_col1.metric(
        "Annual Average",
        (
            f"{temperature_stats['annual_average']:.1f} °C"
        )
    )

else:

    temperature_col1.metric(
        "Annual Average",
        "Unavailable"
    )


# ----------------------------------------------------------
# Maximum
# ----------------------------------------------------------

if temperature_stats[
    "maximum"
] is not None:

    temperature_col2.metric(
        "Maximum",
        (
            f"{temperature_stats['maximum']:.1f} °C"
        )
    )

else:

    temperature_col2.metric(
        "Maximum",
        "Unavailable"
    )


# ----------------------------------------------------------
# Hottest Month
# ----------------------------------------------------------

temperature_col3.metric(
    "Hottest Month",
    temperature_stats[
        "hottest_month"
    ]
    or
    "Unavailable"
)


# ----------------------------------------------------------
# Coolest Month
# ----------------------------------------------------------

temperature_col4.metric(
    "Coolest Month",
    temperature_stats[
        "coolest_month"
    ]
    or
    "Unavailable"
)


# ==========================================================
# SECTION 8 - SEASONAL ANALYSIS
# ==========================================================

st.header(
    "📅 Seasonal Solar Analysis"
)


seasonal = analytics[
    "seasonal_analysis"
]


season_col1, season_col2, season_col3 = (
    st.columns(3)
)


with season_col1:

    st.subheader(
        "☀️ High Solar Months"
    )

    high_months = seasonal[
        "high_solar_months"
    ]

    if high_months:

        for month in high_months:

            st.success(
                month
            )

    else:

        st.info(
            "No high-solar months identified."
        )


with season_col2:

    st.subheader(
        "☀️ Medium Solar Months"
    )

    medium_months = seasonal[
        "medium_solar_months"
    ]

    if medium_months:

        for month in medium_months:

            st.info(
                month
            )

    else:

        st.info(
            "No medium-solar months identified."
        )


with season_col3:

    st.subheader(
        "☁️ Low Solar Months"
    )

    low_months = seasonal[
        "low_solar_months"
    ]

    if low_months:

        for month in low_months:

            st.warning(
                month
            )

    else:

        st.info(
            "No low-solar months identified."
        )


# ==========================================================
# SECTION 9 - MONTHLY SOLAR DATA
# ==========================================================

st.header(
    "📊 Monthly Solar Resource"
)


monthly_solar = analytics[
    "monthly_solar"
]


if monthly_solar:

    st.dataframe(
        monthly_solar,
        use_container_width=True
    )

else:

    st.warning(
        "No monthly solar data was extracted."
    )


# ==========================================================
# SECTION 10 - MONTHLY TEMPERATURE DATA
# ==========================================================

st.header(
    "🌡️ Monthly Temperature"
)


monthly_temperature = analytics[
    "monthly_temperature"
]


if monthly_temperature:

    st.dataframe(
        monthly_temperature,
        use_container_width=True
    )

else:

    st.warning(
        "No monthly temperature data was extracted."
    )


# ==========================================================
# SECTION 11 - BASIC VALIDATION
# ==========================================================

st.header(
    "🧪 Module Validation"
)


solar_count = len(
    monthly_solar
)


temperature_count = len(
    monthly_temperature
)


validation_col1, validation_col2 = (
    st.columns(2)
)


with validation_col1:

    if solar_count == 12:

        st.success(
            "✅ All 12 monthly solar values detected."
        )

    else:

        st.warning(
            f"⚠️ {solar_count}/12 monthly solar values detected."
        )


with validation_col2:

    if temperature_count == 12:

        st.success(
            "✅ All 12 monthly temperature values detected."
        )

    else:

        st.warning(
            f"⚠️ {temperature_count}/12 monthly temperature values detected."
        )


# ==========================================================
# SECTION 12 - RAW ANALYTICS OUTPUT
# ==========================================================

with st.expander(
    "🔍 View Complete Analytics Output"
):

    st.json(
        analytics
    )


# ==========================================================
# SECTION 13 - FINAL TEST STATUS
# ==========================================================

st.divider()


if (
    solar_count == 12
    and
    temperature_count == 12
):

    st.success(
        """
        🎉 SOLAR ANALYTICS TEST PASSED

        The Solar Analytics module successfully:

        • Extracted monthly solar-resource data
        • Extracted monthly temperature data
        • Calculated annual statistics
        • Identified best and lowest solar months
        • Identified hottest and coolest months
        • Performed seasonal classification

        The module is ready for the next stage:
        interactive solar and temperature graphs.
        """
    )

else:

    st.warning(
        """
        ⚠️ SOLAR ANALYTICS TEST INCOMPLETE

        The module loaded, but some monthly values
        were not detected.

        We should correct the data extraction before
        integrating the module into main.py.
        """
    )


# ==========================================================
# SECTION 14 - FOOTER
# ==========================================================

st.divider()


st.caption(
    """
    Solar PV Designer Pro Africa™
    Solar Analytics Test v2.3.0

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu

    For preliminary engineering, education,
    research and demonstration purposes.
    """
)

