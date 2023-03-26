-- Очищаем структуру БД
TRUNCATE "C21-703-7"."Client" CASCADE;
TRUNCATE "C21-703-7"."Contract" CASCADE;
TRUNCATE "C21-703-7"."Room" CASCADE;
TRUNCATE "C21-703-7"."Shelf" CASCADE;
TRUNCATE "C21-703-7"."product" CASCADE;


INSERT INTO "C21-703-7"."Room" Values(1,'Room1',50,50,20,60,18,32),(2,'Room2',500,500,40,100,22,32);
INSERT INTO "C21-703-7"."Shelf" Values(1,1,10,10,500,400,300,500,500),(2,1,50,50,500,400,400,600,600),(3,2,40,40,500,500,500,500,500);
INSERT INTO "C21-703-7"."Client" Values(100,'PAO SBERBANK',
'Юридический адрес	117312, г. Москва, ул. Вавилова, д.19
БИК	044525225
ИНН	7707083893
КПП	773643001
ОКПО	57972160'),(101,' Российская Государственная Библиотека',
' ИНН 7704097560, ОГРН 1037739390809, ОКПО 02175175');

INSERT INTO "C21-703-7"."Contract" Values(1,'26-03-23','25-03-24',100);
INSERT INTO "C21-703-7"."Contract" Values(2,'26-03-23','25-03-24',100);


