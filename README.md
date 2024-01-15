# Лабораторные работы по предмету "Сетевые технолгии" 4 курс 
----------------------------------------------------------------------------------------
## 2 лабораторная работа
----------------------------------------------------------------------------------------
### Концептуальная модель
На основе анализа предметной области «Гостиница», были выделены следующие информационные объекты, которые необходимо хранить в базе данных:

Таблица GUEST представляет информацию о гостях, которые заказывают номера в гостинице. Она содержит следующие атрибуты: (guest_id, first_name, last_name и phone). Guest_id является уникальным идентификатором каждого гостя, а phone содержит номер телефона гостя.

Таблица ROOM представляет информацию о номерах в гостинице. Она содержит следующие атрибуты: (room_id, room_type, price и availability). Room_id является уникальным идентификатором каждого номера, room_type описывает тип номера, price указывает на стоимость номера, а availability указывает на доступность номера для бронирования.

Таблица RESERVATION представляет информацию о бронированиях номеров. Она содержит следующие атрибуты: (reservation_id, guest_id, room_id, check_in_date и check_out_date). reservation_id является уникальным идентификатором каждой бронирования, guest_id и room_id указывают на гостя и номер соответственно, а check_in_date и check_out_date определяют даты заезда и выезда гостя.

Таблица SERVISE представляет информацию о услугах, которые предлагает гостиница. Она содержит следующие атрибуты: service_id, service_name и price. service_id является уникальным идентификатором каждой услуги, service_name описывает название услуги, а price указывает на стоимость услуги.

Таблица EMPLOYEE представляет информацию о сотрудниках гостиницы. Она содержит следующие атрибуты: (employee_id, first_name, last_name и position). Employee_id является уникальным идентификатором каждого сотрудника, first_name и last_name указывают на имена сотрудников, а position описывает их должность в гостинице.

