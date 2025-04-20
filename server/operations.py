import json
import os
import re
import time
import datetime
from fhirclient import client
from fhirclient.models import patient, observation
import requests
import pytz


# FHIR URL
g_fhirUrl = 'https://hapi.up.railway.app/fhir'

# Create dictionary of patient file to FHIR resource ID
g_PatientIds = dict()
g_PatientIdCounter = int(1)
g_PatientLogins = dict()
g_PatientUsernames = list()

# 1 Cup of Coffee worth of Caffeien (mg)
g_OneCupCoffeeCaffeineMg = 95

# Now get the average stress level
# This can be calculated by translating the stress levels to an int
# No Stress = 0
# Low Stress = 1
# Moderate Stress = 2
# High Stress = 3
# Extremely Stressed = 4
g_stressLevelToVal = { "No stress":0, "Low stress":1, "Moderate stress":2, "High stress":3, "Extremely stressed":4 }
g_valToStressLevel = { 0:"No stress", 1:"Low stress", 2:"Moderate stress", 3:"High stress", 4:"Extremely stressed" }

# Configure the FHIR client with the server URL
def create_fhir_client():
    settings = {
        'app_id': 'python-fhir-client',  # This is the application ID, can be anything unique
        'api_base': g_fhirUrl  # HAPI FHIR server URL (R4 version)
    }
    fhir_client = client.FHIRClient(settings=settings)
    return fhir_client

# Get Observations of a patient filtered by lonic code, start, and end times
def getDataValueByLonicCode(patientId, lonicCode):

    # FHIR Client
    fhir_client = create_fhir_client()

    # Build query
    searchParams = {
        'patient': patientId,
        'code': f'{lonicCode}'
    }

    # Execute query
    observations = observation.Observation.where(searchParams).perform_resources(fhir_client.server)

    return observations[0].valueQuantity.value

# Get Observations of a patient filtered by lonic code, start, and end times
def getDataValuesByLonicCode(patientId, startTime, endTime, lonicCode):

    # FHIR Client
    fhir_client = create_fhir_client()

    # Build query
    searchParams = {
        'patient': patientId,
        'date': f'ge{startTime}',
        'date': f'le{endTime}',
        'code': f'{lonicCode}'
    }

    # Execute query
    observations = observation.Observation.where(searchParams).perform_resources(fhir_client.server)

     # Parse results
    values = []
    for obs in observations:
        
        # Debug prints
        # print(f"Observation ID: {obs.id}")
        # print(f"Effective Date: {obs.effectiveDateTime.as_json()}")
        # print(f"Value: {obs.valueQuantity.value} {obs.valueQuantity.unit}")
        # print(f"Patient Reference: {obs.subject.reference}")
        # print('--------------------------------------------------------------------------------')

         # Append value
        values.append( obs.valueQuantity.value )

    return values

# Get Observations of a patient filtered by code text, start, and end times
def getDataValuesByCodeText(patientId, startTime, endTime, codeText):

    # FHIR Client
    fhir_client = create_fhir_client()

    # Build query
    searchParams = {
        'patient': patientId,
        'date': f'ge{startTime}',
        'date': f'le{endTime}',
        'code:text': f'{codeText}'
    }

    # Execute query
    observations = observation.Observation.where(searchParams).perform_resources(fhir_client.server)

     # Parse results
    values = []
    for obs in observations:
         # Append value
        values.append( obs.valueQuantity.value )

    return values

# Get Observations of a patient filtered by lonic code, start, and end times
def getDataValueStringByCodeText(patientId, codeText):

    # FHIR Client
    fhir_client = create_fhir_client()

    # Build query
    searchParams = {
        'patient': patientId,
        'code:text': f'{codeText}'
    }

    # Execute query
    observations = observation.Observation.where(searchParams).perform_resources(fhir_client.server)

    # Parse results
    return observations[0].valueString

