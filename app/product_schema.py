# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# Product Category Schema
# Version: 2.4.4
#
# Defines category-specific fields for the Product Library.
# ==========================================================


# ==========================================================
# CATEGORY DEFINITIONS
# ==========================================================

PRODUCT_CATEGORY_SCHEMAS = {

    # ======================================================
    # SOLAR PANEL
    # ======================================================

    "Solar Panel": {

        "icon": "☀️",

        "description":
            "Photovoltaic solar module specifications.",

        "sections": {

            "Electrical Specifications": [

                {
                    "name": "rated_power_w",
                    "label": "Rated Power",
                    "type": "number",
                    "unit": "W",
                    "min": 0,
                    "step": 10,
                    "default": 0
                },

                {
                    "name": "voc_v",
                    "label": "Open-Circuit Voltage (Voc)",
                    "type": "number",
                    "unit": "V",
                    "min": 0,
                    "step": 0.1,
                    "default": 0
                },

                {
                    "name": "vmp_v",
                    "label": "Maximum Power Voltage (Vmp)",
                    "type": "number",
                    "unit": "V",
                    "min": 0,
                    "step": 0.1,
                    "default": 0
                },

                {
                    "name": "isc_a",
                    "label": "Short-Circuit Current (Isc)",
                    "type": "number",
                    "unit": "A",
                    "min": 0,
                    "step": 0.1,
                    "default": 0
                },

                {
                    "name": "imp_a",
                    "label": "Maximum Power Current (Imp)",
                    "type": "number",
                    "unit": "A",
                    "min": 0,
                    "step": 0.1,
                    "default": 0
                },

                {
                    "name": "efficiency_percent",
                    "label": "Module Efficiency",
                    "type": "number",
                    "unit": "%",
                    "min": 0,
                    "max": 100,
                    "step": 0.1,
                    "default": 0
                },

                {
                    "name": "max_system_voltage_v",
                    "label": "Maximum System Voltage",
                    "type": "number",
                    "unit": "V",
                    "min": 0,
                    "step": 10,
                    "default": 0
                },

                {
                    "name": "max_series_fuse_a",
                    "label": "Maximum Series Fuse",
                    "type": "number",
                    "unit": "A",
                    "min": 0,
                    "step": 1,
                    "default": 0
                }

            ],

            "Physical Specifications": [

                {
                    "name": "length_mm",
                    "label": "Length",
                    "type": "number",
                    "unit": "mm",
                    "min": 0,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "width_mm",
                    "label": "Width",
                    "type": "number",
                    "unit": "mm",
                    "min": 0,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "thickness_mm",
                    "label": "Thickness",
                    "type": "number",
                    "unit": "mm",
                    "min": 0,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "weight_kg",
                    "label": "Weight",
                    "type": "number",
                    "unit": "kg",
                    "min": 0,
                    "step": 0.1,
                    "default": 0
                },

                {
                    "name": "cell_count",
                    "label": "Number of Cells",
                    "type": "number",
                    "unit": "cells",
                    "min": 0,
                    "step": 1,
                    "default": 0
                }

            ],

            "Performance & Warranty": [

                {
                    "name": "temperature_coefficient_pmax",
                    "label": "Temperature Coefficient Pmax",
                    "type": "number",
                    "unit": "%/°C",
                    "step": 0.01,
                    "default": 0
                },

                {
                    "name": "temperature_coefficient_voc",
                    "label": "Temperature Coefficient Voc",
                    "type": "number",
                    "unit": "%/°C",
                    "step": 0.01,
                    "default": 0
                },

                {
                    "name": "product_warranty_years",
                    "label": "Product Warranty",
                    "type": "number",
                    "unit": "years",
                    "min": 0,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "performance_warranty_years",
                    "label": "Performance Warranty",
                    "type": "number",
                    "unit": "years",
                    "min": 0,
                    "step": 1,
                    "default": 0
                }

            ]

        }

    },


    # ======================================================
    # BATTERY
    # ======================================================

    "Battery": {

        "icon": "🔋",

        "description":
            "Battery storage system specifications.",

        "sections": {

            "Electrical Specifications": [

                {
                    "name": "nominal_voltage_v",
                    "label": "Nominal Voltage",
                    "type": "number",
                    "unit": "V",
                    "min": 0,
                    "step": 0.1,
                    "default": 0
                },

                {
                    "name": "capacity_ah",
                    "label": "Capacity",
                    "type": "number",
                    "unit": "Ah",
                    "min": 0,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "energy_kwh",
                    "label": "Nominal Energy",
                    "type": "number",
                    "unit": "kWh",
                    "min": 0,
                    "step": 0.1,
                    "default": 0
                },

                {
                    "name": "max_charge_current_a",
                    "label": "Maximum Charge Current",
                    "type": "number",
                    "unit": "A",
                    "min": 0,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "max_discharge_current_a",
                    "label": "Maximum Discharge Current",
                    "type": "number",
                    "unit": "A",
                    "min": 0,
                    "step": 1,
                    "default": 0
                }

            ],

            "Battery Performance": [

                {
                    "name": "depth_of_discharge_percent",
                    "label": "Maximum Depth of Discharge",
                    "type": "number",
                    "unit": "%",
                    "min": 0,
                    "max": 100,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "round_trip_efficiency_percent",
                    "label": "Round-Trip Efficiency",
                    "type": "number",
                    "unit": "%",
                    "min": 0,
                    "max": 100,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "cycle_life",
                    "label": "Cycle Life",
                    "type": "number",
                    "unit": "cycles",
                    "min": 0,
                    "step": 100,
                    "default": 0
                },

                {
                    "name": "operating_temperature_min_c",
                    "label": "Minimum Operating Temperature",
                    "type": "number",
                    "unit": "°C",
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "operating_temperature_max_c",
                    "label": "Maximum Operating Temperature",
                    "type": "number",
                    "unit": "°C",
                    "step": 1,
                    "default": 0
                }

            ],

            "Physical Specifications": [

                {
                    "name": "length_mm",
                    "label": "Length",
                    "type": "number",
                    "unit": "mm",
                    "min": 0,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "width_mm",
                    "label": "Width",
                    "type": "number",
                    "unit": "mm",
                    "min": 0,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "height_mm",
                    "label": "Height",
                    "type": "number",
                    "unit": "mm",
                    "min": 0,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "weight_kg",
                    "label": "Weight",
                    "type": "number",
                    "unit": "kg",
                    "min": 0,
                    "step": 0.1,
                    "default": 0
                }

            ],

            "Warranty": [

                {
                    "name": "warranty_years",
                    "label": "Warranty",
                    "type": "number",
                    "unit": "years",
                    "min": 0,
                    "step": 1,
                    "default": 0
                }

            ]

        }

    },


    # ======================================================
    # INVERTER
    # ======================================================

    "Inverter": {

        "icon": "⚡",

        "description":
            "Solar inverter and power conversion specifications.",

        "sections": {

            "Power Specifications": [

                {
                    "name": "rated_power_w",
                    "label": "Rated Output Power",
                    "type": "number",
                    "unit": "W",
                    "min": 0,
                    "step": 100,
                    "default": 0
                },

                {
                    "name": "surge_power_w",
                    "label": "Surge Power",
                    "type": "number",
                    "unit": "W",
                    "min": 0,
                    "step": 100,
                    "default": 0
                },

                {
                    "name": "continuous_power_w",
                    "label": "Continuous Power",
                    "type": "number",
                    "unit": "W",
                    "min": 0,
                    "step": 100,
                    "default": 0
                }

            ],

            "DC Specifications": [

                {
                    "name": "dc_nominal_voltage_v",
                    "label": "DC Nominal Voltage",
                    "type": "number",
                    "unit": "V",
                    "min": 0,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "dc_max_voltage_v",
                    "label": "Maximum DC Voltage",
                    "type": "number",
                    "unit": "V",
                    "min": 0,
                    "step": 10,
                    "default": 0
                },

                {
                    "name": "mppt_min_voltage_v",
                    "label": "MPPT Minimum Voltage",
                    "type": "number",
                    "unit": "V",
                    "min": 0,
                    "step": 10,
                    "default": 0
                },

                {
                    "name": "mppt_max_voltage_v",
                    "label": "MPPT Maximum Voltage",
                    "type": "number",
                    "min": 0,
                    "step": 10,
                    "default": 0
                },

                {
                    "name": "max_pv_input_power_w",
                    "label": "Maximum PV Input Power",
                    "type": "number",
                    "unit": "W",
                    "min": 0,
                    "step": 100,
                    "default": 0
                }

            ],

            "AC Specifications": [

                {
                    "name": "ac_output_voltage_v",
                    "label": "AC Output Voltage",
                    "type": "number",
                    "unit": "V",
                    "min": 0,
                    "step": 1,
                    "default": 230
                },

                {
                    "name": "frequency_hz",
                    "label": "Output Frequency",
                    "type": "number",
                    "unit": "Hz",
                    "min": 0,
                    "step": 1,
                    "default": 50
                },

                {
                    "name": "phase",
                    "label": "Phase",
                    "type": "select",
                    "options": [
                        "Single Phase",
                        "Three Phase"
                    ],
                    "default": "Single Phase"
                }

            ],

            "Performance & Features": [

                {
                    "name": "efficiency_percent",
                    "label": "Maximum Efficiency",
                    "type": "number",
                    "unit": "%",
                    "min": 0,
                    "max": 100,
                    "step": 0.1,
                    "default": 0
                },

                {
                    "name": "mppt_count",
                    "label": "Number of MPPT Trackers",
                    "type": "number",
                    "min": 0,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "transfer_time_ms",
                    "label": "Transfer Time",
                    "type": "number",
                    "unit": "ms",
                    "min": 0,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "warranty_years",
                    "label": "Warranty",
                    "type": "number",
                    "unit": "years",
                    "min": 0,
                    "step": 1,
                    "default": 0
                }

            ]

        }

    },


    # ======================================================
    # CHARGE CONTROLLER
    # ======================================================

    "Charge Controller": {

        "icon": "🔌",

        "description":
            "Solar charge controller specifications.",

        "sections": {

            "Controller Specifications": [

                {
                    "name": "controller_type",
                    "label": "Controller Type",
                    "type": "select",
                    "options": [
                        "MPPT",
                        "PWM"
                    ],
                    "default": "MPPT"
                },

                {
                    "name": "system_voltage_v",
                    "label": "System Voltage",
                    "type": "select",
                    "options": [
                        "12 V",
                        "24 V",
                        "48 V",
                        "12/24 V",
                        "12/24/48 V"
                    ],
                    "default": "48 V"
                },

                {
                    "name": "max_charge_current_a",
                    "label": "Maximum Charge Current",
                    "type": "number",
                    "unit": "A",
                    "min": 0,
                    "step": 5,
                    "default": 0
                },

                {
                    "name": "max_pv_input_power_w",
                    "label": "Maximum PV Input Power",
                    "type": "number",
                    "unit": "W",
                    "min": 0,
                    "step": 100,
                    "default": 0
                },

                {
                    "name": "max_pv_voltage_v",
                    "label": "Maximum PV Voltage",
                    "type": "number",
                    "unit": "V",
                    "min": 0,
                    "step": 10,
                    "default": 0
                },

                {
                    "name": "efficiency_percent",
                    "label": "Efficiency",
                    "type": "number",
                    "unit": "%",
                    "min": 0,
                    "max": 100,
                    "step": 0.1,
                    "default": 0
                },

                {
                    "name": "warranty_years",
                    "label": "Warranty",
                    "type": "number",
                    "unit": "years",
                    "min": 0,
                    "step": 1,
                    "default": 0
                }

            ]

        }

    },


    # ======================================================
    # MOUNTING STRUCTURE
    # ======================================================

    "Mounting Structure": {

        "icon": "🏗️",

        "description":
            "Solar PV mounting and support structure.",

        "sections": {

            "Structure Specifications": [

                {
                    "name": "structure_type",
                    "label": "Structure Type",
                    "type": "select",
                    "options": [
                        "Roof Mount",
                        "Ground Mount",
                        "Pole Mount",
                        "Carport",
                        "Custom"
                    ],
                    "default": "Roof Mount"
                },

                {
                    "name": "material",
                    "label": "Material",
                    "type": "select",
                    "options": [
                        "Aluminium",
                        "Galvanized Steel",
                        "Stainless Steel",
                        "Other"
                    ],
                    "default": "Aluminium"
                },

                {
                    "name": "panel_capacity",
                    "label": "Panel Capacity",
                    "type": "number",
                    "unit": "panels",
                    "min": 0,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "roof_type",
                    "label": "Roof / Installation Type",
                    "type": "select",
                    "options": [
                        "Metal Roof",
                        "Tile Roof",
                        "Concrete Roof",
                        "Ground",
                        "Other"
                    ],
                    "default": "Metal Roof"
                },

                {
                    "name": "wind_rating_kmh",
                    "label": "Wind Rating",
                    "type": "number",
                    "unit": "km/h",
                    "min": 0,
                    "step": 10,
                    "default": 0
                },

                {
                    "name": "warranty_years",
                    "label": "Warranty",
                    "type": "number",
                    "unit": "years",
                    "min": 0,
                    "step": 1,
                    "default": 0
                }

            ]

        }

    },


    # ======================================================
    # SOLAR CABLE
    # ======================================================

    "Solar Cable": {

        "icon": "🔗",

        "description":
            "Solar DC cable and conductor specifications.",

        "sections": {

            "Cable Specifications": [

                {
                    "name": "cross_section_mm2",
                    "label": "Cable Cross-Section",
                    "type": "number",
                    "unit": "mm²",
                    "min": 0,
                    "step": 0.5,
                    "default": 0
                },

                {
                    "name": "conductor_material",
                    "label": "Conductor Material",
                    "type": "select",
                    "options": [
                        "Copper",
                        "Aluminium"
                    ],
                    "default": "Copper"
                },

                {
                    "name": "cable_length_m",
                    "label": "Cable Length",
                    "type": "number",
                    "unit": "m",
                    "min": 0,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "voltage_rating_v",
                    "label": "Voltage Rating",
                    "type": "number",
                    "unit": "V",
                    "min": 0,
                    "step": 100,
                    "default": 0
                },

                {
                    "name": "temperature_rating_c",
                    "label": "Temperature Rating",
                    "type": "number",
                    "unit": "°C",
                    "min": 0,
                    "step": 5,
                    "default": 0
                },

                {
                    "name": "uv_resistant",
                    "label": "UV Resistant",
                    "type": "select",
                    "options": [
                        "Yes",
                        "No"
                    ],
                    "default": "Yes"
                }

            ]

        }

    },


    # ======================================================
    # PROTECTION
    # ======================================================

    "Protection": {

        "icon": "🛡️",

        "description":
            "Electrical protection and switching equipment.",

        "sections": {

            "Protection Specifications": [

                {
                    "name": "protection_type",
                    "label": "Protection Type",
                    "type": "select",
                    "options": [
                        "DC Breaker",
                        "AC Breaker",
                        "Fuse",
                        "SPD",
                        "Isolator",
                        "RCD",
                        "RCBO",
                        "Other"
                    ],
                    "default": "DC Breaker"
                },

                {
                    "name": "rated_voltage_v",
                    "label": "Rated Voltage",
                    "type": "number",
                    "unit": "V",
                    "min": 0,
                    "step": 10,
                    "default": 0
                },

                {
                    "name": "rated_current_a",
                    "label": "Rated Current",
                    "type": "number",
                    "unit": "A",
                    "min": 0,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "poles",
                    "label": "Number of Poles",
                    "type": "number",
                    "min": 1,
                    "step": 1,
                    "default": 1
                },

                {
                    "name": "breaking_capacity_ka",
                    "label": "Breaking Capacity",
                    "type": "number",
                    "unit": "kA",
                    "min": 0,
                    "step": 1,
                    "default": 0
                },

                {
                    "name": "dc_or_ac",
                    "label": "Application",
                    "type": "select",
                    "options": [
                        "DC",
                        "AC",
                        "AC/DC"
                    ],
                    "default": "DC"
                },

                {
                    "name": "warranty_years",
                    "label": "Warranty",
                    "type": "number",
                    "unit": "years",
                    "min": 0,
                    "step": 1,
                    "default": 0
                }

            ]

        }

    },


    # ======================================================
    # OTHER
    # ======================================================

    "Other": {

        "icon": "📦",

        "description":
            "Other solar and electrical equipment.",

        "sections": {

            "General Specifications": [

                {
                    "name": "description",
                    "label": "Description",
                    "type": "text",
                    "default": ""
                },

                {
                    "name": "rating",
                    "label": "Rating / Capacity",
                    "type": "text",
                    "default": ""
                },

                {
                    "name": "warranty_years",
                    "label": "Warranty",
                    "type": "number",
                    "unit": "years",
                    "min": 0,
                    "step": 1,
                    "default": 0
                }

            ]

        }

    }

}


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def get_product_schema(category):

    return PRODUCT_CATEGORY_SCHEMAS.get(
        category,
        PRODUCT_CATEGORY_SCHEMAS["Other"]
    )


