"""Geocode place names and collect them into a pandas DataFrame."""

import time

import pandas as pd
from geopy.exc import GeocoderServiceError
from geopy.geocoders import Nominatim


# Nominatim's usage policy allows at most one request per second.
_MIN_REQUEST_INTERVAL = 1.0
_last_request_at = 0.0


def _missing_location(loc):
    """Return a row that keeps the place name and uses NA elsewhere."""
    return {
        "location": loc,
        "latitude": float("nan"),
        "longitude": float("nan"),
        "type": float("nan"),
    }


def _wait_for_nominatim():
    """Pause so repeated lookups stay within Nominatim's rate limit."""
    global _last_request_at
    elapsed = time.time() - _last_request_at
    if elapsed < _MIN_REQUEST_INTERVAL:
        time.sleep(_MIN_REQUEST_INTERVAL - elapsed)
    _last_request_at = time.time()


def get_geolocator(agent="h501-student"):
    """Initiate a Nominatim geolocator instance given an ``agent``.

    Parameters
    ----------
    agent : str, optional
        Agent name for Nominatim, by default ``'h501-student'``.

    Returns
    -------
    geopy.geocoders.Nominatim
        Geolocator used to look up place names.
    """
    return Nominatim(user_agent=agent)


def fetch_location_data(geolocator, loc):
    """Look up one place name.

    Parameters
    ----------
    geolocator : geopy.geocoders.Nominatim
        Geolocator that performs the lookup.
    loc : str
        Place name to geocode.

    Returns
    -------
    dict
        Location name, latitude, longitude, and place type. Latitude,
        longitude, and type are NA when the place cannot be found.
    """
    try:
        _wait_for_nominatim()
        location = geolocator.geocode(loc, timeout=10)
    except GeocoderServiceError:
        return _missing_location(loc)

    if location is None:
        return _missing_location(loc)

    raw_type = (location.raw or {}).get("type")
    if isinstance(raw_type, str) and raw_type:
        geo_type = raw_type.capitalize()
    else:
        geo_type = float("nan")

    return {
        "location": loc,
        "latitude": location.latitude,
        "longitude": location.longitude,
        "type": geo_type,
    }


def build_geo_dataframe(locations, geolocator=None):
    """Geocode each place name and return a DataFrame.

    Parameters
    ----------
    locations : list of str
        Place names to look up.
    geolocator : geopy.geocoders.Nominatim, optional
        Geolocator to use. A new one is created when omitted.

    Returns
    -------
    pandas.DataFrame
        One row per place, with columns ``location``, ``latitude``,
        ``longitude``, and ``type``.
    """
    if geolocator is None:
        geolocator = get_geolocator()

    rows = [fetch_location_data(geolocator, loc) for loc in locations]
    return pd.DataFrame(rows)


class GeoLoader:
    """Geocode a list of place names into a DataFrame.

    Parameters
    ----------
    agent : str, optional
        Nominatim user-agent, by default ``'h501-student'``.
    """

    def __init__(self, agent="h501-student"):
        self.geolocator = get_geolocator(agent)

    def fetch_location_data(self, loc):
        """Return latitude, longitude, and type for one place name.

        Parameters
        ----------
        loc : str
            Place name to geocode.

        Returns
        -------
        dict
            Location name plus coordinates and type, or NA values when
            the place cannot be found.
        """
        return fetch_location_data(self.geolocator, loc)

    def build_geo_dataframe(self, locations):
        """Geocode ``locations`` and return a DataFrame.

        Parameters
        ----------
        locations : list of str
            Place names to look up.

        Returns
        -------
        pandas.DataFrame
            One row per place name.
        """
        return build_geo_dataframe(locations, self.geolocator)