# Get Observations of a patient filtered by lonic code, start, and end times
def getDataValueStringsByCodeText(patientId, startTime, endTime, codeText):

    # FHIR Client
    fhir_client = create_fhir_client()

    # Build query
    searchParams = {
        'patient': patientId,
        'date': f'ge{startTime}',
        'date': f'le{endTime}',
        'code:text': f'{codeText}'
    }

    # Execute query
    observations = observation.Observation.where(searchParams).perform_resources(fhir_client.server)

     # Parse results
    values = []
    for obs in observations:
        
        # Debug prints
        # print(f"Observation ID: {obs.id}")
        # print(f"Effective Date: {obs.effectiveDateTime.as_json()}")
        # print(f"Value: {obs.valueString}")
        # print(f"Patient Reference: {obs.subject.reference}")
        # print('--------------------------------------------------------------------------------')

         # Append value
        values.append( obs.valueString )

    return values

# Get the current time timestamp
def getCurTime():
    
    # Get the current time in UTC
    curTime = datetime.datetime.now(pytz.utc)

    # Format the current time in the desired format: YYYY-MM-DDTHH:MM:SSZ
    timestamp = curTime.strftime('%Y-%m-%dT%H:%M:%SZ')

    return timestamp

# Get Heart Rates of a patient filtered by start and end times
def getHeartRateData(patientId, startTime, endTime):

    # Define the LOINC code for "Heart rate"
    loincCode = "8867-4"

    # Heart Rates, along with the time
    heartRates = getDataValuesByLonicCode(patientId, startTime, endTime, loincCode)

    # Return heart rates    
    return heartRates

# Get Heart Rates of a patient filtered by start and end times
def getHoursSleptData(patientId, startTime, endTime):

    # Define the LOINC code for "Hours Slept"
    loincCode = "76498-7"

    # Hours Slept, along with the time
    hoursSlept = getDataValuesByLonicCode(patientId, startTime, endTime, loincCode)

    # Return heart rates    
    return hoursSlept

# Get Heart Rates of a patient filtered by start and end times
def getAverageStressLevel(patientId, startTime, endTime):

    # Code text for Stress Level
    codeText = "Stress level"

    # Stress Levels
    stressLevels = getDataValueStringsByCodeText(patientId, startTime, endTime, codeText)

    # Parse the stress levels and calculate the average
    averageStressVal = 0
    for stressLevel in stressLevels:
        averageStressVal += g_stressLevelToVal[stressLevel]

    averageStressVal /= len(stressLevels)

    # Return average stress level   
    return g_valToStressLevel[round(averageStressVal)]

# Get Average Exercise Hours for a patient filtered by start and end times
def getAverageExerciseHours(patientId, startTime, endTime):

    # Code text for Stress Level
    codeText = "Exercise"

    # Stress Levels
    exerciseHours = getDataValuesByCodeText(patientId, startTime, endTime, codeText)

    print("Exercise Hour Entries: ", exerciseHours)

    # Parse the stress levels and calculate the average
    averageExercise = 0
    for exerciseHour in exerciseHours:
        averageExercise += exerciseHour

    averageExercise /= len(exerciseHours)

    # Return average exercise hourse   
    return averageExercise

# Get Average Caffeine Intake for a patient filtered by start and end times
def getAverageCaffeineIntake(patientId, startTime, endTime):

    # Code text for Stress Level
    codeText = "Caffeine intake"

    # Stress Levels
    caffeineIntakes = getDataValuesByCodeText(patientId, startTime, endTime, codeText)

    # Parse the stress levels and calculate the average
    averageCaffeineIntake = 0
    for caffeineIntake in caffeineIntakes:
        averageCaffeineIntake += caffeineIntake

    averageCaffeineIntake /= len(caffeineIntakes)

    # Return average caffeine intake   
    return averageCaffeineIntake

# Calculate the sleep quality based on heart rate and patient data
# def calculateSleepQuality(heartRates):

#     # Average Heart Rate
#     averageHearRate = 0

#     # Calculate the average heart rate
#     for hearRate in heartRates:
#         averageHearRate += hearRate
#     averageHearRate /= len(heartRates)

#     # Just return average for now
#     return averageHearRate

