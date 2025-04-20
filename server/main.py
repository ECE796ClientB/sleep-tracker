import os
import datetime
import operations # Custom file with CRUD operations

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/login', methods=['GET'])
def login():

    username = request.args.get('username')
    password = request.args.get('password')

    patientId = operations.login(username, password)
    print("Attempting to Login for ", username)
    if patientId != 0:
        print("Successful Login for Patient ", patientId)
    else:
        print("Unsuccessful Login, could not find Patient")

    # Return the login ID
    return jsonify({
        'patientId': patientId
    })

@app.route('/createPatient', methods=['POST'])
def createPatient():

    # Get the request args
    patientRequest = request.get_json()

    # Get fields from request
    username = patientRequest.get('username')
    password = patientRequest.get('password')
    firstName = patientRequest.get('firstName')
    lastName = patientRequest.get('lastName')
    age = patientRequest.get('age')
    gender = patientRequest.get('gender')
    height = patientRequest.get('height')
    weight = patientRequest.get('weight')
    sleepGoals = patientRequest.get('sleepGoals')
    
    # Create the patient
    patientId = operations.createPatient(username, password, firstName, lastName, age, gender, height, weight, sleepGoals)
    print("Created Patient ", patientId, ": ", firstName, " ", lastName)

    # Return the new Patient ID
    return jsonify({
        'patientId': patientId
    })

# Setup App
def setup():
    
    #######################################################################
    # Connect to the FHIR server
    #######################################################################

    url = operations.g_fhirUrl + '/metadata'
    operations.connectToFhirServer(url)

    #######################################################################
    # Now that we're connected, load the data
    #######################################################################
    
    operations.loadData()

    # # #######################################################################
    # # # Test Functions
    # # #######################################################################

    # # Start/End times
    # startTime = datetime.datetime(2024, 9, 30, 0, 0).isoformat()
    # endTime = datetime.datetime(2024, 12, 28, 23, 59).isoformat()

    # for i in range(10, 11):

    #     # Get data
    #     heartRates = operations.getHeartRateData(operations.g_PatientIds[i], startTime, endTime)
    #     # print("Heart Rates: ", heartRates)
    #     stressLevel = operations.getAverageStressLevel(operations.g_PatientIds[i], startTime, endTime)
    #     print("Stress Level: ", stressLevel)
    #     exerciseHours = operations.getAverageExerciseHours(operations.g_PatientIds[i], startTime, endTime)
    #     print("Exercise Hours: ", exerciseHours)
    #     caffeineIntake = operations.getAverageCaffeineIntake(operations.g_PatientIds[i], startTime, endTime)
    #     print("Caffeine Intake: ", caffeineIntake)
    #     # sleepQuality = operations.calculateSleepQuality(heartRates)
    #     # print("Sleep Quality: ", sleepQuality)

    #     # Flood the stress levels with no stress to verify the addStress works
    #     for j in range(0, 10):
    #         operations.addStressEntry(operations.g_PatientIds[i], "No stress")
    #         operations.addExerciseEntry(operations.g_PatientIds[i], 5)
    #         operations.addCaffeineIntake(operations.g_PatientIds[i], 4)
    #     endTime = datetime.datetime(2026, 12, 28, 23, 59).isoformat()
    #     stressLevel = operations.getAverageStressLevel(operations.g_PatientIds[i], startTime, endTime)
    #     exerciseHours = operations.getAverageExerciseHours(operations.g_PatientIds[i], startTime, endTime)
    #     caffeineIntake = operations.getAverageCaffeineIntake(operations.g_PatientIds[i], startTime, endTime)
    #     print("Updated Stress Level: ", stressLevel)
    #     print("Updated Exercise Hours: ", exerciseHours)
    #     print("Updated Caffeine Intake: ", caffeineIntake)

    # myId = operations.createPatient("username", "password", "Joe", "Balsamo", "27", "male", "6 ft 0 in", "185", "Reduce wakeups during the night, Improve sleep quality")
    # operations.updateSleepGoals(operations.g_PatientIds[myId], "Test")
    # # getPatient(g_PatientIds[myId])

if __name__ == '__main__':
    
    # Connect to FHIR Server and load patients and observations
    setup()

    app.run(host='0.0.0.0', port=5000)