----------------------------------------------------------------------------------------
## ER-диаграмма
![https://ru.wikihow.com/перестать-ругаться-матом ](/IMG/lab2.png)

----------------------------------------------------------------------------------------
### CREATE TABLE
DROP TABLE IF EXISTS guest;
CREATE TABLE IF NOT EXISTS guest(
  guest_id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name VARCHAR(10),
  last_name VARCHAR(20),
  phone VARCHAR(20)
);

DROP TABLE IF EXISTS room;
CREATE TABLE IF NOT EXISTS room(
  room_id INTEGER PRIMARY KEY AUTOINCREMENT,
  room_type VARCHAR(50),
  price INT,
  availability BOOLEAN
);

DROP TABLE IF EXISTS reservation;
CREATE TABLE IF NOT EXISTS reservation(
  reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
  guest_id INTEGER,
  room_id INTEGER,
  check_in_date DATE,
  check_out_date DATE,
  FOREIGN KEY (guest_id) REFERENCES guest(guest_id) ON DELETE CASCADE,
  FOREIGN KEY (room_id) REFERENCES room(room_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS service;
CREATE TABLE IF NOT EXISTS service(
  service_id INTEGER PRIMARY KEY AUTOINCREMENT,
  service_name VARCHAR(60),
  price INT
);
 
 DROP TABLE IF EXISTS employee;
 CREATE TABLE IF NOT EXISTS employee(
   employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
   first_name VARCHAR(10),
   last_name VARCHAR(20),
   position VARCHAR(20)
);

----------------------------------------------------------------------------------------
### INSERT INTO TABLE
INSERT INTO guest(first_name, last_name, phone) VALUES
('Оля','Лем','8-999-341-20-20'),
('Олег','Казенко','8-800-707-53-11'),
('Настя','Пак','8-903-305-55-55'),
('Ольга','Еренько','8-911-315-17-02'),
('Александр','Миридов','8-814-341-21-21'),
('Макар','Блин','8-900-308-90-90'),
('Андрей','Яковлев','8-888-300-90-15'),
('Игорь','Блинников','8-900-100-11-11'),
('Марат','Лобеев','8-715-715-15-15'),
('Кирилл','Будаев','8-954-411-13-14'),
('Вячеслав','Рубчинский','8-888-900-17-71'),
('Михаил','Блинцов','8-777-105-15-18'),
('Роман','Лукьянов','8-911-228-02-05'),
('Максим','Смирнович','8-000-202-33-33'),
('Алина','Крылёва','8-111-121-02-12'),
('Ирина','Коваль','8-954-311-70-09'),
('Марина','Игнатьенко','8-800-909-11-10');

INSERT into room(room_type, price, availability) values
('Одноместный',2000,0),
('Одноместный',2000,0),
('Одноместный',2300,0),
('Одноместный',2300,0),
('Двуместный',3500,0),
('Двуместный',3500,0),
('Двуместный',3500,0),
('Двуместный',3100,0);

INSERT into reservation(guest_id,room_id,check_in_date, check_out_date) VALUES
(1, 3, '2023-11-05','2023-12-10'),
(2, 2, '2023-11-05','2023-11-11'),
(3, 4, '2023-11-07','2023-11-09'),
(3, 1, '2023-11-07','2023-11-10'),
(5, 6, '2023-11-10','2023-11-11'),
(4, 5, '2023-11-10','2023-11-11'),
(6, 3, '2023-11-11','2023-11-20'),
(7, 2, '2023-11-12', '2023-11-14'),
(8, 2, '2023-11-14', '2023-11-26'),
(9, 1, '2023-11-11', '2023-12-01'),
(10, 4, '2023-11-10', '2023-11-19'),
(11, 1, '2023-12-05', '2023-01-01'),
(12, 6, '2023-11-12', '2023-11-21'),
(12, 5, '2023-11-12', '2023-11-21'),
(13, 4, '2023-11-19', '2023-12-02'),
(14, 4, '2023-12-03','2023-12-29'),
(15, 3, '2023-11-22', '2023-12-11'),
(16, 5, '2023-11-22' , '2023-12-21'),
(17, 1, '2023-01-02','2023-01-11');

INSERT INTO service(service_name, price) VALUES
('Уборка одноместного номера', 1000),
('Уборка двуместного номера', 1800),
('Массаж', 2500),
('Курьер', 250),
('Завтрак', 300),
('Обед', 500),
('Ужин', 400),
('Дополнительные принадлежности', 700);

insert into employee(first_name, last_name, position) VALUES
('Александра','Воронова','хостес'),
('Андрей','Кузнецов','менеджер'),
('Данил','Кузнецов','хостес'),
('Александр','Дюнин','Менеджер'),
('Евгений','Лексусович','Уборщик'),
('Алексей', 'Гасанов', 'Сантехник'),
('Эльнура','Гасанова','Владелец');

----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------
### SELECT
#### 1.1 есть ли гости с именем андрей, скажите какую комнату занял и фамилию/фамилии
SELECT guest.last_name, reservation.reservation_id, reservation.room_id
from guest, reservation
where guest.first_name = 'Андрей' AND guest.guest_id = reservation.guest_id
ORDER by guest.last_name;

#### 1.2 есть ли свободные комнаты для заселение после 10 ноября 2023 типа "двуместный"?
SELECT room.room_id, reservation.reservation_id,  reservation.check_out_date
from reservation, room
where room.room_id = reservation.room_id AND room.room_type = 'Двуместный' AND reservation.check_out_date < '2024-12-21'
order by room.room_id;

----------------------------------------------------------------------------------------
#### 2.1 Написать Ф.И. гостей, у которых номер дороже 2к
SELECT room.room_type, guest.last_name, guest.first_name, reservation.room_id, room.price
FROM guest, reservation, room
WHERE guest.guest_id = reservation.reservation_id AND room.room_id = reservation.room_id AND room.price > 2000
GROUP BY room.room_id
ORDER BY room.room_type, guest.last_name;

#### 2.2 Тоже самое ток с left join
SELECT room.room_type, guest.last_name, guest.first_name, reservation.room_id, room.price
FROM reservation
left JOIN room on reservation.room_id = room.room_id
left JOIN guest on reservation.guest_id = guest.guest_id
WHERE room.price > 2000
GROUP BY room.room_id
ORDER BY room.room_type, guest.last_name;

----------------------------------------------------------------------------------------
#### 3.1 Подзапросы и ключевое слово with
у оли лем есть номер в отеле а еще она заказала себе уборку в своем номере,
 если номер одноместный то уборка одноместного номера прибавляется к стоимости номера,
 иначе прибавляется уборка двухместного. 
также посчитать итоговая оплата = стоимость номера * (выезд- заезд) + доп. услуги

SELECT room.room_type as 'Тип', 
       room.price 'Цена',
       (julianday(reservation.check_out_date) - julianday(reservation.check_in_date)) as 'количество дней',
       room.price*(julianday(reservation.check_out_date) - julianday(reservation.check_in_date)) as 'Итог'
FROM guest, room, reservation
WHERE first_name = 'Оля' AND last_name = 'Лем' AND guest.guest_id = reservation.guest_id AND reservation.room_id = room.room_id;
