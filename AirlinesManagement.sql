
CREATE DATABASE IF NOT EXISTS rec;

USE rec;

CREATE TABLE airline (
    flightNo INT PRIMARY KEY,
    amount INT NOT NULL,
    seats INT NOT NULL

);

INSERT INTO airline (flightNo, amount, seats) VALUES
(101, 5000, 5),
(102, 6500, 18),
(103, 4200, 11);
