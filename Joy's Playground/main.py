### IMPORTS ###
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
from kivy.uix.gridlayout import GridLayout


### SET SCREEN SIZE ###
Config.set('graphics', 'resizeable', False)
Config.set('graphics', 'width', 200) # different screens


### ALL WINDOWS ###
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
        
    # builds gui
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

            # checking database information again user input from text fields
            if patient.val().get("Patient Information",{}).get("email") == email and patient.val().get("Patient Information",{}).get("password") == password:
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


        # connection = sqlite3.connect('test_database.db')
        
        # c = connection.cursor()
        # query= "SELECT * FROM patients WHERE email = ? AND password = ?"
        # c.execute(query, (email, password))
        # patient = c.fetchone()
        # c.close()

        # if patient is not None:
        #     self.root.ids.login_scr.ids.error.text = f'Correct Credentials'
        #     #WindowManager().current = "MainMenuWindow"
            # self.root.current = "main menu"
        #     return email
        # else:
            
        #     self.root.ids.login_scr.ids.email.text == ''
        #     self.root.ids.login_scr.ids.password.text == ''
        #     self.root.ids.login_scr.ids.error.text = f'Incorrect Credentials'
            
        #     return False
             
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
        

    def add_camera(self):
            #adding image to screen
            self.img = Image()
            self.root.ids.camera_scr.ids.camera_layout.add_widget(self.img)
            
            #start video capture
            self.capture = cv2.VideoCapture(0)
            Clock.schedule_interval(self.load_video, 1.0/30.0)
                    
    def load_video(self, *args):
        ret, frame = self.capture.read()
        # Frame initialize
        self.image_frame = frame
        
        #calculate the center of the image
        height, width, _ = self.image_frame.shape
        cx = int (width / 2)
        cy = int (height / 2)
        
        # put dot in center of image
        cv2.circle(self.image_frame, (cx, cy), 3, (255,0,0), 3)
        
        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture
        
        cv2.destroyAllWindows()
            
    def color_analysis(self):
        image_name = "test_picture.png"
                
        # write image to file
        cv2.imwrite(image_name, self.image_frame)        
        
        #compute pixel value at center of captured image
        img = cv2.imread("test_picture.png")
        
        # convert image pixel values to RGB format
        rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # get the size of the image
        height, width, _= img.shape
        
        cx = int(width/2)
        cy = int(height/2)
        
        # select pixel value
        pixel_center = rgb_frame[cy, cx]
        r = pixel_center[0]
        g = pixel_center[1]
        b = pixel_center[2]


        result = None
            
        if g > 200:
            result = "LOW"
        elif g > 175:
            result = "MED"
        elif g > 150:
            result = "HIGH" 
        else:
            result = "Error"

        timestamp = str(date.today())
        test_Results =  timestamp + " " + str(r) + " " + str(g) + " " + str(b) + "\n"
        result = str(r) + " " + str(g) + " " + str(b)
        
        file = open("Test_Results.txt", "a")
        #file.write(test_Results)
        
        file.close()

        return timestamp, result
            
            
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
        timestamp,_ = self.color_analysis()
        antibody = "antibody"
        _, result = self.color_analysis()
        
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
        # self.root.ids.test_results_scr.ids.test.text = f'Incorrect Credentials'
        # Create the labels for each cell in the table
        # for i in range(1, 10):
        #     label = Label(text=str(i))
        #     grid.add_widget(label)

        # return grid
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

            row_data= [
                ({test_number_id}, {date}, {antibody}, {result})
            ]
                # data = test_result.val()
                
                #PRINT FOR TESTING
            # print(data)
            # print(row_data)
            # last_num_row = int(self.data_tables.row_data[-1][0])
            # test=("0", "1", "2", "3")
            self.data_tables.add_row(data)

        # customising test results page with patients full name
        first_name = db.child("Patients").child(clean_email).child("Patient Information").get().val().get("first_name")
        last_name = db.child("Patients").child(clean_email).child("Patient Information").get().val().get("last_name")
        self.root.ids.test_results_scr.ids.title.text = f"{first_name} {last_name}'s Test Results"
        
        # print's all the data from the database for patient
        # for test_result in db.child("Patients").child(clean_email).child("Test Results").get():
            
            # print(test_result.val())
        #     print(test_result.val().get('date'))
        #     print(test_result.val().get('antibody'))
        #     print(test_result.val().get('result'))
        #         #test_label = Label(text=f"Test date: {test_result.get('date')}, Antibody: {test_result.get('antibody')},Result: {test_result.get('result')}")
        #         #self.data_tables.add_row({test_result.get('date')},{test_result.get('antibody')},{test_result.get('result')})
        # self.root.ids.data_scr.ids.data_layout.add_widget(self.data_tables)
        
# runs the app / calls MainApp
if __name__ == "__main__":
    MainApp().run()




