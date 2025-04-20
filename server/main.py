import os
import pytz
import datetime
import operations # Custom file with CRUD operations

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Map containing int -> the day of week, with Sunday being 0
g_DayOfWeek = { 0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}

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
        'patientId': patientId,
        'success': True
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
        'patientId': patientId,
        'success': True
    })

@app.route('/sleepData', methods=['GET'])
def getSleepData():

    patientId = operations.g_PatientIds[10]#request.args.get('patientId')
    

    # Calculate sleep data from last 7 days
    # Get the current time in UTC
    curTime = datetime.datetime.now(pytz.utc)
    lastWeek = curTime - datetime.timedelta(days=7)

    # Get current day of the week
    # Get day of the week as an integer (Monday is 0, Sunday is 6)
    dayOfWeek = curTime.weekday()
    
    # Format the time
    # startTime = lastWeek.strftime('%Y-%m-%dT%H:%M:%SZ')
    # endTime = curTime.strftime('%Y-%m-%dT%H:%M:%SZ')

    startTime = datetime.datetime(2024, 10, 23, 23, 59).isoformat()
    endTime = datetime.datetime(2024, 10, 30, 23, 59).isoformat()

    # Get the Heart Rate and Sleep Hours data
    heartRates = operations.getHeartRateData(patientId, startTime, endTime)
    sleepHours = operations.getHoursSleptData(patientId, startTime, endTime)

    print(heartRates)
    print(sleepHours)

    # Form the return response
    responseData = []
    for i in range(len(heartRates)):
        responseData.append({
            "day": g_DayOfWeek[dayOfWeek],
            "heartRate": heartRates[i],
            "hours": sleepHours[i]
        } )
        dayOfWeek += 1

    # Return the data
    response = {
        'success': True,
        'data': responseData
    }
    return jsonify(response)

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
    
    # Format the time
    # startTime = lastWeek.strftime('%Y-%m-%dT%H:%M:%SZ')
    # endTime = curTime.strftime('%Y-%m-%dT%H:%M:%SZ')
    startTime = datetime.datetime(2024, 10, 23, 0, 0).isoformat()
    endTime = datetime.datetime(2024, 10, 30, 23, 59).isoformat()

     # Get the Heart Rate and Sleep Hours data
    heartRates = operations.getHeartRateData(operations.g_PatientIds[10], startTime, endTime)
    sleepHours = operations.getHoursSleptData(operations.g_PatientIds[10], startTime, endTime)

    print(heartRates)
    print(sleepHours)

    app.run(host='0.0.0.0', port=5000)
