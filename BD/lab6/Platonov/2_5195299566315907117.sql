BEGIN;


--drop table public.cars;
--drop sequence cars_seq;
create sequence cars_seq start 1;
CREATE TABLE IF NOT EXISTS public.cars
(
    id integer,
    mark_id integer NOT NULL,
    class_id integer NOT NULL,
    gos_number character varying(9) NOT NULL check(length(gos_number)>=8),
    color_id integer NOT NULL,
    year numeric(4) NOT NULL check(year <= extract(YEAR FROM NOW()) and year >= 1886),
    PRIMARY KEY (id),
    CONSTRAINT uniq_15 UNIQUE (gos_number, year)
);
INSERT INTO public.cars VALUES
((select nextval('cars_seq')),2,2,'с234км198',3,2012),
((select nextval('cars_seq')),3,2,'э281вд28',2,2022),
((select nextval('cars_seq')),1,1,'н271ад77',3,2022),
((select nextval('cars_seq')),4,1,'у281пд542',1,2022),
((select nextval('cars_seq')),2,2,'ц403ва32',4,2019);
--select * from public.cars;
--



--
--drop table public.drivers;
--drop sequence drivers_seq;
create sequence drivers_seq start 1;
CREATE TABLE IF NOT EXISTS public.drivers
(
    id integer,
    last_name character varying NOT NULL,
    first_name character varying NOT NULL,
    second_name character varying,
    birthday date NOT NULL check(extract(YEAR FROM NOW())-date_part('year', birthday) >=18),
    inn numeric(10) NOT NULL check(inn >= 1000000000),
    pasport_series numeric(4) NOT NULL check(pasport_series >= 1000),
    pasport_num numeric(6) NOT NULL check(pasport_num >=100000),
    PRIMARY KEY (id),
    CONSTRAINT uniq_100 UNIQUE (pasport_series, pasport_num),
    CONSTRAINT uniq_2 UNIQUE (last_name, first_name, second_name, birthday, inn)
);
SET DATESTYLE TO German;
INSERT INTO public.drivers VALUES
((select nextval('drivers_seq')),'Муравенко','Павел','Владимирович','27.11.2003',1231231231,2323,343434),
((select nextval('drivers_seq')),'Иванов','Иван','Иванович','01.12.1992',2342342342,3434,454545),
((select nextval('drivers_seq')),'Петров','Петр','Петрович','01.10.2001',3454353453,4545,565656),
((select nextval('drivers_seq')),'Сидоров','Сидр',null,'15.03.1993',4564564564,5656,676767),
((select nextval('drivers_seq')),'Петров','Иван','Иванович','01.12.1992',6786786786,2323,898989);

--select * from public.drivers;
--



--
--drop table public.tariffs;
--drop sequence tariffs_seq;
create sequence tariffs_seq start 1;
CREATE TABLE IF NOT EXISTS public.tariffs
(
    id integer,
    name character varying NOT NULL,
    cost_id integer NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT uniq_16 UNIQUE (name, cost_id)
);
INSERT INTO public.tariffs VALUES
((select nextval('tariffs_seq')),'По Москве',1),
((select nextval('tariffs_seq')),'По Москве(ночной)',2),
((select nextval('tariffs_seq')),'За МКАД с ветерком',3),
((select nextval('tariffs_seq')),'За МКАД с ветерком(ночной)',4),
((select nextval('tariffs_seq')),'Далеко и надолго',5);
--select * from public.tariffs;
--



--
--drop table public.range;
--drop sequence range_seq;
create sequence range_seq start 1;
CREATE TABLE IF NOT EXISTS public.range
(
    id integer,
    name character varying NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT uniq_13 UNIQUE (name)
);
INSERT INTO public.range VALUES
((select nextval('range_seq')),'В пределах МКАД'),
((select nextval('range_seq')),'за МКАД'),
((select nextval('range_seq')),'Подмосковье');
--select * from public.range;
--




