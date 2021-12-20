CREATE SCHEMA bank;
SET search_path TO bank,public;
CREATE TABLE bank.holding (
    holding_id int,
    user_id int,
    holding_stock varchar(8),
    holding_quantity int,
    datetime_created timestamp,
    datetime_updated timestamp,
    primary key(holding_id)
);
ALTER TABLE bank.holding replica identity FULL;
insert into bank.holding values (1000, 1, 'VFIAX', 10, now(), now());