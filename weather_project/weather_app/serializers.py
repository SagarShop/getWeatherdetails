from rest_framework import serializers

class WeatherRequestSerializer(serializers.Serializer):
    city = serializers.CharField()
    output_format = serializers.ChoiceField(choices=["json", "xml"])

    
