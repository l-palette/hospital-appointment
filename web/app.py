from flask import Flask, request, render_template
from models import (
    Patient,
    Doctor,
    Specialization,
    Room,
    Appointment,
    DoctorSpecialization,
)
from database import db
from datetime import datetime
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)
db_url = os.getenv("APP_DATABASE_URL")

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = db_url

db.init_app(app)


@app.route("/")
def home():
    return "hello"


# Patient routes
@app.route("/registration_office", methods=["GET", "POST"])
def patients():
    if request.method == "GET":
        query = db.session.query(
            Patient.id, Patient.name, Patient.address, Patient.telephone
        )
        results = query.all()
        patients_list = [
            {
                "id": result.id,
                "name": result.name,
                "address": result.address,
                "telephone": result.telephone,
            }
            for result in results
        ]
        return {
            "message": "Patients list",
            "method": request.method,
            "results": patients_list,
        }

    if request.method == "POST":
        data = request.json
        new_patient = Patient(
            name=data["name"], address=data["address"], telephone=data["telephone"]
        )
        db.session.add(new_patient)
        db.session.commit()

        return {
            "message": "Add new patient",
            "data": {
                "id": new_patient.id,
                "name": new_patient.name,
                "address": new_patient.address,
                "telephone": new_patient.telephone,
            },
            "method": request.method,
        }


@app.route("/registration_office/<int:id>", methods=["GET", "PUT", "DELETE"])
def patient(id):
    patient = Patient.query.get(id)
    if request.method == "GET":
        return {
            "id": id,
            "name": patient.name,
            "address": patient.address,
            "telephone": patient.telephone,
            "message": "data about patient {}".format(id),
            "method": request.method,
        }

    if request.method == "PUT":
        data = request.json
        patient.name = data["name"]
        patient.address = data["address"]
        patient.telephone = data["telephone"]
        db.session.commit()
        return {
            "id": id,
            "message": "Update patients data {}".format(id),
            "method": request.method,
            "body": data,
        }

    if request.method == "DELETE":
        db.session.delete(patient)
        db.session.commit()
        return {
            "id": id,
            "message": "Delete patients data {}".format(id),
            "method": request.method,
        }


# Doctor routes
@app.route("/doctors", methods=["GET", "POST"])
def doctors():
    if request.method == "GET":
        doctors_list = Doctor.query.all()
        return {
            "message": "Doctors list",
            "results": [{"id": doc.id, "name": doc.name} for doc in doctors_list],
        }
    # TODO бубубу
    if request.method == "POST":
        data = request.json
        new_doctor = Doctor(name=data["name"])
        db.session.add(new_doctor)
        db.session.commit()
        return {
            "message": "Add new doctor",
            "data": {"id": new_doctor.id, "name": new_doctor.name},
        }


@app.route("/doctors/<int:id>", methods=["GET", "PUT", "DELETE"])
def doctor(id):
    doctor = Doctor.query.get(id)
    if request.method == "GET":
        return {"id": id, "name": doctor.name}

    if request.method == "PUT":
        data = request.json
        doctor.name = data["name"]
        db.session.commit()
        return {"message": "Update doctor data", "id": id}

    if request.method == "DELETE":
        db.session.delete(doctor)
        db.session.commit()
        return {"message": "Delete doctor data", "id": id}


# Specialization routes
@app.route("/specializations", methods=["GET", "POST"])
def specializations():
    if request.method == "GET":
        specializations_list = Specialization.query.all()
        return {
            "message": "Specializations list",
            "results": [
                {"id": spec.id, "name": spec.name} for spec in specializations_list
            ],
        }

    if request.method == "POST":
        data = request.json
        new_specialization = Specialization(name=data["name"])
        db.session.add(new_specialization)
        db.session.commit()
        return {
            "message": "Add new specialization",
            "data": {"id": new_specialization.id, "name": new_specialization.name},
        }


