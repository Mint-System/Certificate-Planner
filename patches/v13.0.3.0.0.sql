-- Add id field to BoM Part Relation.
CREATE SEQUENCE public.certificate_planer_bom_certificate_planer_part_rel_id_seq INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;
ALTER SEQUENCE public.certificate_planer_bom_certificate_planer_part_rel_id_seq OWNER TO odoo;
ALTER TABLE public.certificate_planer_bom_certificate_planer_part_rel
ADD COLUMN id integer NOT NULL DEFAULT nextval(
        'certificate_planer_bom_certificate_planer_part_rel_id_seq'::regclass
    );
SELECT setval(
        'certificate_planer_bom_certificate_planer_part_rel_id_seq',
        12000,
        true
    );
-- Create custom sequence for BoM Prerequisite Relation.
CREATE SEQUENCE public.certificate_planer_bom_certificate_planer_prerequisite_rel_id_seq INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;
ALTER SEQUENCE public.certificate_planer_bom_certificate_planer_prerequisite_rel_id_seq OWNER TO odoo;
