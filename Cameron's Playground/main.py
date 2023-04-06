
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_tables = None
        
    # builds gui
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"

        # create database or connect to one
        connection = sqlite3.connect('enc_database.db')

        # create a cursor
        c = connection.cursor()

        # create a table
        c.execute(""" CREATE TABLE if not exists patients(
            first_name TEXT,
            last_name TEXT, 
            email TEXT,
            password TEXT,
            salt INTEGER,
            time TEXT,
            r INTEGER,
            g INTEGER, 
            b INTEGER)
            """)

        # commit the changes
        connection.commit()

        # close the connections
        connection.close()
        
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
        email = self.root.ids.login_scr.ids.email.text
        userPassword = self.root.ids.login_scr.ids.password.text
        passwordsMatch = False
        dbpassword = None
        
        #encode entered password to utf-8 bytes
        userBytes = userPassword.encode('utf-8')
        
        #connect to database
        connection = sqlite3.connect('enc_database.db')
        
        c = connection.cursor()
        
        ### CHECKING PASSWORD ###
        #get password stored in database for provided email
        hashq = "SELECT password FROM patients WHERE email = ?"
        c.execute(hashq, (email,))
        
        #return table entry 
        hashq = c.fetchone()     
        print("Hash query")   
        print(hashq)
        
        if hashq is not None:
            #extract password from the table returned
            dbpassword = hashq[0]
            print(dbpassword)
        
            passwordsMatch = bcrypt.checkpw(userBytes, dbpassword)
            print("Password Result after checking hash")
            print(passwordsMatch)
        
        
        #check if email exitst
        query= "SELECT email FROM patients WHERE email = ?"
        c.execute(query, (email,))
        patient = c.fetchone()
        
        
        c.close()

        # if patient is not None and passwordsMatch == True :
        if passwordsMatch == True :
            self.root.ids.login_scr.ids.error.text = f'Correct Credentials'
            self.root.current = "main menu"
            return True
        else:
            
            self.root.ids.login_scr.ids.email.text == ''
            self.root.ids.login_scr.ids.password.text == ''
            self.root.ids.login_scr.ids.error.text = f'Incorrect Credentials'
            
            return False
             

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
        e = self.root.ids.create_account_scr.ids.email.text
        password_pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$" #!Q1w2e3r4 
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        connection = sqlite3.connect('test_database.db')
        c = connection.cursor()
        c.execute("SELECT * FROM patients WHERE email=?", (e,))
        email_exists = c.fetchone()
        c.close()
        
        

        if(self.root.ids.create_account_scr.ids.first_name.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty first name field'
        elif(self.root.ids.create_account_scr.ids.last_name.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty last name field'
        elif(self.root.ids.create_account_scr.ids.email.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty email address field'
        
        elif(not(re.match(email_pattern, self.root.ids.create_account_scr.ids.email.text))):
            self.root.ids.create_account_scr.ids.email.text = ''
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Please enter a valid email address'
        # check if the email exists in the database
        if email_exists:
            self.root.ids.create_account_scr.ids.email.text = ''
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Email Already Exists'
            
            return email_exists[0] 
        
        elif(self.root.ids.create_account_scr.ids.password.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty password field'

        elif(not(re.match(password_pattern,self.root.ids.create_account_scr.ids.password.text))):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Please enter a password thats a minimum length of 8, at least one uppercase letter, at least one lowercase letter, at least one digit, at least one special character'
        elif(self.root.ids.create_account_scr.ids.password_verification.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty password verification field'
        elif(self.root.ids.create_account_scr.ids.password.text != self.root.ids.create_account_scr.ids.password_verification.text):
            # password don't match error message
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Passwords Do Not Match' 
        else:
            print("fucntion is working")
            # create database or connect to one
            connection = sqlite3.connect('enc_database.db')

            # create a cursor
            c = connection.cursor()

            # adding patient
            first_name = self.root.ids.create_account_scr.ids.first_name.text
            last_name = self.root.ids.create_account_scr.ids.last_name.text
            email = self.root.ids.create_account_scr.ids.email.text
            password = self.root.ids.create_account_scr.ids.password.text


            #hashing password
            pass_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hash_pass = bcrypt.hashpw(pass_bytes, salt)
            
            print(salt)
            print(hash_pass)
            
            c.execute("INSERT INTO patients VALUES(?,?,?,?,?)",(first_name, last_name, email, hash_pass, salt))

            # add a little message
            self.root.ids.create_account_scr.ids.create_account_label.text = f'{first_name} {last_name} Account Created '


            # clear the input box
            self.root.ids.create_account_scr.ids.first_name.text = ''
            self.root.ids.create_account_scr.ids.last_name.text = ''
            self.root.ids.create_account_scr.ids.email.text = ''
            self.root.ids.create_account_scr.ids.password.text = ''
            self.root.ids.create_account_scr.ids.password_verification.text = ''

            # commit the changes
            connection.commit()

            # close the connections
            connection.close()

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
        
        concentration = None
        
        if g > 170:
            concentration = "LOW"
        elif g > 85:
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
        file = open("Test_Results.txt", "a")
        file.write(test_Results)
        
        file.close()
        
        
    def add_datatable(self):
        self.data_tables = MDDataTable(
                size_hint = (0.9, 0.8),
                rows_num = 20,
                column_data = [
                    ("Date", dp(20)),
                    ("Result", dp(20))
                    ("R", dp(10)), 
                    ("G", dp(10)),
                    ("B", dp(10)),
                ])
        
        #add rows to table
        with open("Test_Results.txt", 'r') as results_file:
            for line in results_file:
                data = line.split()
                
                #PRINT FOR TESTING
                print(data)
                
                self.data_tables.add_row(data)
                
        results_file.close()
        
        self.root.ids.data_scr.ids.data_layout.add_widget(self.data_tables)
        
        
# runs the app / calls MainApp
if __name__ == "__main__":
    MainApp().run()