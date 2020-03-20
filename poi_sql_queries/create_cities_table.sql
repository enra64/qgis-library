-- Table: public.cities

-- DROP TABLE public.cities;

CREATE TABLE public.cities
(
    city_name character varying COLLATE pg_catalog."default",
    latitude double precision,
    longitude double precision,
    country_code character varying COLLATE pg_catalog."default",
    country_name character varying COLLATE pg_catalog."default",
    city_type character varying COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE public.cities
    OWNER to "user";