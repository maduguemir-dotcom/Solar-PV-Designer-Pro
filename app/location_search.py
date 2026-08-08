# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Global Location Search Engine
# Version: 2.2.1
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# Purpose:
# Convert a place name into geographical coordinates.
#
# Example:
# "Kano, Nigeria"
#       ↓
# Latitude + Longitude
#
# The coordinates can then be passed to:
# location_engine.py
#       ↓
# NASA POWER
#
# ==========================================================


# ==========================================================
# SECTION 1 - IMPORTS
# ==========================================================

import requests


# ==========================================================
# SECTION 2 - GEOCODING CONFIGURATION
# ==========================================================

GEOCODING_URL = (
    "https://nominatim.openstreetmap.org/search"
)


# ==========================================================
# SECTION 3 - SEARCH LOCATION
# ==========================================================

def search_location(
    query,
    limit=5
):
    """
    Search for a geographical location using
    OpenStreetMap Nominatim.

    Parameters
    ----------
    query : str
        Location entered by the user.

    limit : int
        Maximum number of results.

    Returns
    -------
    list
        List of matching locations.
    """

    if not query:

        return []


    query = str(query).strip()


    if not query:

        return []


    parameters = {

        "q": query,

        "format": "json",

        "limit": limit,

        "addressdetails": 1

    }


    headers = {

        "User-Agent":
            "Solar-PV-Designer-Pro-Africa/2.2"

    }


    try:

        response = requests.get(

            GEOCODING_URL,

            params=parameters,

            headers=headers,

            timeout=15

        )


        response.raise_for_status()


        results = response.json()


    except requests.RequestException:

        return []


    except ValueError:

        return []


    locations = []


    for result in results:

        try:

            latitude = float(
                result["lat"]
            )

            longitude = float(
                result["lon"]
            )

        except (
            KeyError,
            TypeError,
            ValueError
        ):

            continue


        address = result.get(
            "address",
            {}
        )


        location_name = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("municipality")
            or address.get("county")
            or result.get(
                "display_name",
                "Unknown location"
            )
        )


        country = address.get(
            "country",
            ""
        )


        country_code = address.get(
            "country_code",
            ""
        )


        locations.append({

            "name":
                location_name,

            "country":
                country,

            "country_code":
                country_code.upper(),

            "latitude":
                latitude,

            "longitude":
                longitude,

            "display_name":
                result.get(
                    "display_name",
                    location_name
                )

        })


    return locations


# ==========================================================
# SECTION 4 - FORMAT SEARCH RESULT
# ==========================================================

def format_search_result(
    location
):
    """
    Create a clean human-readable label for
    displaying a location search result.
    """

    if not location:

        return "Unknown location"


    name = location.get(
        "name",
        ""
    )


    country = location.get(
        "country",
        ""
    )


    latitude = location.get(
        "latitude"
    )


    longitude = location.get(
        "longitude"
    )


    if name and country:

        return (
            f"{name}, {country} "
            f"({latitude:.4f}°, "
            f"{longitude:.4f}°)"
        )


    return (
        f"{name} "
        f"({latitude:.4f}°, "
        f"{longitude:.4f}°)"
    )


# ==========================================================
# SECTION 5 - VALIDATE SEARCH RESULT
# ==========================================================

def validate_search_result(
    location
):
    """
    Check that a search result contains usable
    geographical coordinates.
    """

    if not location:

        return False


    latitude = location.get(
        "latitude"
    )


    longitude = location.get(
        "longitude"
    )


    if latitude is None:

        return False


    if longitude is None:

        return False


    try:

        latitude = float(
            latitude
        )

        longitude = float(
            longitude
        )

    except (
        TypeError,
        ValueError
    ):

        return False


    if latitude < -90 or latitude > 90:

        return False


    if longitude < -180 or longitude > 180:

        return False


    return True


# ==========================================================
# SECTION 6 - GET FIRST RESULT
# ==========================================================

def get_first_location(
    query
):
    """
    Return the first valid location found.
    """

    results = search_location(
        query,
        limit=5
    )


    for location in results:

        if validate_search_result(
            location
        ):

            return location


    return None


# ==========================================================
# SECTION 7 - TEST
# ==========================================================

if __name__ == "__main__":

    print(
        "Testing Solar PV Designer Pro "
        "Global Location Search..."
    )


    test_query = "Kano, Nigeria"


    results = search_location(
        test_query
    )


    if not results:

        print(
            "No locations found."
        )

    else:

        print(
            f"Found {len(results)} location(s):"
        )


        for index, location in enumerate(
            results,
            start=1
        ):

            print(
                f"{index}. "
                f"{format_search_result(location)}"
            )
