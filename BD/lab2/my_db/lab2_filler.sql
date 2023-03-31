-- Очищаем структуру БД
TRUNCATE "C21-703-7"."Client" CASCADE;
TRUNCATE "C21-703-7"."Contract" CASCADE;
TRUNCATE "C21-703-7"."Room" CASCADE;
TRUNCATE "C21-703-7"."Shelf" CASCADE;
TRUNCATE "C21-703-7"."product" CASCADE;

SET Datestyle to German;
CREATE SEQUENCE room_generator INCREMENT BY 1 CACHE 10 START 1;
CREATE SEQUENCE shelf_generator INCREMENT BY 1 CACHE 10 START 1;
CREATE SEQUENCE client_generator INCREMENT BY 1 CACHE 10 START 100;
CREATE SEQUENCE contract_generator INCREMENT BY 1 CACHE 10 START 1;
CREATE SEQUENCE pid_generator INCREMENT BY 1 CACHE 10 START 1;

INSERT INTO "C21-703-7"."Room" Values
(nextval('room_generator'),'Room1',50,50,20,60,18,32),
(nextval('room_generator'),'Room2',500,500,40,100,22,32),
(nextval('room_generator'),'Room3',50,50,20,60,18,32),
(nextval('room_generator'),'Garage1',10000,10000,40,100,22,32),
(nextval('room_generator'),'Room4',50,50,20,60,18,32);

INSERT INTO "C21-703-7"."Shelf" Values
(nextval('shelf_generator'),(select id from "C21-703-7"."Room" where name ='Room1'),10,10,500,400,300,500,500),
(nextval('shelf_generator'),(select id from "C21-703-7"."Room" where name ='Room1'),50,50,500,400,400,600,600),
(nextval('shelf_generator'),(select id from "C21-703-7"."Room" where name ='Room2'),40,40,500,500,500,500,500),
(nextval('shelf_generator'),(select id from "C21-703-7"."Room" where name ='Room3'),40,40,500,500,500,500,500),
(nextval('shelf_generator'),(select id from "C21-703-7"."Room" where name ='Room4'),5,5,500,500,500,40,40);

