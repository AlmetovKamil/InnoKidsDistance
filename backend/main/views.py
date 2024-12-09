from django.shortcuts import render

# Create your views here.

from django.contrib.gis.db.models.functions import Distance, Centroid
from django.contrib.gis.geos import Point
from django.http import JsonResponse
from .models import ResidentialBuilding, School, Kindergarten

def building_distances(request):
    buildings = ResidentialBuilding.objects.annotate(centroid=Centroid('geometry'))
    
    result = []

    for building in buildings:
        nearest_school = (
            School.objects.annotate(centroid=Centroid('geometry'))
            .annotate(distance=Distance(building.centroid, 'centroid'))
            .order_by('distance')
            .first()
        )

        if nearest_school and nearest_school.distance.m > 0:
            result.append({
                'building': building.name,
                'nearest_school': nearest_school.name,
                'distance_to_school': nearest_school.distance.m
            })

        # Find the nearest kindergarten
        nearest_kindergarten = (
            Kindergarten.objects.annotate(centroid=Centroid('geometry'))
            .annotate(distance=Distance(building.centroid, 'centroid'))
            .order_by('distance')
            .first()
        )

        if nearest_kindergarten and nearest_kindergarten.distance.m > 0:
            result.append({
                'building': building.name,
                'nearest_kindergarten': nearest_kindergarten.name,
                'distance_to_kindergarten': nearest_kindergarten.distance.m
            })

    return JsonResponse(result, safe=False)

