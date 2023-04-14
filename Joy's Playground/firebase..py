import pyrebase


config = {
    "apiKey": "AIzaSyDg9UeV34LMRRBnvKukniuZZregaDhnrHs",
    "authDomain": "periodxapp.firebaseapp.com",
    "projectId": "periodxapp",
    "storageBucket": "periodxapp.appspot.com",
    "messagingSenderId": "1080188099101",
    "appId": "1:1080188099101:web:981944e07511a572ffc4f4",
    "measurementId": "G-YDJGGTR14X",
    "databaseURL" : "https://periodxapp-default-rtdb.firebaseio.com/"
}

# initializing app
firebase = pyrebase.initialize_app(config)

# reference the database
db = firebase.database()
# results_db = firebase.database()

# data in json
patient_data = {
    "first_name": "Daniel",
    "last_name": "Lee",
    "email":"daniel@email.com",
    "password":"!Q1w2e3r4"
    }
results_data = {
    "email": "daniel@email.com",
    "date":"2023-04-11",
    "antibody": "MM9",
    "result":"low"
    }

user_email="daniel@email.com"
clean_email ="danielemailcom"
password = "!Q1w2e3r4"

# create data
# db.child("Patients").child("Daniel Lee").set(patient_data)
# Generate a new test result ID with the matching naming convention
test_results = db.child("Patients").child(clean_email).child("Test Results").get()
if test_results.each():
    last_test_result_id = test_results.each()[-1].key()
    last_number = int(last_test_result_id.split()[-1])
    new_number = last_number + 1
else:
    new_number = 1
new_test_result_id = f"Test Result {new_number}"

# Add the new test result to the Firebase Realtime Database
db.child("Patients").child(clean_email).child("Test Results").child(new_test_result_id).set(results_data)

# Print the result
print(f"Added new test result '{new_test_result_id}' for user '{clean_email}' with data: {results_data}")

#database.child("Users").child("firstPerson").set(data)

# read data
# query = db.child("Patients").order_by_child("email").equal_to(user_email).get()
# query = db.child("Patients").order_by_child("email").equal_to(user_email).get()

# users = db.child("Patients").get()
# found_user = None
# for patient in users.each():
#     if patient.val()["email"] == user_email and patient.val()["password"] == password:
#         found_user = patient.val()
# if found_user:
#     print("login successful")
# else:
#     print("login failed")
# for patient in query.each():
#     print(patient.val())
#     print(patient.password.get().val())
# if query.each():
#     print("email matches with an existing email")
#     print(query.val().child("password").get())
# else:
#     print("no")
# update data
#database.child("Users").child("firstPerson").update({"Name": "John"})

# remove data
# deleting one value
#database.child("Users").child("firstPerson").child("Age").remove()

# deleting the entire node / person
#database.child("Users").child("firstPerson").remove()