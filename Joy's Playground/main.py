# creating a login page
import kivy
# import mysql.connector
from kivy.lang import Builder
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.card import MDCard
from kivy.properties import ObjectProperty

import sqlite3
import re

### ALL THE WINDOWS ###
# login page
class LoginWindow(Screen):
    pass
# main menu window
class MainMenuWindow(Screen):
    def __init__(self, **kwargs):
        super(MainMenuWindow, self).__init__(**kwargs)
        
        self.add_widget(Label(text='Welcome!'))
# create account window
class CreateAccountWindow(Screen):
    pass
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
    LoginWindow = ObjectProperty(None)
    MainMenuWindow = ObjectProperty(None)
    
#create camera window
class CameraWindow(Screen):
    pass
#create results window
class ResultsWindow(Screen):
    pass
         

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
        
        
        Builder.load_file('main.kv')

        #return WindowManager() 

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
        password = self.root.ids.login_scr.ids.password.text
        connection = sqlite3.connect('test_database.db')
        
        c = connection.cursor()
        query= "SELECT * FROM patients WHERE email = ? AND password = ?"
        c.execute(query, (email, password))
        patient = c.fetchone()
        c.close()

        if patient is not None:
            self.root.ids.login_scr.ids.error.text = f'Correct Credentials'
            WindowManager().current = "MainMenuWindow"
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

            # reload screen
            #print('this section of my code is working')
            #MainApp.root = CreateAccountWindow()
            #MainApp.root.clear_widgets()
            #MainApp.root.add_widget(MainApp.root.build())
        
            return Builder.load_file('main.kv')
        


# runs the app / calls MainApp
if __name__ == "__main__":
    MainApp().run()




