COPY checkins FROM '/data-import/dataset_TIST2015_Checkins.txt' DELIMITER E'\t' CSV HEADER;
COPY pois FROM '/data-import/dataset_TIST2015_POIs.txt' DELIMITER E'\t' CSV HEADER;
COPY cities FROM '/data-import/dataset_TIST2015_Cities.txt' DELIMITER E'\t' CSV HEADER;