--
--drop table public.cost;
--drop sequence cost_seq;
create sequence cost_seq start 1;
CREATE TABLE IF NOT EXISTS public.cost
(
    id integer,
    range_id integer NOT NULL,
    day_set_id integer NOT NULL,
    price integer NOT NULL check(price >0),
    PRIMARY KEY (id),
    CONSTRAINT uniq_112 UNIQUE (range_id, day_set_id, price)
);
Insert into public.cost values
((select nextval('cost_seq')),1,1,10),
((select nextval('cost_seq')),1,2,12),
((select nextval('cost_seq')),2,1,15),
((select nextval('cost_seq')),2,2,20),
((select nextval('cost_seq')),3,1,16);
--select * from public.cost;
--




--
--drop table public.day_set;
--drop sequence day_set_seq;
create sequence day_set_seq start 1;
CREATE TABLE IF NOT EXISTS public.day_set
(
    id integer,
    value character varying(1) NOT NULL check(value = 'д' or value = 'н'),
    PRIMARY KEY (id),
    CONSTRAINT "Uniq_19291" UNIQUE (value)
);
Insert into public.day_set values
((select nextval('day_set_seq')),'д'),
((select nextval('day_set_seq')),'н');
--select * from public.day_set;
--



--
--drop table public.mark;
--drop sequence mark_seq;
create sequence mark_seq start 1;
CREATE TABLE IF NOT EXISTS public.mark
(
    id integer,
    name character varying NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT uniq_1 UNIQUE (name)
);
Insert into public.mark values
((select nextval('mark_seq')),'BMW'),
((select nextval('mark_seq')),'Skoda'),
((select nextval('mark_seq')),'Lada'),
((select nextval('mark_seq')),'Renault'),
((select nextval('mark_seq')),'hyundai');
--select * from public.mark;
--




--
--drop table public.color;
--drop sequence color_seq;
create sequence color_seq start 1;
CREATE TABLE IF NOT EXISTS public.color
(
    id integer,
    name character varying NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT uniq_12 UNIQUE (name)
);
Insert into public.color values
((select nextval('color_seq')),'Красный'),
((select nextval('color_seq')),'Белый'),
((select nextval('color_seq')),'Желтый'),
((select nextval('color_seq')),'Черный'),
((select nextval('color_seq')),'Серый');
--select * from public.color;
--




--drop table public.class;
--drop sequence class_seq;
create sequence class_seq start 1;
CREATE TABLE IF NOT EXISTS public.class
(
    id integer,
    name character varying NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT uniq_11 UNIQUE (name)
);
Insert into public.class values
((select nextval('class_seq')),'Эконом'),
((select nextval('class_seq')),'Бизнес');
--select * from public.class;
--






--
--drop table public.cars_drivers;
--drop sequence cars_drivers_seq;
create sequence cars_drivers_seq start 1;
CREATE TABLE IF NOT EXISTS public.cars_drivers
(
    id integer,
    id_driver integer NOT NULL,
    id_car integer NOT NULL,
    start_date date NOT NULL check(start_date <= current_date),
    end_date date,
    start_time time NOT NULL check(start_time <= current_time or start_date <= current_date),
    end_time time,
    PRIMARY KEY (id),
    CONSTRAINT uniq_1010 UNIQUE (id, start_time, start_date),
    CONSTRAINT uniq_1011 UNIQUE (id_driver, start_time, start_date)
);
SET DATESTYLE TO German;
Insert into public.cars_drivers values
((select nextval('cars_drivers_seq')),1,1,'22.03.2023',null ,'21:12:30',null),
((select nextval('cars_drivers_seq')),1,2,'21.03.2022','29.03.2023','14:22:40','20:12:55'),
((select nextval('cars_drivers_seq')),2,1,'22.02.2021','28.03.2023','09:10:00','10:10:00'),
((select nextval('cars_drivers_seq')),3,5,'22.03.2018','27.03.2023','22:12:00','16:22:10'),
((select nextval('cars_drivers_seq')),5,5,'23.03.2017',null,'10:10:10',null);
--select * from public.cars_drivers;
--



