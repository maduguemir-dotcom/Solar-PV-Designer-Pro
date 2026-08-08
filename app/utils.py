# ==========================================================
# Solar PV Designer Pro Africa™
# Utility Functions
# Version 2.0
# ==========================================================



def format_currency(value):

    """
    Convert number into
    readable currency format.
    """

    return (
        f"${value:,.0f}"
    )




def format_number(value):

    """
    Format decimal numbers.
    """

    return (
        f"{value:.2f}"
    )




def validate_positive(value):

    """
    Check that input value
    is greater than zero.
    """

    return value > 0
