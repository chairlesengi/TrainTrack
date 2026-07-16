"""Failure-path tests for Raspberry Pi RGB matrix mode."""

import unittest
from unittest.mock import MagicMock, patch

from RaspberryPiGui import RGB_matrix


class TestRGBMatrixStartup(unittest.TestCase):
    @patch.object(RGB_matrix, "get_all_stations", side_effect=OSError("offline"))
    @patch.object(RGB_matrix, "initialize_tracker")
    @patch.object(RGB_matrix, "PixelStrip")
    def test_gtfs_failure_does_not_touch_hardware(
        self, mock_pixel_strip, mock_initialize_tracker, _mock_get_all_stations
    ):
        RGB_matrix.run_matrix("F20")

        mock_initialize_tracker.assert_called_once_with()
        mock_pixel_strip.assert_not_called()

    @patch.object(RGB_matrix, "get_all_stations", return_value={"F20": "Avenue X"})
    @patch.object(RGB_matrix, "initialize_tracker")
    @patch.object(RGB_matrix, "PixelStrip")
    def test_invalid_station_exits_without_reload_or_gpio(
        self, mock_pixel_strip, mock_initialize_tracker, _mock_get_all_stations
    ):
        tracker = MagicMock()
        tracker.get_station.side_effect = ValueError("not found")
        mock_initialize_tracker.return_value = tracker

        RGB_matrix.run_matrix("BAD")

        tracker.get_station.assert_called_once_with("BAD")
        mock_initialize_tracker.assert_called_once_with()
        mock_pixel_strip.assert_not_called()


if __name__ == "__main__":
    unittest.main()