--
--drop table public.orders;
--drop sequence orders_seq;
create sequence orders_seq start 1;
CREATE TABLE IF NOT EXISTS public.orders
(
    id integer,
    id_tariff integer NOT NULL,
    id_drivers_cars integer NOT NULL,
    order_date date NOT NULL check(order_date <= current_date),
    order_time time NOT NULL check(order_date < current_date or order_time <= current_time),
    start_adress character varying NOT NULL,
    end_adress character varying NOT NULL,
    passengers integer NOT NULL check(passengers <= 4),
    distance integer NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT uniq_17 UNIQUE (id_drivers_cars, order_date, order_time, start_adress, end_adress, passengers, distance)
);
INSERT INTO public.orders VALUES
((select nextval('orders_seq')),1,3,'24.03.2023','20:00:00','Ул. Мира, д. 3, подъезд 4','Ул. Кошкина, д.11к1, подъезд 1',2,14),
((select nextval('orders_seq')),3,4,'24.03.2022','21:50:00','Ул. Пушкина, д. 3, подъезд 6','Ул. Колотушкина, д.110, подъезд 14',4,51),
((select nextval('orders_seq')),1,3,'25.02.2021','09:14:00','Ул. Ленинский проспект, д. 14, подъезд 1','Ул. Талнахская, д.35, подъезд 3',1,3),
((select nextval('orders_seq')),4,5,'25.03.2018','23:54:00','Ул. Каширское Шоссе, д. 142, подъезд 1','Ул. Москворечье, д.9, подъезд 11',4,32),
((select nextval('orders_seq')),1,4,'24.03.2017','20:00:00','Ул. Мира, д. 3, подъезд 4','Ул. Кошкина, д.11к1, подъезд 1',2,14);
--select * from public.orders;
--





--
--drop table public.payment;
--drop sequence payment_seq;
create sequence payment_seq start 1;
CREATE TABLE IF NOT EXISTS public.payment
(
    id integer,
    id_car integer NOT NULL,
    id_order integer NOT NULL,
    id_driver integer NOT NULL,
    miliage integer check(miliage >2),
    sum_cost integer check(sum_cost >0),
    CONSTRAINT test PRIMARY KEY (id),
    CONSTRAINT uniq_18 UNIQUE (id_order, miliage, sum_cost)
);
INSERT INTO public.payment VALUES
((select nextval('payment_seq')),1,1,2,24,1534),
((select nextval('payment_seq')),1,2,2,53,10000),
((select nextval('payment_seq')),1,4,2,24,12636),
((select nextval('payment_seq')),3,3,4,124,3291),
((select nextval('payment_seq')),5,5,1,51,2636);
--select *from public.payment;


