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

# 1 Cup of Coffee worth of Caffeien (mg)
g_OneCupCoffeeCaffeineMg = 95

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

    patientId = operations.g_PatientIds[int(request.args.get('patientId'))]
    
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

    startTime = datetime.datetime(2024, 12, 16, 23, 59).isoformat()
    endTime = datetime.datetime(2024, 12, 30, 23, 59).isoformat()

    # Get the Heart Rate and Sleep Hours data
    heartRates = operations.getHeartRateData(patientId, startTime, endTime)
    sleepHours = operations.getHoursSleptData(patientId, startTime, endTime)

    # Get Caffeine
    stressLevels = operations.getStressLevels(patientId, startTime, endTime)
    exerciseHours = operations.getExerciseHours(patientId, startTime, endTime)
    caffeine = operations.getCaffeineIntake(patientId, startTime, endTime)

    # Get Age
    age = operations.getAge(patientId)

    # Form the return response
    responseData = []
    for i in range(len(heartRates)):
        responseData.append({
            "day": g_DayOfWeek[dayOfWeek],
            "heartRate": heartRates[i],
            "hours": sleepHours[i],
            "caffeine": caffeine[i],
            "exercise": exerciseHours[i],
            "stress": stressLevels[i],
            "age": age
        } )
        dayOfWeek = (dayOfWeek + 1) % 7

    # Return the data
    return jsonify({
        'success': True,
        'data': responseData
    })

@app.route('/logDailies', methods=['POST'])
def logDailies():

    patientId = operations.g_PatientIds[int(request.args.get('patientId'))]
    stressLevel = request.args.get('stressLevel')
    exercise = request.args.get('exercise')
    cupsCoffee = request.args.get('caffeine')

    operations.addStressEntry(patientId, stressLevel)
    operations.addExerciseEntry(patientId, exercise)
    operations.addCaffeineIntake(patientId, cupsCoffee * g_OneCupCoffeeCaffeineMg)

    return jsonify({
        'success': True
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

if __name__ == '__main__':
    
    # Connect to FHIR Server and load patients and observations
    setup()
    app.run(host='0.0.0.0', port=5000)
