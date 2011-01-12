ALTER TABLE meter ADD COLUMN slug varchar(50);
UPDATE meter SET slug = replace(lower(name),' ','-') ; 
