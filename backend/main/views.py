from django.contrib.gis.db.models.functions import Distance, Centroid
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
        min_distance = 300

        if nearest_school and nearest_school.distance.m > min_distance:
            result.append({
                'building': str(building),
                'nearest_school': str(nearest_school),
                'distance_to_school': nearest_school.distance.m
            })

        nearest_kindergarten = (
            Kindergarten.objects.annotate(centroid=Centroid('geometry'))
            .annotate(distance=Distance(building.centroid, 'centroid'))
            .order_by('distance')
            .first()
        )

        if nearest_kindergarten and nearest_kindergarten.distance.m > min_distance:
            result.append({
                'building': str(building),
                'nearest_kindergarten': str(nearest_kindergarten),
                'distance_to_kindergarten': nearest_kindergarten.distance.m
            })

    return JsonResponse(result, safe=False)