def get_product_categories():

    return list(
        PRODUCT_CATEGORY_SCHEMAS.keys()
    )


def get_category_icon(category):

    schema = get_product_schema(
        category
    )

    return schema.get(
        "icon",
        "📦"
    )


def get_category_description(category):

    schema = get_product_schema(
        category
    )

    return schema.get(
        "description",
        ""
    )


def get_category_sections(category):

    schema = get_product_schema(
        category
    )

    return schema.get(
        "sections",
        {}
    )


def get_category_fields(category):

    sections = get_category_sections(
        category
    )

    fields = []

    for section_fields in sections.values():

        fields.extend(
            section_fields
        )

    return fields


def get_field_names(category):

    return [

        field["name"]

        for field
        in get_category_fields(category)

    ]


def get_field(
    category,
    field_name
):

    fields = get_category_fields(
        category
    )

    for field in fields:

        if field["name"] == field_name:

            return field

    return None


def validate_category_fields(
    category,
    specifications
):

    errors = []

    fields = get_category_fields(
        category
    )

    for field in fields:

        field_name = field["name"]

        if field_name not in specifications:

            continue

        value = specifications[
            field_name
        ]

        if field.get("type") == "number":

            try:

                numeric_value = float(
                    value
                )

                if (
                    "min" in field
                    and numeric_value < field["min"]
                ):

                    errors.append(
                        f"{field['label']} "
                        f"cannot be below "
                        f"{field['min']}."
                    )

                if (
                    "max" in field
                    and numeric_value > field["max"]
                ):

                    errors.append(
                        f"{field['label']} "
                        f"cannot exceed "
                        f"{field['max']}."
                    )

            except (
                ValueError,
                TypeError
            ):

                errors.append(
                    f"{field['label']} "
                    f"must be numeric."
                )

        if field.get("type") == "select":

            options = field.get(
                "options",
                []
            )

            if (
                value
                and value not in options
            ):

                errors.append(
                    f"{field['label']} "
                    f"has an invalid selection."
                )

    return errors


def get_default_specifications(
    category
):

    defaults = {}

    for field in get_category_fields(
        category
    ):

        if "default" in field:

            defaults[
                field["name"]
            ] = field["default"]

    return defaults


def get_required_fields(
    category
):

    return [

        field["name"]

        for field
        in get_category_fields(category)

        if field.get(
            "required",
            False
        )

    ]
