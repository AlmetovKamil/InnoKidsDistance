from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection
from main.models import School, Kindergarten, ResidentialBuilding

class Command(BaseCommand):
    help = "Load buildings from PostGIS into Django models"

    def handle(self, *args, **options):
        self.load_buildings('school', School)
        self.load_buildings('kindergarten', Kindergarten)
        self.load_buildings('apartments', ResidentialBuilding)
        self.load_buildings('terrace', ResidentialBuilding)

    def load_buildings(self, table_name, model):
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT 
                    osm_id,
                    name,
                    ST_AsText(way) AS geometry
                    FROM planet_osm_polygon 
                WHERE building = '{table_name}' OR 
                    amenity = '{table_name}' OR 
                    tags -> 'education' = '{table_name}';
            """)
            rows = cursor.fetchall()

        buildings = []
        for osm_id, name, geometry in rows:
            buildings.append(
                model(
                    osm_id=osm_id,
                    name=name,
                    geometry=GEOSGeometry(geometry, srid=4326),
                )
            )
        model.objects.bulk_create(buildings, ignore_conflicts=True)
        self.stdout.write(
            self.style.SUCCESS(f"Imported {len(buildings)} buildings")
        )

