
# Project Name: Proximity Checker for Schools and Kindergartens
This project evaluates the proximity of residential buildings to schools and kindergartens in the city of Innopolis. It identifies cases where walking distances exceed 500 meters, helping urban planners ensure accessibility to essential educational facilities.

## Features
- Imports OpenStreetMap (OSM) data into a PostGIS database using osm2pgsql.
- Filters and processes data for residential buildings, schools, and kindergartens within Innopolis.
- Calculates proximity based on Euclidean distance (500 meters radius).
- Provides an API endpoint to return non-compliant building-school/kindergarten pairs in JSON format.

## Tech Stack
- Backend Framework: Python with Django and Django Rest Framework
- Database: PostgreSQL with PostGIS
- OSM Data Processing: osm2pgsql
- Geospatial Libraries: GeoDjango, GDAL, GeoPandas

## How It Works
1. OSM data is downloaded in .pbf format and imported into PostGIS.
2. The data is processed to extract relevant objects (residential buildings, schools, kindergartens).
3. An API endpoint evaluates the proximity between buildings and educational facilities.
4. Results are returned as JSON with distances exceeding the 500-meter threshold.

## Future Enhancements
- Use routing algorithms to calculate real walking distances via the road network.
- Enable real-time querying of newly added or updated OSM data.

# Run the project

## Prerequisites

- Docker Desctop installed

## Steps

1. Create .env and copy all variables from .env.example
2. Run `docker compose up postgres -d`
3. Run `docker compose build api`
4. Run `docker compose up api --watch`
5. Run (in another terminal) `docker compose exec -it api python manage.py migrate`

# How the project was implemented

- Download OSM data from ...
- Set up PostgreSQL with PostGIS database
- Set up base Django app
- Set up docker compose

---

1. hstore extenstion should be created:

```sql
CREATE EXTENSION IF NOT EXISTS hstore;
```

2. download https://download.geofabrik.de/russia/volga-fed-district-latest.osm.pbf 

3. Extract innopolis from Volga federal descrict:

Innopolis boundaries: https://www.openstreetmap.org/relation/5273126

Get boundaries:
```bash
osmium getid -r -t volga-fed-district-latest.osm.pbf r5273126 -o innopolis-boundary.osm.pbf 
```
Extract innopolis:

```bash
osmium extract  -p innopolis-boundary.osm.pbf volga-fed-district-latest.osm.pbf -o innopolis.osm.pbf
```
Import to postgres:
```bash
PGPASSWORD=postgres osm2pgsql -d innokidsdistance -U postgres -H localhost -P 5432 --slim --create --hstore --latlong ~/innopolis.osm.pbf
```


`docker compose exec -it api chown -R inno:inno /app`
