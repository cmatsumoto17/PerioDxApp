
import kivy
import sqlite3
import re
import cv2
import os
import numpy as np
import collections.abc

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
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ListProperty,StringProperty, ObjectProperty
from kivy.config import Config
from kivy.utils import platform
from kivy.logger import Logger
#from jnius import autoclass,,k,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
from collections.abc import MutableMapping, Mapping


from cryptography.fernet import Fernet
import bcrypt

from datetime import date

import pyrebase


#give Android permissions
#comment out if running on PC
# from android.permissions import request_permissions, Permission
# from android.storage import app_storage_path
# settings_path = app_storage_path()

# request_permissions([
#     Permission.CAMERA,
#     Permission.WRITE_EXTERNAL_STORAGE,
#     Permission.READ_EXTERNAL_STORAGE
#     Permission.WRITE_INTERNAL_STORAGE,
#     Permission.READ_INTERNAL_STORAGE
# ])

#set screen size
Config.set('graphics', 'resizeable', False)
Config.set('graphics', 'width', 200)# different screens

### Create the classes for each window ###

# login page
class LoginWindow(Screen):
    pass
# main menu window
class MainMenuWindow(Screen):
    pass
# create account window
class CreateAccountWindow(Screen):
    pass
#create test instructions window
class TestInstructionsWindow(Screen):
    pass
#create camera window
class CameraWindow(Screen):
    pass
#create results window
class ResultsWindow(Screen):
    pass
         
# window manager
class WindowManager(ScreenManager):
    pass


