from django.db import models
from django.contrib.gis.db import models as gis_models


class Building(models.Model):
    osm_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    geometry = gis_models.PolygonField()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.osm_id}: {self.name if self.name else ''}"


class ResidentialBuilding(Building):
    pass


class School(Building):
    pass


class Kindergarten(Building):
    pass
