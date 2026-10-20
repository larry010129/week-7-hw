"""Load geographical data into a pandas DataFrame and save it as a CSV file."""

from apputil import (
    GeoLoader,
    build_geo_dataframe,
    fetch_location_data,
    get_geolocator,
)

__all__ = [
    "GeoLoader",
    "build_geo_dataframe",
    "fetch_location_data",
    "get_geolocator",
]


if __name__ == "__main__":
    loader = GeoLoader()

    locations = [
        "Museum of Modern Art",
        "iuyt8765(*&)",
        "Alaska",
        "Franklin's Barbecue",
        "Burj Khalifa",
    ]

    df = loader.build_geo_dataframe(locations)
    df.to_csv("./geo_data.csv")
