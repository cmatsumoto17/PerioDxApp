### Summary: ###
# DOESN'T WORK IGNORE ME

### Authors: ###
# Camerson Mastumoto
# Joy Niu

### Imports ###
import kivy
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.card import MDCard
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.uix.datatables import MDDataTable
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ListProperty,StringProperty, ObjectProperty
from kivy.config import Config
import cv2
from cryptography.fernet import Fernet
import bcrypt
from datetime import date
import sqlite3
import re
import pyrebase
from kivy.config import Config
from kivy.utils import platform
from kivy.logger import Logger
import os
import numpy as np

### Set Screen Size ###
Config.set('graphics', 'resizeable', False)
Config.set('graphics', 'width', 200) # different screens

### All Classes for Windows and WindowManager ###
class LoginWindow(Screen):
    pass
class MainMenuWindow(Screen):
    def __init__(self, **kwargs):
        super(MainMenuWindow, self).__init__(**kwargs)
        
        self.add_widget(Label(text='Welcome!'))
class CreateAccountWindow(Screen):
    pass
class TestInstructionsWindow(Screen):
    pass 
class CameraWindow(Screen):
    pass
class ResultsWindow(Screen):
    pass
class TestResultsWindow(Screen):
    pass
class WindowManager(ScreenManager):
    LoginWindow = ObjectProperty(None)
    MainMenuWindow = ObjectProperty(None)

