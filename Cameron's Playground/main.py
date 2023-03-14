# creating a login page
import kivy
import cv2
# import mysql.connector
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.card import MDCard
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.uix.datatables import MDDataTable
from kivy.clock import Clock
from datetime import date

from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ListProperty,StringProperty, ObjectProperty

from kivy.config import Config

Config.set('graphics', 'resizeable', False)
Config.set('graphics', 'width', 200)

#Builder.load_file('src/menus/home.py')


# different screens
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

# creating the app
class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_tables = None
        
        
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        
        # connecting to the local mysql database
        # note: needed: $ pip install mysql-connector-python
        # mydb = mysql.connector.connect(
        #     host = "localhost", # url of the database
        #     user = "root", # default user
        #     passwd = "www.498SeniorDesign.com", #TODO hide password
        #     database = "users_db"
        #     )
        # create a cursor
        # c = mydb.cursor()

        # create a database
        #c.execute("CREATE DATABASE IF NOT EXISTS users_db") #name of the database if users_db

        # check if database was created
        #c.execute("SHOW DATABASES")
        #for db in c:
            #print(db)
        
        # create table
        # c.execute("""CREATE TABLE if not exists users(
        #     first_name VARCHAR(50),
        #     last_name VARCHAR(50),
        #     email VARCHAR(50),
        #     password VARCHAR(50)
        # )
        # """)

        # commit changes
        # mydb.commit()

        # close connection
        # mydb.close()

        # checking if the database is connected 
        # print(mydb)

    # creating user into the database
    def createuser(self):
        # mydb = mysql.connector.connect(
        #     host = "localhost", # url of the database
        #     user = "root", # default user
        #     passwd = "www.498SeniorDesign.com", #TODO hide password
        #     database = "users_db"
        #     )
        # create a cursor
        # c = mydb.cursor()

        # add first name
        add_first_name = "INSERT INTO users (first_name) VALUES (%s)"
        values = (self.root.ids.first_name.text,)

        # c.execute(add_first_name, values)
        # add messesage
        # add

        # commit changes
        # mydb.commit()

        # close connection
        # mydb.close()


    # checking the user's password
    def checkPass(self):
        # obtaining user's inputs
        email_field = self.ids.email
        passwd_field = self.ids.password

        email = email_field.text
        passwd = passwd_field.text

        # blank error message
        blank_user_pass = self.ids.blank

        if email == " " or passwd == " ":
            blank_user_pass.text = ("[color = #FF0000]User and/or password requried[/color]")
        else:
            print("logged in successfully")

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
        
if __name__ == "__main__":
    MainApp().run()


