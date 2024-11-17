-- Table: public.stock

-- DROP TABLE IF EXISTS public.stock;

CREATE TABLE IF NOT EXISTS public.stock
(
    brand character varying COLLATE pg_catalog."default" NOT NULL,
    fno character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT stock_pkey PRIMARY KEY (brand, fno)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.stock
    OWNER to floss;