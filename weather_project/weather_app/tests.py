from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch
import json


class WeatherAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/getCurrentWeather"
        self.mock_response = {
            "current": {"temp_c": 24},
            "location": {
                "name": "Bangalore",
                "country": "India",
                "lat": 12.9716,
                "lon": 77.5946
            }
        }

    @patch("weather_app.views.httpx.Client.get")
    def test_json_response(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.mock_response

        payload = {
            "city": "Bangalore",
            "output_format": "json"
        }

        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Weather", response.json())
        self.assertIn("Latitude", response.json())
        self.assertIn("Longitude", response.json())
        self.assertIn("City", response.json())


    @patch("weather_app.views.httpx.Client.get")
    def test_xml_response(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.mock_response

        payload = {
            "city": "Bangalore",
            "output_format": "xml"
        }

        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertIn(b"<City>Bangalore India</City>", response.content)