ALTER TABLE IF EXISTS public.cars
    ADD FOREIGN KEY (color_id)
    REFERENCES public.color (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.cars
    ADD FOREIGN KEY (class_id)
    REFERENCES public.class (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.cars
    ADD FOREIGN KEY (mark_id)
    REFERENCES public.mark (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.tariffs
    ADD FOREIGN KEY (cost_id)
    REFERENCES public.cost (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.orders
    ADD FOREIGN KEY (id_tariff)
    REFERENCES public.tariffs (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.orders
    ADD FOREIGN KEY (id_drivers_cars)
    REFERENCES public.cars_drivers (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;
	
ALTER TABLE IF EXISTS public.payment
    ADD FOREIGN KEY (id_order)
    REFERENCES public.orders (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.cars_drivers
    ADD FOREIGN KEY (id_driver)
    REFERENCES public.drivers (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.cars_drivers
    ADD FOREIGN KEY (id_car)
    REFERENCES public.cars (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.cost
    ADD FOREIGN KEY (range_id)
    REFERENCES public.range (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.cost
    ADD FOREIGN KEY (day_set_id)
    REFERENCES public.day_set (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;



END;



--0
select drivers.last_name, drivers.first_name, drivers.second_name, drivers.inn, SUM(payment.sum_cost) as "Всего заработано"
from payment
join orders on payment.id_order=orders.id
join cars_drivers on orders.id_drivers_cars=cars_drivers.id
join drivers  on drivers.id=cars_drivers.id_driver
group by drivers.id
having SUM(payment.sum_cost) >= all(select SUM(payment.sum_cost) from payment
join orders on payment.id_order=orders.id
join cars_drivers on orders.id_drivers_cars=cars_drivers.id
join drivers  on drivers.id=cars_drivers.id_driver
group by drivers.id)
--



--1
select drivers.last_name, drivers.first_name, drivers.second_name, orders.order_date, orders.start_adress
from drivers 
join cars_drivers
on drivers.id = cars_drivers.id_driver
join orders
on cars_drivers.id = orders.id_drivers_cars
join tariffs 
on tariffs.id = orders.id_tariff
join cost
on cost.id = tariffs.cost_id
WHERE orders.order_date >= date_trunc('month', current_date - interval '1 month') AND orders.order_date < date_trunc('month', current_date);

select tariffs.id, tariffs.name, SUM(payment.sum_cost) as "Всего заработано"
from payment
join orders on payment.id_order=orders.id
join tariffs on tariffs.id=orders.id_tariff
join cost on cost.id=tariffs.cost_id
where orders.order_date between '01.01.2023' and '31.12.2023'
GROUP BY tariffs.id
ORDER BY "Всего заработано" desc
--

--2
select class.name, count(class.name) as "колво заказов за 2023"
from orders 
join cars_drivers 
on orders.id_drivers_cars = cars_drivers.id
join cars 
on cars_drivers.id_car = cars.id
join class
on cars.class_id = class.id
where orders.order_date between '01.01.2016' and '31.12.2023'
group by class.name;
--



--3
ALTER TABLE cars_drivers
DROP CONSTRAINT cars_drivers_id_car_fkey,
ADD CONSTRAINT cars_drivers_id_car_fkey FOREIGN KEY (id_car) REFERENCES cars(id)
ON DELETE CASCADE;

delete FROM cars WHERE
id NOT IN (SELECT DISTINCT id_car FROM cars_drivers WHERE cars_drivers.id
IN (SELECT DISTINCT id_drivers_cars FROM orders))
OR 
id NOT IN (SELECT DISTINCT id_car FROM cars_drivers);
--


--4
update cost
set price=price*1.1
where cost.id=(SELECT max(cost.id)
				FROM payment
				JOIN orders ON payment.id_order=orders.id
				JOIN tariffs ON tariffs.id=orders.id_tariff
				JOIN cost ON cost.id=tariffs.cost_id
				GROUP BY tariffs.id
				ORDER BY SUM(payment.sum_cost) DESC
				LIMIT 1);

--

--5
ALTER TABLE orders ADD COLUMN maybe_price INTEGER CHECK (maybe_price > 0);


--UPDATE orders
--SET maybe_price = (SELECT orders.distance * cost.price FROM orders 
--				   JOIN tariffs ON tariffs.id=orders.id_tariff
--				   JOIN cost ON cost.id=tariffs.cost_id
--				   WHERE orders.id_tariff = tariffs.id and tariffs.cost_id=cost.id)
--WHERE maybe_price IS NULL;
--

--6
ALTER TABLE orders
ADD CONSTRAINT check_distance
CHECK (distance >=2);
--
DROP TABLE orders CASCADE;


ALTER TABLE orders DROP COLUMN cost_id;
drop view orders_with_cost;
CREATE VIEW orders_with_cost AS
SELECT orders.id, orders.order_time, orders.start_adress,orders.end_adress, cost.price
FROM orders
JOIN tariffs ON orders.id_tariff = tariffs.id
JOIN cost ON tariffs.cost_id = cost.id;

select * from orders_with_cost;

select * from cost;
select * from orders;

Rollback;

UPDATE orders_with_cost SET price = 105 WHERE id = 12;

UPDATE orders 
SET id_tariff = (SELECT tariffs.id FROM tariffs JOIN cost ON tariffs.cost_id = cost.id WHERE cost.price = NEW.price) 
WHERE id = id AND id_tariff IS NOT NULL;
    
UPDATE orders_with_cost 
SET price = 99 
FROM orders 
JOIN tariffs ON orders.id_tariff = tariffs.id 
JOIN cost ON tariffs.cost_id = cost.id 
WHERE orders.id = 11;
ALTER TABLE orders ADD COLUMN price numeric;
    


CREATE OR REPLACE FUNCTION update_orders_with_cost() 
RETURNS TRIGGER AS 
$$
DECLARE
    order_id INTEGER;
BEGIN
    SELECT id INTO order_id FROM orders WHERE id = NEW.id;
    UPDATE cost SET price = NEW.price WHERE id = (SELECT cost_id FROM tariffs WHERE id = (SELECT id_tariff FROM orders WHERE id = order_id));
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER update_orders_with_cost_trigger 
INSTEAD OF UPDATE ON orders_with_cost
FOR EACH ROW 
EXECUTE FUNCTION update_orders_with_cost();
		
