--ALTER TABLE meter ADD COLUMN slug varchar(50);
--UPDATE meter SET slug = replace(lower(name),' ','-') ; 

ALTER TABLE job_message ADD COLUMN text varchar(100);
