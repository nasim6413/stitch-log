-- Table: public.dmc_to_anchor

-- DROP TABLE IF EXISTS public.dmc_to_anchor;

CREATE TABLE IF NOT EXISTS public.dmc_to_anchor
(
    dmc character varying(5) COLLATE pg_catalog."default" NOT NULL,
    anchor character varying(5) COLLATE pg_catalog."default" NOT NULL,
    hex character varying COLLATE pg_catalog."default",
    fname character varying COLLATE pg_catalog."default",
    CONSTRAINT dmc_to_anchor_pkey PRIMARY KEY (dmc, anchor)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.dmc_to_anchor
    OWNER to floss;