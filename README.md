
# Proximity Checker for Schools and Kindergartens
This project evaluates the proximity of residential buildings to schools and kindergartens in the city of Innopolis. It identifies cases where walking distances exceed 500 meters, helping urban planners ensure accessibility to essential educational facilities.

## Features
- Imports OpenStreetMap (OSM) data into a PostGIS database using osm2pgsql.
- Filters and processes data for residential buildings, schools, and kindergartens within Innopolis.
- Calculates distance between residential buildings and schools/kindergardens (minimal distance between their centroids).
- Provides an API endpoint to return building<->school/kindergarten pairs that are at least 500 meters apart from each other in JSON format.

## Tech Stack
- Backend Framework: Python with Django and Django Rest Framework
- Database: PostgreSQL with PostGIS
- OSM Data Processing: osm2pgsql, osmium
- Geospatial Libraries: GeoDjango

## How It Works
1. OSM data is downloaded in .pbf format and imported into PostGIS.
2. The data is processed to extract relevant objects (residential buildings, schools, kindergartens).
3. An API endpoint evaluates the distance between buildings and educational facilities.
4. Results are returned as JSON with distances exceeding the 500-meter threshold.

## Future Enhancements
- Automate filling the database with OSM data
- Use routing algorithms to calculate real walking distances via the road network.

# Run the project

## Prerequisites

- Docker Desktop installed
- `osmium` installed
- `osm2pgsql` installed

## Steps

1. Create .env and copy all variables from .env.example
2. Run `docker compose build`
3. Run `docker compose up`
4. Import OSM data to the database (see below for more information)
5. Run `docker compose exec -it api python manage.py migrate`
6. Fill the django models with OSM data:
    ```bash
    docker compose exec -it api python manage.py load_buildings
    ```
7. The endpoint is available at http://localhost:8000/building-distances/

## Import OSM data to the database

1. Download https://download.geofabrik.de/russia/volga-fed-district-latest.osm.pbf 

2. Extract Innopolis from Volga federal descrict using the city's boundaries:

    - Innopolis boundaries: https://www.openstreetmap.org/relation/5273126

    - Get boundaries:
    ```bash
    osmium getid -r -t volga-fed-district-latest.osm.pbf r5273126 -o innopolis-boundary.osm.pbf 
    ```

    - Extract innopolis:
    ```bash
    osmium extract  -p innopolis-boundary.osm.pbf volga-fed-district-latest.osm.pbf -o innopolis.osm.pbf
    ```

3. Import to postgres:
```bash
PGPASSWORD=postgres osm2pgsql -d innokidsdistance -U postgres -H localhost -P 5432 --slim --create --hstore --latlong ~/innopolis.osm.pbf
```

# P.S.

- The minimum distance can be set by enviroment variable `MIN_DISTANCE` (default 500). If it's 500, there are no such
building<->school/kindergarten pairs.

- I don't check is the buildings are inside the administrative boundaries of Innopolis because I import
only items that are inside the borders. But it's better to add this check to generalize the solution.
