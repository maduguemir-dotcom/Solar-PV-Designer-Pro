# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Solar Graph Visualization Test
# Version: 2.3.0
#
# ==========================================================

import streamlit as st

from solar_analytics import (
    analyze_solar_resource
)

from graph_visualization import (
    create_solar_resource_chart,
    create_temperature_chart,
    create_solar_bar_chart,
    create_combined_dataframe
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Solar Graph Test",
    page_icon="📊",
    layout="wide"
)


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "📊 Solar PV Designer Pro Africa™"
)

st.subheader(
    "Solar Graph Visualization Test"
)


# ==========================================================
# SAMPLE DATA
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
# ANALYZE DATA
# ==========================================================

try:

    analytics = analyze_solar_resource(
        sample_data
    )

    st.success(
        "✅ Solar analytics data loaded successfully."
    )

except Exception as error:

    st.error(
        f"❌ Analytics error: {error}"
    )

    st.stop()


# ==========================================================
# EXTRACT DATA
# ==========================================================

monthly_solar = analytics[
    "monthly_solar"
]


monthly_temperature = analytics[
    "monthly_temperature"
]


# ==========================================================
# SOLAR RESOURCE LINE GRAPH
# ==========================================================

st.header(
    "☀️ Monthly Solar Resource"
)


solar_chart = create_solar_resource_chart(
    monthly_solar
)


if solar_chart is not None:

    st.plotly_chart(
        solar_chart,
        use_container_width=True
    )

else:

    st.warning(
        "Solar resource graph could not be created."
    )


# ==========================================================
# TEMPERATURE GRAPH
# ==========================================================

st.header(
    "🌡️ Monthly Temperature"
)


temperature_chart = create_temperature_chart(
    monthly_temperature
)


if temperature_chart is not None:

    st.plotly_chart(
        temperature_chart,
        use_container_width=True
    )

else:

    st.warning(
        "Temperature graph could not be created."
    )


# ==========================================================
# SOLAR BAR GRAPH
# ==========================================================

st.header(
    "📊 Monthly Solar Resource — Bar Chart"
)


solar_bar_chart = create_solar_bar_chart(
    monthly_solar
)


if solar_bar_chart is not None:

    st.plotly_chart(
        solar_bar_chart,
        use_container_width=True
    )

else:

    st.warning(
        "Solar bar chart could not be created."
    )


# ==========================================================
# COMBINED DATA TABLE
# ==========================================================

st.header(
    "📋 Combined Solar & Temperature Data"
)


combined_data = create_combined_dataframe(
    monthly_solar,
    monthly_temperature
)


if not combined_data.empty:

    st.dataframe(
        combined_data,
        use_container_width=True
    )

else:

    st.warning(
        "Combined data could not be created."
    )


# ==========================================================
# TEST STATUS
# ==========================================================

st.divider()


if (
    solar_chart is not None
    and
    temperature_chart is not None
    and
    solar_bar_chart is not None
):

    st.success(
        """
        🎉 GRAPH VISUALIZATION TEST PASSED

        The application successfully generated:

        • Monthly solar-resource line chart
        • Monthly temperature line chart
        • Monthly solar-resource bar chart
        • Combined data table

        The visualization module is ready
        for integration into the main application.
        """
    )

else:

    st.warning(
        """
        ⚠️ GRAPH TEST INCOMPLETE

        One or more graphs could not be generated.
        """
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    """
    Solar PV Designer Pro Africa™
    Graph Visualization Test v2.3.0

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu
    """
)

