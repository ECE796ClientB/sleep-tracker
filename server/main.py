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
    print("Attempting to Login ", username, ":", password)

    # Return the login ID
    return jsonify({
        'patientId': operations.login(username, password),
        'success': True
    })

@app.route('/createPatient', methods=['POST'])
def createPatient():

    # Get fields from request
    username = request.args.get('username')
    password = request.args.get('password')
    firstName = request.args.get('firstName')
    lastName = request.args.get('lastName')
    age = request.args.get('age')
    gender = request.args.get('gender')
    height = request.args.get('height')
    weight = request.args.get('weight')
    sleepGoals = request.args.get('sleepGoals')
    
    # Create the patient
    print("Creating Patient ", firstName, " ", lastName)
    patientId = operations.createPatient(username, password, firstName, lastName, age, gender, height, weight, sleepGoals)

    # Make sure it was a success
    success = True
    if patientId == 0:
        success = False

    # Return the new Patient ID
    return jsonify({
        'patientId': patientId,
        'success': success
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

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
