from database import db

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)

class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class Specialization(db.Model):
    __tablename__ ='specialization'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class DoctorSpecialization(db.Model):
    __tablename__ = 'doctor_specialization'
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), primary_key=True)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specialization.id'), primary_key=True)

    doctor = db.relationship('Doctor', backref='specializations')
    specialization = db.relationship('Specialization', backref='doctors')

class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    status = db.Column(db.String, nullable=False)
    
    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')
    room = db.relationship('Room', backref='appointments')
    