@app.route("/specializations/<int:id>", methods=["GET", "PUT", "DELETE"])
def specialization(id):
    specialization = Specialization.query.get(id)
    if request.method == "GET":
        return {"id": id, "name": specialization.name}

    if request.method == "PUT":
        data = request.json
        specialization.name = data["name"]
        db.session.commit()
        return {"message": "Update specialization data", "id": id}

    if request.method == "DELETE":
        db.session.delete(specialization)
        db.session.commit()
        return {"message": "Delete specialization data", "id": id}


# Room routes
@app.route("/rooms", methods=["GET", "POST"])
def rooms():
    if request.method == "GET":
        rooms_list = Room.query.all()
        return {
            "message": "Rooms list",
            "results": [{"id": room.id, "name": room.name} for room in rooms_list],
        }

    if request.method == "POST":
        data = request.json
        new_room = Room(name=data["name"])
        db.session.add(new_room)
        db.session.commit()
        return {
            "message": "Add new room",
            "data": {"id": new_room.id, "name": new_room.name},
        }


@app.route("/rooms/<int:id>", methods=["GET", "PUT", "DELETE"])
def room(id):
    room = Room.query.get(id)
    if request.method == "GET":
        return {"id": id, "name": room.name}

    if request.method == "PUT":
        data = request.json
        room.name = data["name"]
        db.session.commit()
        return {"message": "Update room data", "id": id}

    if request.method == "DELETE":
        db.session.delete(room)
        db.session.commit()
        return {"message": "Delete room data", "id": id}


# Appointment routes
@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    if request.method == "GET":
        appointments_list = Appointment.query.all()
        return {
            "message": "Appointments list",
            "results": [
                {
                    "id": appt.id,
                    "patient_id": appt.patient_id,
                    "doctor_id": appt.doctor_id,
                    "time": appt.time.strftime("%H:%M:%S"),  # Convert time to string
                    "date": appt.date.strftime("%Y-%m-%d"),  # Convert date to string
                    "room_id": appt.room_id,
                    "status": appt.status,
                }
                for appt in appointments_list
            ],
        }

    if request.method == "POST":
        data = request.json
        new_appointment = Appointment(
            patient_id=data["patient_id"],
            doctor_id=data["doctor_id"],
            time=datetime.strptime(
                data["time"], "%H:%M:%S"
            ).time(),  # Convert string to time
            date=datetime.strptime(
                data["date"], "%Y-%m-%d"
            ).date(),  # Convert string to date
            room_id=data["room_id"],
            status=data["status"],
        )
        db.session.add(new_appointment)
        db.session.commit()
        return {"message": "Add new appointment", "data": {"id": new_appointment.id}}


@app.route("/appointments/<int:id>", methods=["GET", "PUT", "DELETE"])
def appointment(id):
    appointment = Appointment.query.get(id)
    if request.method == "GET":
        return {
            "id": id,
            "patient_id": appointment.patient_id,
            "doctor_id": appointment.doctor_id,
            "time": appointment.time.strftime("%H:%M:%S"),  # Convert time to string
            "date": appointment.date.strftime("%Y-%m-%d"),  # Convert date to string
            "room_id": appointment.room_id,
            "status": appointment.status,
        }

    if request.method == "PUT":
        data = request.json
        appointment.patient_id = data["patient_id"]
        appointment.doctor_id = data["doctor_id"]
        appointment.time = datetime.strptime(
            data["time"], "%H:%M:%S"
        ).time()  # Convert string to time
        appointment.date = datetime.strptime(
            data["date"], "%Y-%m-%d"
        ).date()  # Convert string to date
        appointment.room_id = data["room_id"]
        appointment.status = data["status"]
        db.session.commit()
        return {"message": "Update appointment data", "id": id}

    if request.method == "DELETE":
        db.session.delete(appointment)
        db.session.commit()
        return {"message": "Delete appointment data", "id": id}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
