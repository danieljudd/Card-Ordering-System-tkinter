CREATE TABLE Orders (
  order_id int IDENTITY(1,1) PRIMARY KEY,
  customer_id int,
  variant_id int,
  quantity int,
  card_size varchar(255)
);

CREATE TABLE Customers (
  customer_id int IDENTITY(1,1) PRIMARY KEY,
  name varchar(255),
  address varchar(255),
  email varchar(255),
  UNIQUE (email)
);

CREATE TABLE Cards (
  variant_id int IDENTITY(1,1) PRIMARY KEY,
  occasion varchar(255),
  card_message_id int
);

CREATE TABLE Card_Message (
  card_message_id int IDENTITY(1,1) PRIMARY KEY,
  message varchar(255)
);

ALTER TABLE Orders ADD FOREIGN KEY (customer_id) REFERENCES Customers (customer_id);

ALTER TABLE Orders ADD FOREIGN KEY (variant_id) REFERENCES Cards (variant_id);

ALTER TABLE Cards ADD FOREIGN KEY (card_message_id) REFERENCES Card_Message (card_message_id);

-- Insert data into Card_Message table
INSERT INTO Card_Message (message) VALUES
('Happy Birthday!'),
('Congratulations on your wedding!'),
('Wishing you a Merry Christmas!'),
('Get well soon!'),
('Best of luck in your new job!'),
('Happy 40th Birthday!'),
('We''ll miss you, good luck!'),
('Congratulations'),
('We''re proud of you'),
('Take it easy'),
('Feliz Navidad'), -- 11
('Tying the knot');

-- Insert data into Cards table
INSERT INTO Cards (occasion, card_message_id) VALUES
('Birthday', 1),
('Wedding', 2),
('Christmas', 3),
('Get Well', 4),
('New Job', 5),
('Birthday', 6),
('Birthday', 1),
('Birthday', 6),
('Birthday', 8),
('Get Well', 10),
('Birthday', 8),
('Wedding', 12),
('Birthday', 6),
('Birthday', 8),
('Get Well', 10),
('New Job', 5),
('Birthday', 1),
('Wedding', 2),
('Christmas', 3),
('Christmas', 11),
('Christmas', 3),
('New Job', 8),
('New Job', 7),
('Get Well', 9),
('Wedding', 9);

-- Insert data into Customers table
INSERT INTO Customers (name, address, email) VALUES
('Alice Johnson', '123 Maple Street', 'ajohnson@gmail.com'),
('Bob Smith', '456 Oak Avenue','bsmith@gmail.com'),
('Charlie Brown', '789 Pine Road','cbrown@gmail.com'),
('Diana Prince', '101 Elm Drive','dprice@gmail.com'),
('Ethan Hunt', '202 Cedar Lane','ehunt@gmail.com');

-- Insert data into Orders table
INSERT INTO Orders (customer_id, variant_id, quantity, card_size) VALUES
(1, 1, 2, 'A4'),
(2, 2, 1, 'A6'),
(3, 3, 5, 'A4'),
(4, 4, 3, 'A5'),
(5, 5, 2, 'A4');