# Creates a patient
def createPatient(username, password, firstName, lastName, age, gender, height, weight, sleepGoals):

    global g_PatientIdCounter

    # Only continue if the username does not exist
    if username in g_PatientUsernames:
        return 0

    # Create the Patient
    patientRequest = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
            "resource": {
                "resourceType": "Patient",
                "name": [
                {
                    "use": "official",
                    "family": f"{lastName}",
                    "given": [
                        f"{firstName}"
                    ]
                }
                ],
                "gender": f"{gender}",
            },
            "request": {
                "method": "POST",
                "url": "Patient"
            }
            }
        ]
    }

    # Send POST request with JSON data
    response = requests.post(g_fhirUrl, json=patientRequest)

    # Patient ID
    retId = 0
    patientId = 0

    # Check the response status and print the result
    if response.status_code == 200:
        print('Successfully created patient')

        # Save the Patient ID
        match = re.search(r'/(?P<number>\d+)/', response.json()['entry'][0]['response']['location'])
        patientId = match.group('number')
        g_PatientIds[g_PatientIdCounter] = patientId # Get the non-FHIR Patient ID from the filename 
        # print(response.json())
        retId = g_PatientIdCounter
        g_PatientLogins[(username, password)] = retId
        g_PatientUsernames.append(username)
        g_PatientIdCounter +=1
    else:
        print('Failed to create patient')
        print(f'Status code: {response.status_code}')
        return 0

    # Get current time
    curTime = getCurTime()

    # Create the Age, Height, and Weight Observations
    observationRequest = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
            "resource": {
                "resourceType": "Observation",
                "id": "1a732120-fd02-4446-b079-e8398654e020",
                "status": "final",
                "code": {
                "text": "Sleep goals"
                },
                "subject": {
                "reference": f"Patient/{patientId}"
                },
                "effectiveDateTime": f"{curTime}",
                "valueString": f"{sleepGoals}"
            },
            "request": {
                "method": "POST",
                "url": "Observation"
            }
            },      
            {
            "resource": {
                "resourceType": "Observation",
                "id": "98f9d448-4dba-4bb9-9ac9-105506909001",
                "status": "final",
                "code": {
                "coding": [
                    {
                    "code": "30525-0",
                    "display": "Age",
                    "system": "http://loinc.org"
                    }
                ],
                "text": "Age"
                },
                "subject": {
                "reference": f"Patient/{patientId}"
                },
                "effectiveDateTime": f"{curTime}",
                "valueQuantity": {
                "value": age,
                "unit": "years"
                }
            },
            "request": {
                "method": "POST",
                "url": "Observation"
            }
            },
            {
            "resource": {
                "resourceType": "Observation",
                "id": "3ffd7298-5b93-4cc0-91ca-841ad488013d",
                "status": "final",
                "code": {
                "text": "Body height"
                },
                "subject": {
                "reference": f"Patient/{patientId}"
                },
                "effectiveDateTime": f"{curTime}",
                "valueString": f"{height}"
            },
            "request": {
                "method": "POST",
                "url": "Observation"
            }
            },
            {
            "resource": {
                "resourceType": "Observation",
                "id": "ee880b8a-7fca-41b3-a34a-7aae03044afd",
                "status": "final",
                "code": {
                "coding": [
                    {
                    "code": "29463-7",
                    "display": "Body weight",
                    "system": "http://loinc.org"
                    }
                ],
                "text": "Body weight"
                },
                "subject": {
                "reference": f"Patient/{patientId}"
                },
                "effectiveDateTime": f"{curTime}",
                "valueQuantity": {
                "value": weight,
                "unit": "lb"
                }
            },
            "request": {
                "method": "POST",
                "url": "Observation"
            }
            }
        ]
    }

    # Send POST request with JSON data
    response = requests.post(g_fhirUrl, json=observationRequest)

    # Check the response status and print the result
    if response.status_code != 200:
        print('Failed to create observations')
        print(f'Status code: {response.status_code}')

    return retId

# Update Sleep Goals
def updateSleepGoals(patientId, sleepGoals):

     # FHIR Client
    fhir_client = create_fhir_client()

    # Get current sleep goal observation

    # Build query
    searchParams = {
        'patient': patientId,
        'code:text': 'Sleep goals'
    }

    # Execute query
    observations = observation.Observation.where(searchParams).perform_resources(fhir_client.server)

    # Update observation
    observations[0].valueString = sleepGoals
    observations[0].update(fhir_client.server)
    