INSERT INTO "C21-703-7"."Client" Values(nextval('client_generator'),'PAO SBERBANK',
'Юридический адрес	117312, г. Москва, ул. Вавилова, д.19
БИК	044525225
ИНН	7707083893
КПП	773643001
ОКПО	57972160'),
(nextval('client_generator'),' Российская Государственная Библиотека',
' ИНН 7704097560, ОГРН 1037739390809, ОКПО 02175175'),
(nextval('client_generator'),'Мираторг', 'Наименование:	"Агропромышленный холдинг "Мираторг", ООО
Основной ОКВЭД:	Консультирование по вопросам коммерческой деятельности и управления
Страна:	РОССИЯ
Регион:	Московская область
ИНН:	7704669440
ОКПО или др.:	84054099
Данные госрегистрации:	№1077763208874 от 29.11.2007, Межрайонная инспекция ФНС N 46 по г. Москве
Юридический адрес:	142030, Московская обл, г. Домодедово, тер. Трио-Инвест-Ям (Центральный Мкр, стр. 3
Почтовый адрес:	142000, Московская обл., г. Домодедово, мкр Центральный, тер. Трио-Инвест-Ям, стр. 3'),
(nextval('client_generator'),'НИЯУ МИФИ', 'Федеральное государственное автономное учреждение
Полное наименование:
Федеральное государственное автономное образовательное учреждение высшего образования «Национальный исследовательский ядерный университет «МИФИ»
Наименование без ОПФ:
Национальный исследовательский ядерный университет «МИФИ»
Сокращенное наименование:
НИЯУ МИФИ
Полное наименование на английском языке:
National Research Nuclear University MEPhI (Moscow Engineering Physics Institute)
Сокращенное наименование на английском языке:
MEPhI
Дата государственной регистрации образовательного учреждения:
23 ноября 1942
Адрес (место нахождения):
115409, г. Москва, Каширское шоссе, д. 31
Юридический адрес:
115409, г. Москва, Каширское шоссе, д. 31
ИНН:
7724068140
КПП:
772401001
 
Справочная:
+7 495 788-5699, +7 499 324-7777
Факс:
+7 499 324-2111
Адрес электронной почты:
info@mephi.ru'),

(nextval('client_generator'),'ОЗОН','Юридический адрес	123112, г. Москва, Пресненская наб., д. 10, эт. 41, Пом. I, комн. 6
Фактический адрес	123112, Москва, Пресненская наб., д. 10, блок С, комплекс «Башня на набережной»
№ ОГРН	1027739244741
ИНН	7704217370
КПП
(По месту постановки на учет в качестве крупного налогоплательщика)	997750001
КПП
(По месту регистрации)	770301001
Код по ОКПО	55185357
ОКВЭД	52.47.1, 45.21, 45.21.1., 51.12.23, 51.12.24, 51.18.22, 51.18.25, 51.47.34, 51.52.23, 51.70, 52.45.4, 52.48.2, 52.48.22, 52.50.1, 52.50.2, 52.61.1, 74.40, 74.84
ОКФС	23
ОКОПФ	65
Расчетный счет	40702810100002400756 в АО «Райффайзенбанк» г. Москва
Корреспондентский счет	30101810200000000700
БИК	044525700');



CREATE OR REPLACE FUNCTION slot_finder(ushelf_id integer) RETURNS integer as $$
BEGIN
CASE when (SELECT count(*) from "C21-703-7"."product" p where p.shelf_id = ushelf_id) > 0 then
RETURN (SELECT max(slot_id) + 1 FROM "C21-703-7"."product" p where p.shelf_id = ushelf_id);
else 
RETURN 1;
END CASE;
END;

$$ language plpgsql;



INSERT INTO "C21-703-7"."Contract" Values(nextval('contract_generator'),'25-03-24','26-03-23',(SELECT client_id FROM "C21-703-7"."Client" where name = 'PAO SBERBANK'));
INSERT INTO "C21-703-7"."Contract" Values(nextval('contract_generator'),'25-03-24','26-03-23',(SELECT client_id FROM "C21-703-7"."Client" where name = 'PAO SBERBANK'));

INSERT INTO "C21-703-7"."Contract" Values(nextval('contract_generator'),'29-03-24','30-03-23',(SELECT client_id FROM "C21-703-7"."Client" where name = 'ОЗОН'));
INSERT INTO "C21-703-7"."Contract" Values(nextval('contract_generator'),'29-03-24','30-03-23',(SELECT client_id FROM "C21-703-7"."Client" where name = 'НИЯУ МИФИ'));
INSERT INTO "C21-703-7"."Contract" Values(nextval('contract_generator'),'29-03-24','30-03-23',(SELECT client_id FROM "C21-703-7"."Client" where name = 'НИЯУ МИФИ'));
INSERT INTO "C21-703-7"."Contract" Values(nextval('contract_generator'),'29-03-24','30-03-23',(SELECT client_id FROM "C21-703-7"."Client" where name = 'Мираторг'));

INSERT INTO "C21-703-7"."product" Values(nextval('pid_generator'),110,120,130,now(),1,60,30,20,50,5,slot_finder(5),10);
INSERT INTO "C21-703-7"."product" Values(nextval('pid_generator'),300,300,300,now(),2,60,30,20,50,1,slot_finder(1),100);
INSERT INTO "C21-703-7"."product" Values(nextval('pid_generator'),210,220,230,now(),3,80,50,40,70,2,slot_finder(2),37);
INSERT INTO "C21-703-7"."product" Values(nextval('pid_generator'),70,50,30,now(),4,60,30,20,50,5,slot_finder(5),10);
INSERT INTO "C21-703-7"."product" Values(nextval('pid_generator'),110,120,130,now(),5,60,30,20,50,5,slot_finder(5),70);

