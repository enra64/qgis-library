UPDATE pois SET the_geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);
UPDATE cities SET the_geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);