### Creates the GUI ###
class MainApp(MDApp):
    test_type = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_tables = None
        
    # builds gui
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"

        
    def check_email_db(self):
        connection = sqlite3.connect('test_database.db')
        c = connection.cursor()
        c.execute("SELECT email FROM patients")
        email_exists = c.fetchone()
        c.close()

        if email_exists:
            self.root.ids.create_account_scr.ids.create_account_label.text = f'This email has been used before'
            return email_exists[0]
        
        else:
            return None

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
            print("login failed")
            return False 
    # def login(self):
    #     email = self.root.ids.login_scr.ids.email.text
    #     userPassword = self.root.ids.login_scr.ids.password.text
    #     passwordsMatch = False
    #     dbpassword = None
        
    #     #encode entered password to utf-8 bytes
    #     userBytes = userPassword.encode('utf-8')
        
    #     #connect to database
    #     connection = sqlite3.connect('enc_database.db')
        
    #     c = connection.cursor()
        
    #     ### CHECKING PASSWORD ###
    #     #get password stored in database for provided email
    #     hashq = "SELECT password FROM patients WHERE email = ?"
    #     c.execute(hashq, (email,))
        
    #     #return table entry 
    #     hashq = c.fetchone()     
    #     print("Hash query")   
    #     print(hashq)
        
    #     if hashq is not None:
    #         #extract password from the table returned
    #         dbpassword = hashq[0]
    #         print(dbpassword)
        
    #         passwordsMatch = bcrypt.checkpw(userBytes, dbpassword)
    #         print("Password Result after checking hash")
    #         print(passwordsMatch)
        
        
    #     #check if email exitst
    #     query= "SELECT email FROM patients WHERE email = ?"
    #     c.execute(query, (email,))
    #     patient = c.fetchone()
        
        
        # c.close()

        # # if patient is not None and passwordsMatch == True :
        # if passwordsMatch == True :
        #     self.root.ids.login_scr.ids.error.text = f'Correct Credentials'
        #     self.root.current = "main menu"
        #     return True
        # else:
            
        #     self.root.ids.login_scr.ids.email.text == ''
        #     self.root.ids.login_scr.ids.password.text == ''
        #     self.root.ids.login_scr.ids.error.text = f'Incorrect Credentials'
            
        #     return False
             

    def check_password(self):
        password_pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if(self.root.ids.create_account_scr.ids.password.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty password field'
            return 0

        elif(self.root.ids.create_account_scr.ids.password_verification.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty password verification field'
            return 0

        elif(re.match(password_pattern,self.root.ids.create_account_scr.ids.password.text)):
            if(self.root.ids.create_account_scr.ids.password.text == self.root.ids.create_account_scr.ids.password_verification.text):
                
                print(self.root.ids.create_account_scr.ids.password.text)
                return self.root.ids.create_account_scr.ids.password.text
                
            else:
                # password don't match error message
                self.root.ids.create_account_scr.ids.create_account_label.text = f'Passwords Do Not Match'
                return 0
            
        else:
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Please enter a password thats a minimum length of 8, at least one uppercase letter, at least one lowercase letter, at least one digit, at least one specicial character'
            return 0
    
    
    def email_exist(self):
        email = self.root.ids.create_account_scr.ids.email.text
        connection = sqlite3.connect('test_database.db')
        c = connection.cursor()
        c.execute("SELECT * FROM patients WHERE email=?", (email,))
        result = c.fetchone()
        c.close()


        # check if the email exists in the database
        if result:
            self.root.ids.create_account_scr.ids.email.text = ''
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Match found'
            
        else:
            self.root.ids.create_account_scr.ids.create_account_label.text = f'No Match found'
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
        print("why aren't you working")

        # clean entered email to remove special character.  Firebase cannot handle these characters
        clean_user_email = self.root.ids.create_account_scr.ids.email.text.replace('.', '').replace('@', '')
        
        account_exists = False
        
        #get patients in database
        patients = db.child("Patients").get()
        
        #check if email exists in database
        for user in patients.each():
            if user.key() == clean_user_email:
                account_exists = True
        
        if account_exists:
            self.root.ids.create_account_scr.ids.email.text = ''
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Email Already Exists'

        # empty first or last name
        elif(self.root.ids.create_account_scr.ids.first_name.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty first name field'
        
        elif(self.root.ids.create_account_scr.ids.last_name.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty last name field'
        
        elif(self.root.ids.create_account_scr.ids.email.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty email address field'
        
        # invalid email address
        elif(not(re.match(email_pattern, self.root.ids.create_account_scr.ids.email.text))):
            self.root.ids.create_account_scr.ids.email.text = ''
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Please enter a valid email address'

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

            results_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": hash_pass.decode('utf-8')
            }
            clean_email = email.replace('.', '').replace('@', '')
            db.child("Patients").child(clean_email).child("Patient Information").set(patient_data)
            db.child("Patients").child(clean_email).child("Test Result").set(results_data)
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
        
            # return Builder.load_file('main.kv')
    
    # def create_account(self):
    #     e = self.root.ids.create_account_scr.ids.email.text
    #     password_pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$" #!Q1w2e3r4 
    #     email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    #     connection = sqlite3.connect('test_database.db')
    #     c = connection.cursor()
    #     c.execute("SELECT * FROM patients WHERE email=?", (e,))
    #     email_exists = c.fetchone()
    #     c.close()
        
        

    #     if(self.root.ids.create_account_scr.ids.first_name.text == ''):
    #         self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty first name field'
    #     elif(self.root.ids.create_account_scr.ids.last_name.text == ''):
    #         self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty last name field'
    #     elif(self.root.ids.create_account_scr.ids.email.text == ''):
    #         self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty email address field'
        
    #     elif(not(re.match(email_pattern, self.root.ids.create_account_scr.ids.email.text))):
    #         self.root.ids.create_account_scr.ids.email.text = ''
    #         self.root.ids.create_account_scr.ids.create_account_label.text = f'Please enter a valid email address'
    #     # check if the email exists in the database
    #     if email_exists:
    #         self.root.ids.create_account_scr.ids.email.text = ''
    #         self.root.ids.create_account_scr.ids.create_account_label.text = f'Email Already Exists'
            
    #         return email_exists[0] 
        
    #     elif(self.root.ids.create_account_scr.ids.password.text == ''):
    #         self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty password field'

    #     elif(not(re.match(password_pattern,self.root.ids.create_account_scr.ids.password.text))):
    #         self.root.ids.create_account_scr.ids.create_account_label.text = f'Please enter a password thats a minimum length of 8, at least one uppercase letter, at least one lowercase letter, at least one digit, at least one special character'
    #     elif(self.root.ids.create_account_scr.ids.password_verification.text == ''):
    #         self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty password verification field'
    #     elif(self.root.ids.create_account_scr.ids.password.text != self.root.ids.create_account_scr.ids.password_verification.text):
    #         # password don't match error message
    #         self.root.ids.create_account_scr.ids.create_account_label.text = f'Passwords Do Not Match' 
    #     else:
    #         print("fucntion is working")
    #         # create database or connect to one
    #         connection = sqlite3.connect('enc_database.db')

    #         # create a cursor
    #         c = connection.cursor()

    #         # adding patient
    #         first_name = self.root.ids.create_account_scr.ids.first_name.text
    #         last_name = self.root.ids.create_account_scr.ids.last_name.text
    #         email = self.root.ids.create_account_scr.ids.email.text
    #         password = self.root.ids.create_account_scr.ids.password.text


    #         #hashing password
    #         pass_bytes = password.encode('utf-8')
    #         salt = bcrypt.gensalt()
    #         hash_pass = bcrypt.hashpw(pass_bytes, salt)
            
    #         print(salt)
    #         print(hash_pass)
            
    #         c.execute("INSERT INTO patients VALUES(?,?,?,?,?)",(first_name, last_name, email, hash_pass, salt))

    #         # add a little message
    #         self.root.ids.create_account_scr.ids.create_account_label.text = f'{first_name} {last_name} Account Created '


    #         # clear the input box
    #         self.root.ids.create_account_scr.ids.first_name.text = ''
    #         self.root.ids.create_account_scr.ids.last_name.text = ''
    #         self.root.ids.create_account_scr.ids.email.text = ''
    #         self.root.ids.create_account_scr.ids.password.text = ''
    #         self.root.ids.create_account_scr.ids.password_verification.text = ''

    #         # commit the changes
    #         connection.commit()

    #         # close the connections
    #         connection.close()

    #         # reload screen
    #         #print('this section of my code is working')
    #         #MainApp.root = CreateAccountWindow()
    #         #MainApp.root.clear_widgets()
    #         #MainApp.root.add_widget(MainApp.root.build())
        
    #         return Builder.load_file('main.kv')
        
        
    def add_camera(self):
        #adding image to screen
        self.img = Image()
        self.root.ids.camera_scr.ids.camera_layout.add_widget(self.img)
        
        #start video capture
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0/30.0)
                
    def print(self):
        print("whaddaup")

    def IL6_test(self):
        self.test_type = "IL-6"
        
    def MMP9_test(self):
        self.test_type = "MMP-9"
        
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
            elif g > 256 or g < 0:
                concentration = "Error"
                
            
            timestamp = str(date.today())
            test_Results =  timestamp + " " + self.test_type + " " + concentration +  "\n"
            
            
            #INSERT DATA INTO DATABASE
            # create database or connect to one
            # connection = sqlite3.connect('enc_database.db')

            # # create a cursor
            # c = connection.cursor()
            
            # c.execute("INSERT INTO patients VALUES(date,r,g,b)",(timestamp, r, g, b))

            
            #INSERT DATA INTO TXT FILE
            file = open("Test_Results.txt", "a")
            file.write(test_Results)
            
            file.close()
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

        
        
        # # create database or connect to one
        # connection = sqlite3.connect('test_database.db')

        # # create a cursor
        # c = connection.cursor()

        # # create a patients table
        # c.execute(""" CREATE TABLE if not exists test_results(
        #     patient TEXT,
        #     date TEXT,
        #     antibody TEXT,
        #     result TEXT)
        #     """)
        
        # # adding test results
        # patient = self.login()
        # timestamp,_ = self.color_analysis()
        # antibody = "antibody"
        # _, result = self.color_analysis()
        # c.execute("INSERT INTO test_results VALUES(?,?,?,?)",(patient,timestamp,antibody,result))
        

        # # commit the changes
        # connection.commit()

        # # close the connections
        # connection.close()

        # self.data_tables = MDDataTable(
        #         size_hint = (0.9, 0.8),
        #         rows_num = 20,
        #         column_data = [
        #             ("Date", dp(20)),
        #             ("R", dp(10)), 
        #             ("G", dp(10)),
        #             ("B", dp(10)),
        #         ])
        
        # #add rows to table
        # with open("Test_Results.txt", 'r') as results_file:
        #     for line in results_file:
        #         data = line.split()
                
        #         #PRINT FOR TESTING
        #         print(data)
                
        #         self.data_tables.add_row(data)
                
        # results_file.close()
        
        # self.root.ids.data_scr.ids.data_layout.add_widget(self.data_tables) 
    # def add_datatable(self):
    #     self.data_tables = MDDataTable(
    #             size_hint = (0.9, 0.8),
    #             rows_num = 20,
    #             column_data = [
    #                 ("Date", dp(20)),
    #                 ("Result", dp(20)),
    #                 ("R", dp(10)), 
    #                 ("G", dp(10)),
    #                 ("B", dp(10)),
    #             ])
        
    #     #add rows to table
    #     with open("Test_Results.txt", 'r') as results_file:
    #         for line in results_file:
    #             data = line.split()
                
    #             #PRINT FOR TESTING
    #             print(data)
                
    #             self.data_tables.add_row(data)
                
    #     results_file.close()
        
    #     self.root.ids.data_scr.ids.data_layout.add_widget(self.data_tables)
        
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

        # Define the properties of the table
        # grid = GridLayout(cols=3, rows=3, size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        # self.root.ids.data_scr.ids.test.text = f'Incorrect Credentials'
        # Create the labels for each cell in the table
        # for i in range(1, 10):
        #     label = Label(text=str(i))
        #     grid.add_widget(label)

        # return grid


        # customising test results page with patients full name
        first_name = db.child("Patients").child(clean_email).child("Patient Information").get().val().get("first_name")
        last_name = db.child("Patients").child(clean_email).child("Patient Information").get().val().get("last_name")
        self.root.ids.data_scr.ids.title.text = f"{first_name} {last_name}'s Test Results"

        # testing to see about empty data tables
        test_results = db.child("Patients").child(clean_email).get().val()
        
        if "Test Results" not in test_results:
            self.root.ids.data_scr.ids.no_results.text = f"No Test Results Yet"
        else:
            self.root.ids.data_scr.ids.no_results.text = f""
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
            self.root.ids.data_scr.ids.data_layout.add_widget(self.data_tables)
        
            for test_result in db.child("Patients").child(clean_email).child("Test Results").get():
                test_number_id = test_result.key()
                date = test_result.val().get('date')
                antibody = test_result.val().get('antibody')
                result = test_result.val().get('result')
                data = (test_number_id, date,  antibody, result)
                

            # row_data= [
            #     ({test_number_id}, {date}, {antibody}, {result})
            # ]
                # data = test_result.val()
                
                #PRINT FOR TESTING
            # print(data)
            # print(row_data)
            # last_num_row = int(self.data_tables.row_data[-1][0])
            # test=("0", "1", "2", "3")
            self.data_tables.add_row(data)

            
# runs the app / calls MainApp
if __name__ == "__main__":
    MainApp().run()