import unittest

import pandas as pd

from loader import build_geo_dataframe, fetch_location_data, get_geolocator


class TestLoader(unittest.TestCase):
    def test_valid_locations(self):
        # Nominatim coordinates sit very close to the Google Maps values,
        # so compare to two decimal places (about 1 km).
        expected = [
            ("Museum of Modern Art", 40.7618552, -73.9782438, "Museum"),
            (
                "USS Alabama Battleship Memorial Park",
                30.684373,
                -88.015316,
                "Park",
            ),
        ]

        df = build_geo_dataframe([row[0] for row in expected])
        df = df.set_index("location")

        for name, latitude, longitude, geo_type in expected:
            self.assertAlmostEqual(
                df.loc[name, "latitude"], latitude, places=2
            )
            self.assertAlmostEqual(
                df.loc[name, "longitude"], longitude, places=2
            )
            self.assertEqual(
                str(df.loc[name, "type"]).lower(), geo_type.lower()
            )

    def test_invalid_location(self):
        geolocator = get_geolocator()
        result = fetch_location_data(geolocator, "asdfqwer1234")

        self.assertEqual(result["location"], "asdfqwer1234")
        self.assertTrue(
            pd.isna(result["latitude"]),
            "A nonexistent location should have NA latitude.",
        )
        self.assertTrue(
            pd.isna(result["longitude"]),
            "A nonexistent location should have NA longitude.",
        )
        self.assertTrue(
            pd.isna(result["type"]),
            "A nonexistent location should have NA type.",
        )


if __name__ == "__main__":
    unittest.main()
