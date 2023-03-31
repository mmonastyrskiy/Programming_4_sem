--0
SELECT sum(weight) from "C21-703-7"."product";
--1
SELECT sum(width*height*length) from "C21-703-7"."product" p GROUP BY (SELECT client_id from "C21-703-7"."Contract" c where c.contract_id = p.contract_id) ORDER BY sum(weight) DESC LIMIT 3;
--2
SELECT DISTINCT count(shelf_id,slot_id) from "C21-703-7"."product" p; --WTF
--3
delete from "C21-703-7"."product" p where (SELECT max_weight from "C21-703-7"."Shelf" s where s.shelf_id = p.shelf_id) < 100;
--4
update "C21-703-7"."Contract" set expiration_date = expiration_date + interval '1 month' where client_id = 100;
--5
alter table "C21-703-7"."product" add column if not exists is_fragile char NOT NULL;
--6
alter table "C21-703-7"."product" add constraint max_weight_check (max_weight <= 500);
validate constraint max_weight_check;
