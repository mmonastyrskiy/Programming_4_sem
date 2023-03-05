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
FROM people s left join people m on (s.mother_id = m.id) left join people f on (s.father_id = f.id)
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

# Вариант 2
## Задание 1
```sql
create table staff(
id integer primary key,
last_name varchar(64) not null,
first_name varchar(64) not null,
second_name varchar(64),
sex char check(sex='f' or sex='m'),
birthday date not null,
post varchar(128) not null,
department varchar(128) not null,
head_id integer references staff(id),
CONSTRAINT post_department_unique UNIQUE (post, department)
);
```
## Задание 2
```sql
CREATE SEQUENCE staff_id_seq INCREMENT BY -1 CACHE 100 NO MINVALUE;
INSERT INTO staff VALUES
(nextval('staff_id_seq'), 'Сталин','Иосиф','Виссарионович','м', to_date('21.12.1879','DD.MM.YYYY'),'Председатель','ГКО', null),
(nextval('staff_id_seq'), 'Молотов','Вячеслав','Михайлович','м', to_date('09.03.1890', 'DD.MM.YYYY'), 'Заместитель председателя', 'ГКО', 1),
(nextval('staff_id_seq'), 'Маленков','Георгий','Максимилианович','м', to_date('08.01.1902', 'DD.MM.YYYY'), 'Начальник', 'УК ЦК ВКП(б)', 2),
(nextval('staff_id_seq'), 'Ворошилов','Климент','Ефремович','м', to_date('04.02.1881', 'DD.MM.YYYY'), 'Председатель КО', 'СНК', 2),
(nextval('staff_id_seq'), 'Микоян','Анастас','Иванович','м', to_date('25.11.1895', 'DD.MM.YYYY'), 'Председатель', 'КП-ВС РККА', 2) returning *;

```
## Задание 3
```sql
select t1.last_name, t1.first_name, t1.second_name, t1.post, t2.last_name as hLast_name, t2.first_name as hFirstName, t2.second_name as hSecond_name
from staff t1 left join staff t2 on (t1.head_id=t2.id);
```
## Задание 4
```sql
update STAFF set STAFF.id = STAFF.id-2 where STAFF.head_id IS NULL returning *;
```
## Задание 5
```sql
CREATE OR REPLACE PROCEDURE birthday_boys(month integer) as $$
DECLARE
attr_e record;
a integer;
BEGIN
a:=0;
FOR attr_e in (SELECT * FROM people where extract(month from birthday) = month)
LOOP
raise info '% % % ',attr_e.last_name,attr_e.first_name,attr_e.second_name;
a := a+1;
END LOOP;
raise info '%',a;
raise info '%', (SELECT max(extract(year from age(NOW(),birthday))) from staff where extract(month from birthday) = month);
raise info '%', (SELECT min(extract(year from age(NOW(),birthday))) from staff  where extract(month from birthday) = month);
raise info '%', (SELECT round(avg(extract(year from age(NOW(),birthday))),2) from staff  where extract(month from birthday) = month);
END
$$
LANGUAGE plpgsql;
call birthday_boys(3);
```
## Задание 6
```sql
WITH RECURSIVE subordinates AS (
SELECT id, head_id, 1 AS chain_length
FROM staff
WHERE head_id IS NOT NULL
UNION ALL
SELECT s.id, s.head_id, chain_length + 1
FROM staff s
JOIN subordinates sub ON s.head_id = sub.id
)
SELECT MAX(chain_length)
FROM subordinates;
```

# Вариант 3
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
```
## Задание 2
```sql
CREATE SEQUENCE people_id_seq START WITH 5 INCREMENT BY -1 CACHE 10 NO minvalue maxvalue 5;
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
SELECT s.first_name, s.last_name,s.second_name,p.first_name,p.last_name,p.second_name from people s left join people p where(s.sex = 'м' and s.father_id = p.id)
```
## Задание 4
```sql
update people set birthday = birthday - interval '3 month',death_date = death_date - interval '3 month'
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
with recursive length(id,mother_id) AS (
SELECT id,mother_id from people where id =2
union all
SELECT people.id,people.mother_id from people join length l on l.id = people.mother_id
)
SELECT count(*) FROM length
```


# Вариант 4
## Задание 1
```sql

create table staff(
id integer not null primary key,
last_name varchar(64) not null,
first_name varchar(64)not null,
second_name varchar(64),
sex char not null check(sex = 'м' or sex = 'ж'),
birthday date not null,
post varchar(128) not null,
department varchar(128) not null,
unique(post, department),
head_id integer references staff(id)
);
```
## Задание 2
```sql
drop sequence staff_id_seq;
CREATE SEQUENCE staff_id_seq INCREMENT BY 1;
INSERT INTO staff VALUES
(nextval('staff_id_seq'), 'Сталин','Иосиф','Виссарионович','м', to_date('21.12.1879','DD.MM.YYYY'),'Председатель','ГКО', null),
(nextval('staff_id_seq'), 'Молотов','Вячеслав','Михайлович','м', to_date('09.03.1890', 'DD.MM.YYYY'), 'Заместитель председателя', 'ГКО', 1),
(nextval('staff_id_seq'), 'Маленков','Георгий','Максимилианович','м', to_date('08.01.1902', 'DD.MM.YYYY'), 'Начальник', 'УК ЦК ВКП(б)', 2),
(nextval('staff_id_seq'), 'Ворошилов','Климент','Ефремович','м', to_date('04.02.1881', 'DD.MM.YYYY'), 'Председатель КО', 'СНК', 2),
(nextval('staff_id_seq'), 'Микоян','Анастас','Иванович','м', to_date('25.11.1895', 'DD.MM.YYYY'), 'Председатель', 'КП-ВС РККА', 2) returning *;
```
## Задание 3
```sql
select s1.last_name, s1.first_name, s1.second_name, s2.last_name, s2.first_name, s2.second_name,s2.post from staff s1 left join staff s2 on s1.id = s2.head_id;
```
## Задание 5
```sql
CREATE OR REPLACE PROCEDURE birthday_boys(month integer) as $$
DECLARE
attr_e record;
a integer;
BEGIN
a:=0;
FOR attr_e in (SELECT * FROM people where extract(month from birthday) = month)
LOOP
raise info '% % % ',attr_e.last_name,attr_e.first_name,attr_e.second_name;
a := a+1;
END LOOP;
raise info '%',a;
raise info '%', (SELECT max(extract(year from age(NOW(),birthday))) from staff where extract(month from birthday) = month);
raise info '%', (SELECT min(extract(year from age(NOW(),birthday))) from staff  where extract(month from birthday) = month);
raise info '%', (SELECT round(avg(extract(year from age(NOW(),birthday))),2) from staff  where extract(month from birthday) = month);
END
$$
LANGUAGE plpgsql;
call birthday_boys(3);
```
## Задание 6
```sql
WITH RECURSIVE rstaff(id, head_id, len) AS(
  SELECT id, head_id, 1 
    FROM staff
    WHERE head_id is null
  UNION ALL
  SELECT staff.id, staff.head_id, rstaff.len + 1
    FROM rstaff
    JOIN staff ON rstaff.id=staff.head_id
)  
SELECT max(len) FROM rstaff;
```