CREATE SEQUENCE IF NOT EXISTS patientid_seq START WITH 1;
CREATE TABLE IF NOT EXISTS patient (
    id INT PRIMARY KEY DEFAULT nextval('patientid_seq'),
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    telephone VARCHAR(20) NOT NULL
);

CREATE SEQUENCE IF NOT EXISTS doctor_id START WITH 1;
CREATE TABLE doctor (
    id INT PRIMARY KEY DEFAULT nextval('doctor_id'),
    name VARCHAR(255) NOT NULL
);

CREATE SEQUENCE IF NOT EXISTS specialization_id START WITH 1;
CREATE TABLE specialization (
    id INT PRIMARY KEY DEFAULT nextval('specialization_id'),
    name VARCHAR(255) NOT NULL
);

CREATE SEQUENCE IF NOT EXISTS doctor_specialization_id START WITH 1;
CREATE TABLE doctor_specialization (
    id INT PRIMARY KEY DEFAULT nextval('doctor_specialization_id'),
    doctor_id INT REFERENCES doctor(id),
    specialization_id INT REFERENCES specialization(id)
);

CREATE SEQUENCE IF NOT EXISTS room_id START WITH 1;
CREATE TABLE room (
    id INT PRIMARY KEY DEFAULT nextval('room_id'),
    name VARCHAR(20) NOT NULL
);

CREATE SEQUENCE IF NOT EXISTS appointment_id START WITH 1;
CREATE TABLE appointment ( 
    id INT PRIMARY KEY DEFAULT nextval('appointment_id'),
    patient_id INT REFERENCES patient(id),
    doctor_id INT REFERENCES doctor(id),
    time TIME NOT NULL,
    date DATE NOT NULL,
    room_id INT REFERENCES room(id),
    status VARCHAR NOT NULL
);