class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_tables = None

    def build(self):

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
    
    def login(self):

        # user input from text fields
        email = self.root.ids.login_scr.ids.email.text
        password = self.root.ids.login_scr.ids.password.text

        # database configuration
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

        # reference the databases
        db = firebase.database()

        # temp variable for finding patient
        found_patient = None

        # loops through all the patients in Patient DB
        for patient in db.child("Patients").get().each():
            print(patient.val().get("Patient Information",{}).get("password"))
            # checking database information again user input from text fields
            if patient.val().get("Patient Information",{}).get("email") == email and bcrypt.checkpw(password.encode('utf-8'), patient.val().get("Patient Information",{}).get("password").encode('utf-8')):
                
                found_patient = patient.val()
            # user's information matches
        if found_patient:
            print("login successful")
            self.root.current = "main menu"
            return email
        
        # user's information failed
        else:
            self.root.ids.login_scr.ids.email.text == ''
            self.root.ids.login_scr.ids.password.text == ''
            self.root.ids.login_scr.ids.error.text = f'Incorrect Credentials'
            return False

    def create_account(self):
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

        # reference the databases
        db = firebase.database()

        # variables needed
        # e = self.root.ids.create_account_scr.ids.email.text
        password_pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$" #!Q1w2e3r4 
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        

        # connection = sqlite3.connect('test_database.db')
        # c = connection.cursor()
        # c.execute("SELECT * FROM patients WHERE email=?", (e,))
        # email_exists = c.fetchone()
        # c.close()
        
        
        # empty first or last name
        if(self.root.ids.create_account_scr.ids.first_name.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty first name field'
        elif(self.root.ids.create_account_scr.ids.last_name.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty last name field'
        elif(self.root.ids.create_account_scr.ids.email.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty email address field'
        
        # invalid email address
        elif(not(re.match(email_pattern, self.root.ids.create_account_scr.ids.email.text))):
            self.root.ids.create_account_scr.ids.email.text = ''
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Please enter a valid email address'

        # check if the email exists in the database
        query = db.child("Patients").order_by_child("email").equal_to(self.root.ids.create_account_scr.ids.email.text).get()
        if query.each():
            self.root.ids.create_account_scr.ids.email.text = ''
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Email Already Exists'

        # empty password field
        elif(self.root.ids.create_account_scr.ids.password.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty password field'

        # invalid password
        elif(not(re.match(password_pattern,self.root.ids.create_account_scr.ids.password.text))):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Please enter a password thats a minimum length of 8, at least one uppercase letter, at least one lowercase letter, at least one digit, at least one special character'
        
        # empty password verification field 
        elif(self.root.ids.create_account_scr.ids.password_verification.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty password verification field'
        
        # checking password and password verification
        elif(self.root.ids.create_account_scr.ids.password.text != self.root.ids.create_account_scr.ids.password_verification.text):
            # password don't match error message
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Passwords Do Not Match' 
        
        # create an account
        else:

            # adding patient
            first_name = self.root.ids.create_account_scr.ids.first_name.text
            last_name = self.root.ids.create_account_scr.ids.last_name.text
            email = self.root.ids.create_account_scr.ids.email.text
            password = self.root.ids.create_account_scr.ids.password.text

            # hashing password
            pass_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hash_pass = bcrypt.hashpw(pass_bytes, salt)

            patient_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": hash_pass.decode('utf-8')
            }
            clean_email = email.replace('.', '').replace('@', '')
            db.child("Patients").child(clean_email).child("Patient Information").set(patient_data)
            # c.execute("INSERT INTO patients VALUES(?,?,?,?)",(first_name,last_name,email,password))

            # add a little message
            self.root.ids.create_account_scr.ids.create_account_label.text = f'{first_name} {last_name} Account Created '


            # clear the text fields
            self.root.ids.create_account_scr.ids.first_name.text = ''
            self.root.ids.create_account_scr.ids.last_name.text = ''
            self.root.ids.create_account_scr.ids.email.text = ''
            self.root.ids.create_account_scr.ids.password.text = ''
            self.root.ids.create_account_scr.ids.password_verification.text = ''

            # # commit the changes
            # connection.commit()

            # # close the connections
            # connection.close()

            # reload screen
            #print('this section of my code is working')
            #MainApp.root = CreateAccountWindow()
            #MainApp.root.clear_widgets()
            #MainApp.root.add_widget(MainApp.root.build())
        
        return Builder.load_file('main.kv')
            
    def capture(self):
        camera = self.root.ids.camera_scr.ids['camera']
        img = camera.texture
        
        if img is not None:
            img = img.pixels
            img = np.frombuffer(img, dtype=np.uint8)
            img = img.reshape(camera.texture_size[1], camera.texture_size[0], -1)
            rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # get the size of the image
            height, width, _ = rgb_frame.shape

            cx = int(width / 2)
            cy = int(height / 2)

            # select pixel value
            pixel_center = rgb_frame[cy, cx]
            r = pixel_center[2]
            g = pixel_center[1]
            b = pixel_center[1]

            print(f"RGB values at center: ({r}, {g}, {b})")
            
            concentration = None
            
            if g > 210:
                concentration = "LOW"
            elif g > 170:
                concentration = "MED"
            elif g > 0:
                concentration = "HIGH" 
            else:
                concentration = "Error"
                
            
            timestamp = str(date.today())
            test_Results =  timestamp + " " + concentration + " " + str(r) + " " + str(g) + " " + str(b) + "\n"
            
            
            #INSERT DATA INTO DATABASE
            # create database or connect to one
            # connection = sqlite3.connect('enc_database.db')

            # # create a cursor
            # c = connection.cursor()
            
            # c.execute("INSERT INTO patients VALUES(date,r,g,b)",(timestamp, r, g, b))

            
            #INSERT DATA INTO TXT FILE
            # file = open("Test_Results.txt", "a")
            # file.write(test_Results)
            
            # file.close()
        else:
            print("No image captured")
            
        return timestamp, concentration

    def add_datatable(self):
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

        # reference the databases
        db = firebase.database()

        # obtained variables
        patient = self.login()
        clean_email = patient.replace('.', '').replace('@', '')
        timestamp,_ = self.capture()
        antibody = "antibody"
        _, result = self.capture()
        
        # organize obtained variables into new result
        new_result = {
            "email": patient,
            "date": timestamp,
            "antibody": antibody,
            "result":result
            }
        
        ### creating the correct test result id ###
        test_results = db.child("Patients").child(clean_email).child("Test Results").get()
        if test_results.each():
            last_test_result_id = test_results.each()[-1].key()
            last_number = int(last_test_result_id.split()[-1])
            new_number = last_number + 1
        else:
            new_number = 1
        new_test_result_id = f"Test Result {new_number}"

        # Add the new test result to the Firebase Realtime Database
        
        db.child("Patients").child(clean_email).child("Test Results").child(new_test_result_id).set(new_result)

    def view_results(self):
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

        # reference the databases
        db = firebase.database()

        # obtained variables
        patient = self.login()
        clean_email = patient.replace('.', '').replace('@', '')

        # trying to add a table to the screen
        self.data_tables = MDDataTable(
                size_hint = (0.9, 0.8),
                rows_num = 20,
                column_data = [
                    ("Test Number", dp(30)),
                    ("Date", dp(20)),
                    ("Antibody", dp(20)), 
                    ("Result", dp(20))
                ],)
        self.root.ids.test_results_scr.ids.data_layout.add_widget(self.data_tables)
        
        for test_result in db.child("Patients").child(clean_email).child("Test Results").get():
            test_number_id = test_result.key()
            date = test_result.val().get('date')
            antibody = test_result.val().get('antibody')
            result = test_result.val().get('result')
            data = (test_number_id, date,  antibody, result)
            self.data_tables.add_row(data)

        # customising test results page with patients full name
        first_name = db.child("Patients").child(clean_email).child("Patient Information").get().val().get("first_name")
        last_name = db.child("Patients").child(clean_email).child("Patient Information").get().val().get("last_name")
        self.root.ids.test_results_scr.ids.title.text = f"{first_name} {last_name}'s Test Results"
        
        
# runs the app / calls MainApp
if __name__ == "__main__":
    MainApp().run()
    
        