# Get Age
def getAge(patientId):
    return getDataValueByLonicCode(patientId, "30525-0")

# Get Height
def getHeight(patientId):
    return getDataValueStringByCodeText(patientId, "Body height")

# Get Weight
def getWeight(patientId):
    return getDataValueByLonicCode(patientId, "29463-7")

# Get Sleep Goals
def getSleepGoals(patientId):
    return getDataValueStringByCodeText(patientId, "Sleep Goals")

# Fetch patient information by ID from the FHIR server
def getPatient(patientId):

    fhir_client = create_fhir_client()
    
    # Patient
    patientResource = patient.Patient.read(patientId, fhir_client.server)

    # Age
    age = getAge(patientId)

    # Height
    height = getHeight(patientId)

    # Weight
    weight = getWeight(patientId)

    # Sleep Goals
    sleepGoals = getSleepGoals(patientId)

    print("Patient found:")
    print(f"Name: {patientResource.name[0].given[0]} {patientResource.name[0].family}")
    print(f"Age: {age}")
    print(f"Height: {height}")
    print(f"Weight: {weight}")
    print(f"Sleep Goals: {sleepGoals}")

    return patientResource, age, height, weight
    
# Add a Stress Level entry
def addStressEntry(patientId, stressLevel):

    # Get current time
    curTime = getCurTime()

    # Create the Age, Height, and Weight Observations
    observationRequest = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
            "resource": {
                "resourceType": "Observation",
                "id": "33eeed4f-125a-4f6e-9612-28bc17fb0b96",
                "status": "final",
                "code": {
                "text": "Stress level"
                },
                "subject": {
                "reference": f"Patient/{patientId}"
                },
                "effectiveDateTime": curTime,
                "valueString": f"{stressLevel}"
            },
            "request": {
                "method": "POST",
                "url": "Observation"
            }
            }
        ]
    }

    # Send POST request with JSON data
    response = requests.post(g_fhirUrl, json=observationRequest)

    # Check the response status and print the result
    if response.status_code != 200:
        print('Failed to create observation')
        print(f'Status code: {response.status_code}')

# Add a Exercise entry
def addExerciseEntry(patientId, hours):

    # Get current time
    curTime = getCurTime()

    # Create the Age, Height, and Weight Observations
    observationRequest = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "resource": {
                    "resourceType": "Observation",
                    "id": "9e2e592e-20f0-47d3-87d4-6097dfbec555",
                    "status": "final",
                    "code": {
                    "text": "Exercise"
                    },
                    "subject": {
                    "reference": f"Patient/{patientId}"
                    },
                    "effectiveDateTime": curTime,
                    "valueQuantity": {
                    "value": hours,
                    "unit": "hours"
                    }
                },
                "request": {
                    "method": "POST",
                    "url": "Observation"
                }
            }
        ]
    }

    # Send POST request with JSON data
    response = requests.post(g_fhirUrl, json=observationRequest)

    # Check the response status and print the result
    if response.status_code != 200:
        print('Failed to create observation')
        print(f'Status code: {response.status_code}')

# Add a Stress Level entry
def addCaffeineIntake(patientId, cups):

    # Get current time
    curTime = getCurTime()

    # Create the Age, Height, and Weight Observations
    observationRequest = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "resource": {
                    "resourceType": "Observation",
                    "id": "9e2e592e-20f0-47d3-87d4-6097dfbec555",
                    "status": "final",
                    "code": {
                    "text": "Caffeine intake"
                    },
                    "subject": {
                    "reference": f"Patient/{patientId}"
                    },
                    "effectiveDateTime": curTime,
                    "valueQuantity": {
                    "value": cups,
                    "unit": "cups"
                    }
                },
                "request": {
                    "method": "POST",
                    "url": "Observation"
                }
            }
        ]
    }

    # Send POST request with JSON data
    response = requests.post(g_fhirUrl, json=observationRequest)

    # Check the response status and print the result
    if response.status_code != 200:
        print('Failed to create observation')
        print(f'Status code: {response.status_code}')

