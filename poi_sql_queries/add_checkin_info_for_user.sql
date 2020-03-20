
SELECT AddGeometryColumn ('public','checkins','the_geom',4326,'POINT',2);

UPDATE checkins
SET the_geom = pois.the_geom, category_name = pois.category_name, country_code = pois.country_code
FROM pois
WHERE checkins.venue_id = pois.venue_id AND checkins.user_id = '170604'