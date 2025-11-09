from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import InformeResguardo
from .serializers import InformeResguardoSerializer
from .locations import parse, Caminos
import threading
import os

class DataProcessingView(APIView):
    def post(self, request):
        thread = threading.Thread(target=self.run_data_processing, daemon=True)
        thread.start()
        return Response({"message": "Data processing initiated successfully."}, status=status.HTTP_202_ACCEPTED)

    def run_data_processing(self):
        engine_file = os.path.join(os.getcwd(), "./data/EngineStatusMessages-844585.xml")
        location_file1 = os.path.join(os.getcwd(), "./data/LocationMessages-844585-page_1.xml")
        location_file2 = os.path.join(os.getcwd(), "./data/LocationMessages-844585-page_2.xml")
        caminos_file = os.path.join(os.getcwd(), "./data/CAMINOS_7336.shp")

        machine_serial = "844585"

        locations_times, engine_reports, lats, lons = parse(engine_file, location_file1, location_file2)
        caminos_processor = Caminos(caminos_file)

        for i in range(len(locations_times)):
            caminos_processor.distance_to_road(locations_times[i], engine_reports[i], lats[i], lons[i])

        for i, report in enumerate(caminos_processor.report_datetimes):

            data = {
                "machine_serial": machine_serial,
                "report_datetime": report,
                "engine_off_timestamp": caminos_processor.engine_off_timestamps[i],
                "lat": caminos_processor.lats[i],
                "lon": caminos_processor.lons[i],
                "is_safe": caminos_processor.is_saves[i],
                "distance_to_road_m": caminos_processor.distances_to_road_m[i],
                "is_active": True,
            }


            existing = InformeResguardo.objects.filter(
                machine_serial=data["machine_serial"],
                report_datetime=data["report_datetime"],
                engine_off_timestamp=data["engine_off_timestamp"]
            ).first()

            if existing:
                if not existing.is_active:
                    existing.is_active = True
                    existing.save()
                    print(f"Informe reactivado (id={existing.id}).")
                else:
                    print(f"Informe duplicado detectado (id={existing.id}). No se guarda.")
            else:
                InformeResguardo.objects.create(**data)
                print("Informe guardado correctamente.")


class SafeguardReportListView(generics.ListAPIView):
    """
    GET /safeguard-reports/
    Devuelve la lista de informes de resguardo.
    """
    #queryset = InformeResguardo.objects.all().order_by('-report_datetime')
    queryset = InformeResguardo.objects.filter(is_active=True).order_by('-report_datetime')
    serializer_class = InformeResguardoSerializer

class SafeguardReportUpdateView(APIView):
    """
    PATCH /safeguard-reports/{id}/
    Permite actualizar el campo is_active (soft delete)
    """

    def patch(self, request, pk):
        try:
            report = InformeResguardo.objects.get(pk=pk)
        except InformeResguardo.DoesNotExist:
            return Response({"error": "Report not found."}, status=status.HTTP_404_NOT_FOUND)

        # Solo permitir cambiar 'is_active'
        is_active = request.data.get("is_active")
        if is_active is None:
            return Response({"error": "Missing 'is_active' field."}, status=status.HTTP_400_BAD_REQUEST)

        report.is_active = is_active
        report.save()

        serializer = InformeResguardoSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)
