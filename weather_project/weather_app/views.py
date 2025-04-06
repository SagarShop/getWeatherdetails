import httpx
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import WeatherRequestSerializer
from dicttoxml import dicttoxml
from django.http import HttpResponse
from django.conf import settings

class GetCurrentWeather(APIView):
    def post(self, request):
        serializer = WeatherRequestSerializer(data=request.data)
        if serializer.is_valid():
            city = serializer.validated_data['city']
            output_format = serializer.validated_data['output_format']

            headers = {
                "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
                "X-RapidAPI-Host": settings.RAPIDAPI_HOST
            }
            params = {"q": city}

            try:
                response = httpx.get(
                    "https://weatherapi-com.p.rapidapi.com/current.json",
                    headers=headers,
                    params={"q": city}
                )
                response.raise_for_status()
            except httpx.RequestError as e:
                return Response({"error": "Network error", "details": str(e)},
                                status=status.HTTP_502_BAD_GATEWAY)
            except httpx.HTTPStatusError:
                return Response({"error": "Weather API failed"},
                                status=status.HTTP_502_BAD_GATEWAY)

            data = response.json()
            current = data.get("current", {})
            location = data.get("location", {})

            result = {
                "Weather": f"{current.get('temp_c')} C",
                "Latitude": str(location.get("lat")),
                "Longitude": str(location.get("lon")),
                "City": f"{location.get('name')} {location.get('country')}"
            }

            if output_format == "json":
                return Response(result)
            elif output_format == "xml":
                xml_data = dicttoxml(result, custom_root='root', attr_type=False)
                return HttpResponse(xml_data, content_type='application/xml')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
