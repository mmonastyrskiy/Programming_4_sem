--0

CREATE OR REPLACE FUNCTION place_restrictions_trigger_func() RETURNS trigger as $$
BEGIN
if (SELECT spaces_left-1 from "C21-703-7"."Shelf" where shelf_id =new.shelf_id) < 0 then
RAISE EXCEPTION 'Привышена емкость полки %', new.shelf_id;
else
if (pg_trigger_depth()=1) then
UPDATE "C21-703-7"."Shelf" set spaces_left = spaces_left-1 where shelf_id = new.shelf_id
end if;
END IF;


I




END;
$$ language plpgsql;
CREATE TRIGGER place_restrictions_trigger BEFORE INSERT OR UPDATE ON "C21-703-7"."Shelf" s  LEFT JOIN "C21-703-7"."product" p 
on(s.shelf_id = p.shelf_id)
FOR EACH ROW
EXECUTE PROCEDURE place_restrictions_trigger_func();



--1
CREATE OR REPLACE FUNCTION product_finder(client_n varchar(255),cdate date) RETURNS integer as $$
BEGIN
return SELECT count(product_id) from "C21-703-7"."product" p JOIN "C21-703-7"."Contract" c on(p.contract_id = c.contract_id)
 LEFT JOIN "C21-703-7"."Client" cl on (cl.client_id = c.client_id)
 where (client_name = client_n and expiration_date < cdate)
 END;
$$ language plpgsql;

--2

--3

--4
