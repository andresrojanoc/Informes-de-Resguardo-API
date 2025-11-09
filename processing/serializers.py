from rest_framework import serializers
from .models import InformeResguardo

class InformeResguardoSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()

    class Meta:
        model = InformeResguardo
        fields = [
            "id",
            "machine_serial",
            "report_datetime",
            "engine_off_timestamp",
            "is_safe",
            "location",
            "distance_to_road_m",
            "is_active",
        ]

    def get_location(self, obj):
        return {
            "latitude": obj.lat,
            "longitude": obj.lon,
        }

