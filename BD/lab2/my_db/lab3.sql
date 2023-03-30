--0
SELECT sum(weight) from "C21-703-7"."product";
--1
SELECT sum(width*height*length) from "C21-703-7"."product" p GROUP BY (SELECT client_id from "C21-703-7"."Contract" c where c.contract_id = p.contract_id) ORDER BY sum(weight) DESC LIMIT 3;
--2
SELECT DISTINCT count(shelf_id,slot_id) from "C21-703-7"."product" p;
--3
delete 
--4
--5
--6