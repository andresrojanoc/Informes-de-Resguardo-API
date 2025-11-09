from django.db import models

class InformeResguardo(models.Model):
    machine_serial = models.CharField(max_length=50)
    report_datetime = models.DateTimeField()
    engine_off_timestamp = models.DateTimeField()
    lat = models.FloatField()
    lon = models.FloatField()
    is_safe = models.BooleanField()
    distance_to_road_m = models.FloatField()
    is_active = models.BooleanField(default=True)  # 👈 campo requerido por el contrato

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Informe {self.machine_serial} - {self.report_datetime}"


