
from kivy.lang import Builder
from kivymd.app import MDApp

import sqlite3

class MainApp(MDApp):
    # builds gui
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        # create database or connect to one
        connection = sqlite3.connect('test_database.db')

        # create a cursor
        c = connection.cursor()

        # create a table
        c.execute(""" CREATE TABLE if not exists patients(
            name text)
            """)

        # commit the changes
        connection.commit()

        # close the connections
        connection.close()

        return Builder.load_file('main.kv')

    # adding data to database
    def submit(self):
        # create database or connect to one
        connection = sqlite3.connect('test_database.db')

        # create a cursor
        c = connection.cursor()

        # adding patient
        c.execute("INSERT INTO patients VALUES(:first)",
            {
                'first':self.root.ids.word_input.text, # id = word_input from kivy
            })

        # add a little message
        self.root.ids.word_label.text = f'{self.root.ids.word_input.text} Added'

        # clear the input box
        self.root.ids.word_input.text = ''

        # commit the changes
        connection.commit()

        # close the connections
        connection.close()

        return Builder.load_file('main.kv')

    # show records from database
    def show_records(self):
        # create database or connect to one
        connection = sqlite3.connect('test_database.db')
        # create a cursor
        c = connection.cursor()

        # grab records from database
        c.execute("SELECT * FROM patients") # * = everything
        records = c.fetchall()
        word = ''
        # loop through records
        for record in records:
            word = f'{word}\n{record[0]}'
            self.root.ids.word_label.text = f'{word}'

        # commit the changes
        connection.commit()

        # close the connections
        connection.close()

MainApp().run()