# Function to recursively find and replace a string in the JSON data
def findAndReplace(data, oldStr, newStr):
    
    if isinstance(data, dict):  # If data is a dictionary
        for key, value in data.items():
            data[key] = findAndReplace(value, oldStr, newStr)
    
    elif isinstance(data, list):  # If data is a list
        for i in range(len(data)):
            data[i] = findAndReplace(data[i], oldStr, newStr)
    
    elif isinstance(data, str):  # If data is a string
        data = data.replace(oldStr, newStr)  # Replace the old string with the new one
    
    return data

# Connect to the FHIR server, waiting until it comes online before returning
def connectToFhirServer(url):

    # Periodically ping the FHIR server until there's a succesful response
    # Check the fhir/metadata endpoint to verify connectivity
    
    # Status code of the request
    status_code = 0

    # Keep sending GET requests until the response code comes back as 200
    while status_code!= 200:

        # Send the request
        try:
            response = requests.get(url)
            status_code = response.status_code
        except Exception as e:
            print('Failed to connect... trying again in 30 seconds')
            status_code = 0
            time.sleep(30)

        # Status code will be 0 if an exception was thrown
        if status_code == 0:

            # Wait 30 seconds before sending another request
            print('Failed to connect... trying again in 30 seconds')
            time.sleep(30)

    print('Connected to FHIR Server')

# Load Patient and Observation data into the FHIR server
def loadData():

    global g_PatientIdCounter

    # Get the folder path
    # NOTE: This Python app must be launched from the 'server' directory 
    #       If not, then the path won't be able to be created
    folder_path = os.path.abspath('data/patients')

    # Load the patients
    for filename in os.listdir(folder_path):

        # Create the file path
        file_path = os.path.join(folder_path, filename)
        
        # Only process JSON files
        if filename.startswith('patient_10') and filename.endswith('.json'):

            # Open the file
            with open(file_path, 'r') as file:
                
                # Load the JSON data
                data = json.load(file)

            # Send POST request with JSON data
            response = requests.post(g_fhirUrl, json=data)

            # Check the response status and print the result
            if response.status_code == 200:
                print(f'{filename} - Successfully loaded patient')

                # Save the Patient ID
                match = re.search(r'/(?P<number>\d+)/', response.json()['entry'][0]['response']['location'])
                patientId = match.group('number')
                name, extension = os.path.splitext(filename)
                g_PatientIds[int(name[8:])] = patientId # Get the non-FHIR Patient ID from the filename 
                # print(response.json())
                g_PatientLogins[("patient_" + name[8:], "password_" + name[8:])] = g_PatientIdCounter
                g_PatientUsernames.append("patient_" + name[8:])
                g_PatientIdCounter += 1
            else:
                print(f'{filename} - Failed to load patient')
                print(f'Status code: {response.status_code}')

    # print(g_PatientIds)

    # Get the folder path
    # NOTE: This Python app must be launched from the 'server' directory 
    #       If not, then the path won't be able to be created
    folder_path = os.path.abspath('data/observations')

    # Load the observations
    for filename in os.listdir(folder_path):

        # Create the file path
        file_path = os.path.join(folder_path, filename)
        
        # Only process JSON files
        if filename.startswith('observations_10') and filename.endswith('.json'):

            # Open the file
            with open(file_path, 'r') as file:
                
                # Load the JSON data
                data = json.load(file)

            # Update the patient references with the correct patient ID
            name, extension = os.path.splitext(filename)
            print(name)
            patientId = int(name[13:]) # Get the non-FHIR Patient ID from the filename 
            findAndReplace(data, ("Patient/" + str(patientId)), ("Patient/" + g_PatientIds[patientId]) )
            # print(data)

            # Send POST request with JSON data
            response = requests.post(g_fhirUrl, json=data)

            # Check the response status and print the result
            if response.status_code == 200:
                print(f'{filename} - Successfully loaded observations')
            else:
                print(f'{filename} - Failed to load observations')
                print(f'Status code: {response.status_code}')

# Attempt to validate login credentials
def login(username, password):

    # If the username/password correlates to an ID, return it
    if (username, password) in g_PatientLogins:
        return g_PatientLogins[(username, password)]
    
    # Else not found, return invalid ID
    else:
        return 0
