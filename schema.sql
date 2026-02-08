-- Coffee Shop Database Schema

-- Employee Table
CREATE TABLE Employee (
    SSN CHAR(11) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE,
    salary NUMERIC(10,2) CHECK (salary >= 0)
);

-- Manager Table
CREATE TABLE Manager (
    SSN CHAR(11) PRIMARY KEY,
    ownership_percentage NUMERIC(5,2) CHECK (ownership_percentage BETWEEN 0.00 AND 100.00),
    FOREIGN KEY (SSN) REFERENCES Employee(SSN) ON DELETE CASCADE
);

-- Barista Table
CREATE TABLE Barista (
    SSN CHAR(11) PRIMARY KEY,
    FOREIGN KEY (SSN) REFERENCES Employee(SSN) ON DELETE CASCADE
);

-- Barista Schedule Table
CREATE TABLE Barista_Schedule (
    barista_SSN CHAR(11),
    day_of_week VARCHAR(9) CHECK (day_of_week IN ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    CHECK (start_time < end_time),
    PRIMARY KEY (barista_SSN, day_of_week, start_time),
    FOREIGN KEY (barista_SSN) REFERENCES Barista(SSN) ON DELETE CASCADE
);

-- Accounting Table
CREATE TABLE Accounting (
    entry_date TIMESTAMP PRIMARY KEY,
    balance NUMERIC(10,2) NOT NULL
);

-- Menu Table
CREATE TABLE Menu (
    name VARCHAR(100) PRIMARY KEY,
    size INT CHECK (size > 0),
    type VARCHAR(20) CHECK (type IN ('Tea','Coffee','Soft Drink')),
    price NUMERIC(10,2) CHECK (price >= 0),
    temperature VARCHAR(4) CHECK (temperature IN ('Hot', 'Cold'))
);

-- Recipes Table
CREATE TABLE Recipes (
    name VARCHAR(100) PRIMARY KEY,
    FOREIGN KEY (name) REFERENCES Menu(name) ON DELETE CASCADE
);

-- Preparation Step Table
CREATE TABLE PreparationStep (
    name VARCHAR(100) NOT NULL,
    step_number INT CHECK (step_number > 0),
    step_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (name, step_number),
    FOREIGN KEY (name) REFERENCES Recipes(name) ON DELETE CASCADE
);

-- Inventory Table
CREATE TABLE Inventory (
    item_name VARCHAR(100) PRIMARY KEY,
    unit VARCHAR(50) NOT NULL,
    price NUMERIC(10,2) CHECK (price >= 0),
    quantity_in_stock NUMERIC(10,2) CHECK (quantity_in_stock >= 0)
);

-- Ingredient Table
CREATE TABLE Ingredient (
    name VARCHAR(100) NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    quantity NUMERIC(10,2) CHECK (quantity >= 0),
    unit VARCHAR(50) NOT NULL,
    PRIMARY KEY (name, item_name),
    FOREIGN KEY (name) REFERENCES Recipes(name) ON DELETE CASCADE,
    FOREIGN KEY (item_name) REFERENCES Inventory(item_name) ON DELETE CASCADE
);

-- Sales Table
CREATE TABLE Sales (
    order_id VARCHAR(20) PRIMARY KEY,
    order_time TIMESTAMP NOT NULL,
    payment_method VARCHAR(20) CHECK (payment_method IN('Cash','Credit Card','App')),
    total NUMERIC(10,2) CHECK (total >= 0),
    FOREIGN KEY (order_time) REFERENCES Accounting(entry_date)
);

-- Line Item Table
CREATE TABLE LineItem (
    order_id VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    line_item_total NUMERIC(10,2) CHECK (line_item_total >= 0),
    PRIMARY KEY (order_id, name),
    FOREIGN KEY (order_id) REFERENCES Sales(order_id) ON DELETE CASCADE,
    FOREIGN KEY (name) REFERENCES Menu(name)
);

-- Indexes for Performance
CREATE INDEX employee_email_idx ON Employee(email);
CREATE INDEX employee_name_idx ON Employee(name);
CREATE INDEX barista_ssn_idx ON Barista_Schedule(barista_SSN);
CREATE INDEX preparationstep_name_idx ON PreparationStep(name);
CREATE INDEX ingredient_name_idx ON Ingredient(name);
CREATE INDEX sales_order_time_idx ON Sales(order_time);
CREATE INDEX lineitem_name_idx ON LineItem(name);
