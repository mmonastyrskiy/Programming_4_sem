-- Очищаем структуру БД
TRUNCATE "C21-703-7"."Client" CASCADE;
TRUNCATE "C21-703-7"."Contract" CASCADE;
TRUNCATE "C21-703-7"."Room" CASCADE;
TRUNCATE "C21-703-7"."Shelf" CASCADE;
TRUNCATE "C21-703-7"."product" CASCADE;


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
+7 499 324-2111'),

();

INSERT INTO "C21-703-7"."Contract" Values(1,'26-03-23','25-03-24',100);
INSERT INTO "C21-703-7"."Contract" Values(2,'26-03-23','25-03-24',100);


