CREATE TABLE holding (
    holding_id int,
    user_id int,
    holding_stock varchar(8),
    holding_quantity int,
    datetime_created timestamp,
    datetime_updated timestamp,
    primary key(holding_id)
);

ALTER TABLE holding replica identity FULL;
INSERT INTO holding VALUES (1000, 1, 'VFIAX', 10, now(), now());