/* Напишите SQL-запрос, который посчитает зарплату по каждому сотруднику по месяцам */

Проверить выполнение запроса можно по ссылке: https://www.db-fiddle.com/f/bguBHeKmijG4YMtzJWGsRc/0

/* Создание таблицы для тестирования: */

CREATE TABLE Employee (
    empid INT PRIMARY KEY,
    empname VARCHAR(255)
);

CREATE TABLE Employee_timesheet (
    empid INT,
    date DATE,
    num_of_hours INT,
    FOREIGN KEY (empid) REFERENCES Employee(empid)
);

CREATE TABLE Employee_hourly_rate (
    empid INT PRIMARY KEY,
    hourly_rate DECIMAL(10, 2),
    FOREIGN KEY (empid) REFERENCES Employee(empid)
);

INSERT INTO Employee (empid, empname) VALUES
(1, 'Иванов Иван'),
(2, 'Петров Петр'),
(3, 'Сидоров Алексей'),
(4, 'Козлов Дмитрий'),
(5, 'Смирнова Елена'),
(6, 'Павлова Анна'),
(7, 'Федоров Денис');

INSERT INTO Employee_timesheet (empid, date, num_of_hours) VALUES
(1, '2024-02-01', 8),
(1, '2024-02-02', 7),
(1, '2024-02-03', 6),
(1, '2024-03-02', 7),
(1, '2024-03-03', 6),
(2, '2024-02-01', 9),
(2, '2024-02-02', 6),
(2, '2024-02-03', 8),
(3, '2024-03-01', 7),
(3, '2024-02-02', 8),
(3, '2024-03-03', 7),
(4, '2024-01-01', 8),
(4, '2024-03-02', 7),
(4, '2024-03-03', 9),
(5, '2024-03-01', 8),
(5, '2024-03-02', 8),
(5, '2024-08-03', 8),
(6, '2024-04-01', 8),
(6, '2024-04-02', 8),
(6, '2024-06-03', 8),
(7, '2024-04-01', 8),
(7, '2024-04-02', 8),
(7, '2024-04-03', 8);

INSERT INTO Employee_hourly_rate (empid, hourly_rate) VALUES
(1, 10.50),
(2, 12.00),
(3, 11.75),
(4, 10.25),
(5, 13.50),
(6, 14.25),
(7, 12.75);

/* Запрос: */

SELECT 
    e.empid,
    e.empname,
    EXTRACT(YEAR FROM et.date) AS year,
    EXTRACT(MONTH FROM et.date) AS month,
    SUM(et.num_of_hours * ehr.hourly_rate) AS salary
FROM 
    Employee e
JOIN 
    Employee_timesheet et ON e.empid = et.empid
JOIN 
    Employee_hourly_rate ehr ON e.empid = ehr.empid
GROUP BY 
    e.empid,
    e.empname,
    EXTRACT(YEAR FROM et.date),
    EXTRACT(MONTH FROM et.date)
ORDER BY 
    e.empid,
    EXTRACT(YEAR FROM et.date),
    EXTRACT(MONTH FROM et.date);