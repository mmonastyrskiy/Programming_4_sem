--0

CREATE OR REPLACE FUNCTION place_restrictions_trigger_func() RETURNS trigger as $$
BEGIN
if ((SELECT spaces_left-1 from "C21-703-7"."Shelf" where shelf_id =new.shelf_id) < 0) then
RAISE EXCEPTION 'Привышена емкость полки %', new.shelf_id;
else
if (pg_trigger_depth()=1) then
UPDATE "C21-703-7"."Shelf" set spaces_left = spaces_left-1 where shelf_id = new.shelf_id
end if;
END IF;
if((sum(weight) FROM "C21-703-7"."Shelf" s LEFT JOIN "C21-703-7"."product" p) > max_weight) then
RAISE EXCEPTION 'Привышен максимальный вес %', new.shelf_id;

I

END;
$$ language plpgsql;
CREATE TRIGGER place_restrictions_trigger BEFORE INSERT OR UPDATE ON ("C21-703-7"."Shelf" s  LEFT JOIN "C21-703-7"."product" p )
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
CREATE OR REPLACE FUNCTION max_parameters_step(numeric[], numeric[]) RETURNS numeric[] AS $$
DECLARE
res numeric[];
BEGIN
IF $1[1] > $2[1] THEN
res[1] := $1[1];
ELSE
res[1] := $2[1];
END IF;
IF $1[2] > $2[2] THEN
res[2] := $1[2];
ELSE
res[2] := $2[2];
END IF;
IF $1[3] > $2[3] THEN
res[3] := $1[3];
ELSE
res[3] := $2[3];
END IF;
RETURN res;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION max_parameters_final(numeric[]) RETURNS text AS $$
SELECT (to_char($1[1],'99999999D999') || 'x' || to_char($1[2],'99999999D999') ||
'x' ||to_char($1[3],'9999999999D999'));
$$ LANGUAGE sql;

CREATE OR REPLACE AGGREGATE maxpam(numeric[]) (
sfunc = max_parameters_step,
stype = numeric[],
initcond = '{0, 0, 0}',
finalfunc = max_parameters_final
);

select maxpam(ARRAY[p.height,p.width,p.length]) FROM public."product" p


--3


CREATE VIEW client_product_view AS
SELECT c.name AS client_name, p.product_id, p.width, p.height, p.length, p.unpacking_date, p.shelf_id, p.slot_id, p.weight
FROM "C21-703-7"."Client" c
INNER JOIN "C21-703-7"."Contract" ct ON c.client_id = ct.client_id
INNER JOIN "C21-703-7"."Product" p ON ct.contract_id = p.contract_id;

--4
CREATE FUNCTION init()
RETURNS VOID
AS $$
BEGIN
DROP TABLE queue;
    CREATE TABLE queue (
                id SERIAL PRIMARY KEY,
                data VARCHAR(64) NOT NULL,
                inserted_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION enqueue(new_data VARCHAR(64))
RETURNS VOID
AS
$$
BEGIN
    INSERT INTO queue (data) VALUES (new_data);
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION dequeue()
RETURNS VOID
AS
$$
BEGIN
    DELETE FROM queue WHERE id = (SELECT max(id) FROM queue);
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION empty()
RETURNS VOID
AS
$$
BEGIN
    DELETE FROM queue;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION top()
RETURNS VARCHAR(64)
AS
$$
BEGIN
    RETURN (SELECT data FROM queue ORDER BY id LIMIT 1);
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION tail()
RETURNS VARCHAR(64)
AS
$$
BEGIN
    RETURN (SELECT data FROM queue ORDER BY id ASC LIMIT 1);
END;
$$
LANGUAGE plpgsql;


--test


select init();
select init();
select enqueue('Mathematics');
select enqueue('Physics');
select enqueue('English');
select enqueue('Biology');
select enqueue('Social studies');
select * from queue;
select dequeue();
select top();
select tail();
select dequeue();select dequeue();select dequeue();select dequeue();select dequeue();select dequeue();

