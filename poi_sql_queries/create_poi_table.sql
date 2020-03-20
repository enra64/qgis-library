-- Table: public.pois

-- DROP TABLE public.pois;

CREATE TABLE public.pois
(
    venue_id character varying COLLATE pg_catalog."default",
    latitude double precision,
    longitude double precision,
    category_name character varying COLLATE pg_catalog."default",
    country_code character varying COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE public.pois
    OWNER to "user";
-- Index: pois venue id

-- DROP INDEX public."pois venue id";

CREATE INDEX "pois venue id"
    ON public.pois USING btree
    (venue_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;