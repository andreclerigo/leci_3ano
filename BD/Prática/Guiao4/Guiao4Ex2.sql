CREATE TABLE Airport(
	city VARCHAR(20) NOT NULL,
	airport_code INT NOT NULL,
	country_state VARCHAR(20) NOT NULL,
	airport_name VARCHAR(30) NOT NULL,
	
	PRIMARY KEY (airport_code)
);

CREATE TABLE Airplane_Type(
	max_seats INT NOT NULL CHECK (max_seats > 1),
	type__name VARCHAR(10) NOT NULL,
	company VARCHAR(30) NOT NULL,

	PRIMARY KEY (type__name)
);

CREATE TABLE Can_Land(
	airport_code INT NOT NULL,
	type__name VARCHAR(10) NOT NULL,
	
	PRIMARY KEY (airport_code, type__name),
	FOREIGN KEY (airport_code) REFERENCES Airport(airport_code),
	FOREIGN KEY (type__name) REFERENCES Airplane_Type(type__name)
);

CREATE TABLE Airplane(
	total_seats INT NOT NULL CHECK (total_seats > 1),
	type__name VARCHAR(10) NOT NULL,
	airplane_id INT NOT NULL,

	PRIMARY KEY (airplane_id),
	FOREIGN KEY (type__name) REFERENCES Airplane_Type(type__name)
);

CREATE TABLE Flight(
	airline varchar(30) NOT NULL,
	number INT NOT NULL CHECK (number > 0),
	weekdays varchar(8) NOT NULL,

	PRIMARY KEY (number)
);

CREATE TABLE Flight_Leg(
	leg_no INT NOT NULL,
	flight_number INT NOT NULL CHECK (flight_number > 0),
	cod_airport_dep INT NOT NULL,
	cod_airport_arr INT NOT NULL,
	sched_dep_time TIME NOT NULL,
	sched_arr_time TIME NOT NULL,

	PRIMARY KEY (leg_no, flight_number),
	FOREIGN KEY (flight_number) REFERENCES Flight(number),
	FOREIGN KEY (cod_airport_dep) REFERENCES Airport(airport_code),
	FOREIGN KEY (cod_airport_arr) REFERENCES Airport(airport_code)
);

CREATE TABLE Leg_Instance(
	leg_date DATE NOT NULL,
	leg_no INT NOT NULL,
	flight_number INT NOT NULL CHECK (flight_number > 0),
	cod_airport_dep INT NOT NULL,
	cod_airport_arr INT NOT NULL,
	sched_dep_time TIME NOT NULL,
	sched_arr_time TIME NOT NULL,

	PRIMARY KEY (leg_date, leg_no),
	FOREIGN KEY (leg_no, flight_number) REFERENCES Flight_Leg(leg_no, flight_number),
	FOREIGN KEY (cod_airport_dep) REFERENCES Airport(airport_code),
	FOREIGN KEY (cod_airport_arr) REFERENCES Airport(airport_code)
);

CREATE TABLE Seat(
	seat_no INT NOT NULL CHECK (seat_no > 0),
	flight_number INT NOT NULL CHECK (flight_number > 0),
	leg_no INT NOT NULL,
	costumer_name varchar(50) NOT NULL,
	cphone varchar(9) NOT NULL,
	leg_date DATE NOT NULL,

	PRIMARY KEY (seat_no, flight_number),
	FOREIGN KEY (leg_no, flight_number) REFERENCES Flight_Leg(leg_no, flight_number),
	FOREIGN KEY (leg_date, leg_no) REFERENCES Leg_Instance(leg_date, leg_no)
);