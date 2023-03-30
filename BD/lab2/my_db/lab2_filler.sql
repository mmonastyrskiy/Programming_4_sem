-- Очищаем структуру БД
TRUNCATE "C21-703-7"."Client" CASCADE;
TRUNCATE "C21-703-7"."Contract" CASCADE;
TRUNCATE "C21-703-7"."Room" CASCADE;
TRUNCATE "C21-703-7"."Shelf" CASCADE;
TRUNCATE "C21-703-7"."product" CASCADE;

SET Datestyle to German;

INSERT INTO "C21-703-7"."Room" Values
(1,'Room1',50,50,20,60,18,32),
(2,'Room2',500,500,40,100,22,32),
(3,'Room3',50,50,20,60,18,32),
(10,'Garage1',10000,10000,40,100,22,32),
(4,'Room4',50,50,20,60,18,32),
(5,'Room5',500,500,40,100,22,32);
INSERT INTO "C21-703-7"."Shelf" Values
(1,1,10,10,500,400,300,500,500),
(2,1,50,50,500,400,400,600,600),
(3,2,40,40,500,500,500,500,500),
(4,3,40,40,500,500,500,500,500),
(5,4,5,5,500,500,500,40,40);

INSERT INTO "C21-703-7"."Client" Values(100,'PAO SBERBANK',
'Юридический адрес	117312, г. Москва, ул. Вавилова, д.19
БИК	044525225
ИНН	7707083893
КПП	773643001
ОКПО	57972160'),
(101,' Российская Государственная Библиотека',
' ИНН 7704097560, ОГРН 1037739390809, ОКПО 02175175'),
(102,'Мираторг', 'Наименование:	"Агропромышленный холдинг "Мираторг", ООО
Основной ОКВЭД:	Консультирование по вопросам коммерческой деятельности и управления
Страна:	РОССИЯ
Регион:	Московская область
ИНН:	7704669440
ОКПО или др.:	84054099
Данные госрегистрации:	№1077763208874 от 29.11.2007, Межрайонная инспекция ФНС N 46 по г. Москве
Юридический адрес:	142030, Московская обл, г. Домодедово, тер. Трио-Инвест-Ям (Центральный Мкр, стр. 3
Почтовый адрес:	142000, Московская обл., г. Домодедово, мкр Центральный, тер. Трио-Инвест-Ям, стр. 3'),
(103,'НИЯУ МИФИ', 'Федеральное государственное автономное учреждение
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

(104,'ОЗОН','Юридический адрес	123112, г. Москва, Пресненская наб., д. 10, эт. 41, Пом. I, комн. 6
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


INSERT INTO "C21-703-7"."Contract" Values(1,'25-03-24','26-03-23',100);
INSERT INTO "C21-703-7"."Contract" Values(2,'25-03-24','26-03-23',100);

INSERT INTO "C21-703-7"."Contract" Values(3,'29-03-24','30-03-23',101);
INSERT INTO "C21-703-7"."Contract" Values(4,'29-03-24','30-03-23',102);
INSERT INTO "C21-703-7"."Contract" Values(5,'29-03-24','30-03-23',103);
INSERT INTO "C21-703-7"."Contract" Values(6,'29-03-24','30-03-23',104);

INSERT INTO "C21-703-7"."product" Values(1,110,120,130,now(),1,60,30,20,50,5,2,10);
INSERT INTO "C21-703-7"."product" Values(2,300,300,300,now(),2,60,30,20,50,1,3,100);
INSERT INTO "C21-703-7"."product" Values(3,210,220,230,now(),3,80,50,40,70,2,1,37);
INSERT INTO "C21-703-7"."product" Values(4,70,50,30,now(),4,60,30,20,50,5,3,10);
INSERT INTO "C21-703-7"."product" Values(5,110,120,130,now(),5,60,30,20,50,5,6,70);

