import os
import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime
from django.conf import settings


def combine_files(file1, file2):

    with open(file1, 'r', encoding='utf-8') as f1:
         content1 = f1.read()
    with open(file2, 'r', encoding='utf-8') as f2:
         content2 = f2.read()
    content_all = content1 +  content2
    return content_all

def parse(engine_file, location_file1, location_file2):

    engine_times = []
    engine_reports = []
    engine_statuses = []
    locations_times = []
    lats = []
    lons = []
    
    with open(engine_file, 'r') as f:
        for line in f:
            if line.startswith("    <EngineStatus datetime="):
                l = line.strip().split()
                datetime_str = l[1].strip("datetime=>\"")
                dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            if line.startswith("        <Running>"):
                l = line.strip().split()
                status = l[0].strip("<Running></")
                engine_times.append(dt)
                engine_statuses.append(status)

    previous_lt = None
    previous_et = None
    previous_lat = None
    previous_lon = None

    combined_content = combine_files(location_file1,location_file2)
    lines = combined_content.splitlines()

    for line in lines:
        if line.startswith("    <Location datetime="):
            l = line.strip().split()
            last = l[1].strip("datetime=>\"")

    last_time = datetime.fromisoformat(last.replace('Z', '+00:00'))

    
    for line_num, line in enumerate(lines):
        if line.startswith("    <Location datetime="):
            l = line.strip().split()
            location_time = l[1].strip("datetime=>\"")
            lt = datetime.fromisoformat(location_time.replace('Z', '+00:00'))
            sw = 0
            latitude = lines[line_num + 1].strip().split()[0]
            lat = latitude.strip("<Latitude>\"</")
            longitude = lines[line_num + 2].strip().split()[0]
            lon = longitude.strip("<Longitude>\"</")
            if previous_lt == None:
                previous_lt = lt
            for i, et in enumerate(engine_times):

                if previous_et == None:
                    previous_et = et
                if engine_statuses[i] == "false" and sw == 0:
                    if lt >= et and et > previous_et :
                        sw = 1
                        previous_et = et
                        
                        if previous_lt.hour < 8 or (previous_lt.hour == 8 and previous_lt.minute < 30) or previous_lt.hour >= 20 or (previous_lt.hour == 19 and previous_lt.minute > 30):
                            locations_times.append(previous_lt)
                            engine_reports.append(et)
                            lats.append(previous_lat)
                            lons.append(previous_lon)


                    elif et == engine_times[-1]  and et >= previous_lt :
                        if lt == last_time:
                            sw = 1
                            if lt.hour < 8 or (lt.hour == 8 and lt.minute < 30) or lt.hour >= 20 or (lt.hour == 19 and lt.minute > 30):
                                locations_times.append(lt)
                                engine_reports.append(et)
                                lats.append(lat)
                                lons.append(lon)
                    
            previous_lt = lt
            previous_lat = lat
            previous_lon = lon

    return locations_times, engine_reports, lats, lons

class Caminos:
    def __init__(self, caminos_file):
        self.caminos_gdf = gpd.read_file(caminos_file)
        self.report_datetimes = []
        self.engine_off_timestamps = []
        self.lats = []
        self.lons = []
        self.is_saves = []
        self.distances_to_road_m = []

    def distance_to_road(self, report_datetime, engine_off_timestamp, lat, lon):
        try:
            geo_point = Point(lon, lat)
            
            gdf_point_geo = gpd.GeoDataFrame(
                [{'geometry': geo_point}], 
                crs='EPSG:4326'
            )
            
            gdf_point_utm = gdf_point_geo.to_crs(self.caminos_gdf.crs)
            point_utm = gdf_point_utm.geometry.iloc[0]
            distances = self.caminos_gdf.distance(point_utm)
            min_distance = distances.min()
            allowed_distance=50

            if min_distance > allowed_distance:
                is_safe = True
            else:
                is_safe = False

            self.report_datetimes.append(report_datetime)
            self.engine_off_timestamps.append(engine_off_timestamp)
            self.lats.append(lat)
            self.lons.append(lon)
            self.is_saves.append(is_safe)
            self.distances_to_road_m.append(min_distance)

                
        except Exception as e:
            print(f"Error: {e}")


def main():

    engine_file = "EngineStatusMessages-844585.xml"
    location_file1 = "LocationMessages-844585-page_1.xml"
    location_file2 = "LocationMessages-844585-page_2.xml"

    #engine_file = os.path.join(settings.BASE_DIR, "data", "EngineStatusMessages-844585.xml")
    #location_file1 = os.path.join(settings.BASE_DIR, "data", "LocationMessages-844585-page_1.xml")
    #location_file2 = os.path.join(settings.BASE_DIR, "data", "LocationMessages-844585-page_2.xml")


    locations_times, engine_reports, lats, lons = parse(engine_file, location_file1, location_file2)


    machine_serial = "844585"
    caminos_file = "CAMINOS_7336.shp"
    #caminos_file = os.path.join(settings.BASE_DIR, "data", "CAMINOS_7336.shp")

    caminos_processor = Caminos(caminos_file)

    for i in range(len(locations_times)):
        caminos_processor.distance_to_road(locations_times[i], engine_reports[i], lats[i], lons[i])

    for i, report in enumerate(caminos_processor.report_datetimes):

        print(f"\nEntry {i+1}:")
        print(f"machine_serial: {machine_serial}")
        print(f"report_datetime: {type(report)}")
        print(f"engine_off_timestamp: {caminos_processor.engine_off_timestamps[i]}")
        print(f"lat: {caminos_processor.lats[i]}")
        print(f"lon: {caminos_processor.lons[i]}")
        print(f"is_safe: {caminos_processor.is_saves[i]}")
        print(f"distance_to_road_m: {caminos_processor.distances_to_road_m[i]}")


if __name__ == "__main__":
    main()
