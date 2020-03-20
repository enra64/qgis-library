-- Table: public.checkins

-- DROP TABLE public.checkins;

CREATE TABLE public.checkins
(
    user_id character varying COLLATE pg_catalog."default",
    venue_id character varying COLLATE pg_catalog."default",
    "timestamp" timestamp without time zone,
    "offset" integer
)

TABLESPACE pg_default;

ALTER TABLE public.checkins
    OWNER to "user";
-- Index: uid checkins

-- DROP INDEX public."uid checkins";

CREATE INDEX "uid checkins"
    ON public.checkins USING btree
    (user_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: vid

-- DROP INDEX public.vid;

CREATE INDEX vid
    ON public.checkins USING btree
    (venue_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;