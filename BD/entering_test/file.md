# Вариант 1
## Задание 1
```sql
CREATE TABLE people(
id integer PRIMARY KEY,
last_name varchar(32) NOT NULL,
first_name varchar(32) NOT NULL,
second_name varchar(32),
sex char NOT NULL,
birthday date,
death_date date,
mother_id integer references people(id),
father_id integer references people(id),
CHECK (sex in ('м','ж'))
);
```
## Задание 2
```sql
CREATE SEQUENCE people_id_seq START WITH 1 INCREMENT BY 1 CACHE 10;
SET DATESTYLE TO German;
INSERT INTO people VALUES
(nextval('people_id_seq'),'Романов', 'Николай','Павлович','м','17.07.1796','14.03.1855',null,null),
(nextval('people_id_seq'),'Романова', 'Александра','Федоровна','ж','13.07.1798','01.11.1860',null,null),
(nextval('people_id_seq'),'Романов', 'Александр','Николаевич','м','29.04.1818','13.03.1881',2,1),
(nextval('people_id_seq'),'Романова', 'Мария','Александровна','ж','08.08.1824','03.06.1880',null,null),
(nextval('people_id_seq'),'Романов', 'Александр','Александрович','м','10.03.1845','01.11.1894',4,3)
returning *;
```
## Задание 3
```sql
SELECT s.first_name, s.last_name, s.second_name, 
f.first_name, f.last_name, f.second_name,m.first_name, m.last_name, m.second_name
FROM people s join people m on (s.mother_id = m.id) join people f on (s.father_id = f.id)
```
## Задание 4
```sql
update people set birthday = birthday - interval '12 years',death_date = death_date - interval '12 years'
	returning *;
```
## Задание 5
```sql
SET DATESTYLE TO German;
CREATE OR REPLACE PROCEDURE long_livers(age integer) as $$
DECLARE
attr_e record;
a integer;
BEGIN
a:=0;
FOR attr_e in (SELECT * FROM people where extract(year from age(death_date,birthday)) > age)
LOOP
raise info '% % % ',attr_e.first_name,attr_e.last_name,attr_e.second_name;
a := a+1;
END LOOP;
raise info '%',a;
raise info '%', (SELECT max(extract(year from age(death_date,birthday))) from people);
raise info '%', (SELECT min(extract(year from age(death_date,birthday))) from people);
raise info '%', (SELECT avg(extract(year from age(death_date,birthday))) from people);
END
$$
LANGUAGE plpgsql;
call long_livers(50);
```
## Задание 6
```sql
with recursive length(id,father_id) AS (
SELECT id,father_id from people where id =1
union all
SELECT people.id,people.father_id from people join length l on l.id = people.father_id
)
SELECT count(*) FROM length

```