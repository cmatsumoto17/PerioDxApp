
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
        connection = sqlite3.connect('test_database.db')

        # create a cursor
        c = connection.cursor()

        # create a table
        c.execute(""" CREATE TABLE if not exists patients(
            first_name TEXT,
            last_name TEXT, 
            email TEXT,
            password TEXT)
            """)

        # commit the changes
        connection.commit()

        # close the connections
        connection.close()
        
# Builder.load_file('main.kv')

    def check_email(self):
        # check email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if(self.root.ids.create_account_scr.ids.email.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty email address text field'
            return 0
        elif(email_pattern != self.root.ids.create_account_scr.ids.email.text):
        
            # validity email error message
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Please enter a valid email address'
            return 0

        #TODO check if the email exists in the database
        else:
            return self.root.ids.create_account_scr.ids.email.text
            

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

    def create_account(self):
        password_pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        
        if(self.root.ids.create_account_scr.ids.first_name.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty first name field'
        elif(self.root.ids.create_account_scr.ids.last_name.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty last name field'
        elif(self.root.ids.create_account_scr.ids.email.text == ''):
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Empty email address field'
        
        
        
        elif(not(re.match(email_pattern, self.root.ids.create_account_scr.ids.email.text))):
            self.root.ids.create_account_scr.ids.email.text = ''
            self.root.ids.create_account_scr.ids.create_account_label.text = f'Please enter a valid email address'
        #TODO check if the email exists in the database
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
            # create database or connect to one
            connection = sqlite3.connect('test_database.db')

            # create a cursor
            c = connection.cursor()

            # adding patient
            first_name = self.root.ids.create_account_scr.ids.first_name.text
            last_name = self.root.ids.create_account_scr.ids.last_name.text
            email = self.root.ids.create_account_scr.ids.email.text
            password = self.root.ids.create_account_scr.ids.password.text
            c.execute("INSERT INTO patients VALUES(?,?,?,?)",(first_name,last_name,email,password))

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
            
            self.root.current = "main menu"
            
            
        
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
        
        timestamp = str(date.today())
        test_Results =  timestamp + " " + str(r) + " " + str(g) + " " + str(b) + "\n"
        
        file = open("Test_Results.txt", "a")
        file.write(test_Results)
        
        file.close()
        
        
    def add_datatable(self):
        self.data_tables = MDDataTable(
                size_hint = (0.9, 0.8),
                rows_num = 20,
                column_data = [
                    ("Date", dp(20)),
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