import mysql.connector
import kivy
from kivy.app import App

from tkinter import filedialog

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput

n=1
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(name, year, genre,asubject, developer, publisher, logo):
    print("Inserting BLOB into python_employee table")
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='games',
                                             user='Lorenc',
                                             password='SAhara137797!')

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO games
                          (name, year, genre,subject, developer,publisher,logo) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        sql_update_blob_query = """ INSERT INTO games
                          (year, genre,subject, developer,publisher,logo) VALUES (%s,%s,%s,%s,%s,%s) Where name=%s"""


        empPicture = convertToBinaryData(logo)

        # Convert data into tuple format


        insert_blob_tuple = (name, year, genre, asubject, developer, publisher, empPicture)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into games table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

#insertBLOB("Far Cry 3", "2012", "FPS", "Ubisoft", "Ubisoft",r"C:\Users\a.lorenc\Downloads\FarCry3.jpg")

# Press the green button in the gutter to run the script.

def callback(instance):
    global n
    print('The button <%s> is being pressed' % instance.text)
    n=n+1

class AllGamesView(ScrollView):
    list_of_games=["Assasins Creed","Far Cry","Splinter Cell","Anno"]
    def __init__(self, **kwargs):
        super(AllGamesView, self).__init__(**kwargs)

        #self.pos_hint = {'center_x': 0.5, 'top': 1}

        stack=StackLayout()
        stack.bind(height=stack.setter('height'))
        stack.spacing=[10,10]
        for game in self.list_of_games:
            stack.add_widget(Button(text=game, size_hint=[None, None],size=(150,150)))
            stack.add_widget(Button(text=game, size_hint=[None, None],size=(150,150)))
            stack.add_widget(Button(text=game, size_hint=[None, None],size=(150,150)))
            stack.add_widget(Button(text=game, size_hint=[None, None],size=(150,150)))
            stack.add_widget(Button(text=game, size_hint=[None, None],size=(150,150)))
            stack.add_widget(Button(text=game, size_hint=[None, None],size=(150,150)))
            stack.add_widget(Button(text=game, size_hint=[None, None],size=(150,150)))
            stack.add_widget(Button(text=game, size_hint=[None, None],size=(150,150)))


        stack.orientation="lr-tb"
        stack.size_hint = [1,None]
        #stack.height=stack.minimum_height
        stack.bind(minimum_height = stack.setter("height"))
        self.add_widget(stack)
        print(stack.minimum_height)
        print(self.height)
class AllGamesView2(StackLayout):
    list_of_games=["Assasins Creed","Far Cry","Splinter Cell","Anno"]
    def __init__(self, **kwargs):
        super(AllGamesView2, self).__init__(**kwargs)

        self.spacing=[10,10]
        for game in self.list_of_games:
            self.add_widget(Button(text=game, size_hint=[0.125, 0.125]))
            self.add_widget(Button(text=game, size_hint=[0.125, 0.125]))
            self.add_widget(Button(text=game, size_hint=[0.125, 0.125]))
            self.add_widget(Button(text=game, size_hint=[0.125, 0.125]))
            self.add_widget(Button(text=game, size_hint=[0.125, 0.125]))
            self.add_widget(Button(text=game, size_hint=[0.125, 0.125]))
            self.add_widget(Button(text=game, size_hint=[0.125, 0.125]))
            self.add_widget(Button(text=game, size_hint=[0.25, 0.25]))


class MainView(AnchorLayout):
    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        self.add_widget(Label(text="Game Selector",color=[1,1,0,1],font_size=40,pos=[0.5,0]))

class LookupView(GridLayout):
    def __init__(self, **kwargs):
        super(LookupView, self).__init__(**kwargs)
        self.cols = 2
        boxlayout=BoxLayout(size_hint=[0.5,1]) #lista cech
        boxlayout.orientation="vertical"
        anchor=AnchorLayout() #obrazek
        boxlayout.add_widget(Label(text='Nazwa Gry'))
        boxlayout.add_widget(Label(text='Rok Produkcji'))
        boxlayout.add_widget(Label(text='Gatunek'))
        boxlayout.add_widget(Label(text='Teamtyka'))
        boxlayout.add_widget(Label(text='Deweloper'))
        boxlayout.add_widget(Label(text='Wydawca'))

        anchor.add_widget(Button(text="test"))
        self.add_widget(boxlayout)
        self.add_widget(anchor)
        ##przyciski: usuń, losuj, wróć


class AddView(GridLayout):
    def __init__(self, **kwargs):
        super(AddView, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Nazwa Gry'))
        self.add_widget(Label(text='Rok Produkcji'))
        self.add_widget(TextInput(multiline=True,size_hint=(0.5,0.5)))
        self.add_widget(TextInput(multiline=False))
        self.add_widget(Label(text='Gatunek'))
        self.add_widget(Label(text='Teamtyka'))
        self.add_widget(TextInput(multiline=False))
        self.add_widget(TextInput(multiline=False))
        self.add_widget(Label(text='Deweloper'))
        self.add_widget(Label(text='Wydawca'))
        self.add_widget(TextInput(multiline=False))
        self.add_widget(TextInput(multiline=False))
        #self.add_widget(Label(text='Okładka'))
        self.add_widget(Button(text='Wybierz okładkę',on_press=callback))

        #self.add_widget(Label())
        grid=GridLayout()
        grid.cols=2
        grid.add_widget(Button(text='Zapisz',on_press=callback))
        grid.add_widget(Button(text='Wyczyść',on_press=callback))
        self.add_widget(grid)


class MyApp(App):

    def build(self):
        self.title = 'Game Selector'
        #return AddView()
        #return AllGamesView()
        #return MainView()
        #return LookupView()
        self.screen_manager = ScreenManager()
        '''Creation of login screen'''
        self.login_page = AllGamesView()
        screen = Screen(name='Login')
        screen.add_widget(self.login_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == '__main__':
    MyApp().run()
#Valid properties are ['anchors', 'base_direction', 'bold', 'center', 'center_x', 'center_y', 'children', 'cls', 'color',
# 'disabled', 'disabled_color', 'disabled_outline_color', 'ellipsis_options', 'font_blended', 'font_context', 'font_family',
# 'font_features', 'font_hinting', 'font_kerning', 'font_name', 'font_size', 'halign', 'height', 'ids', 'is_shortened',
# 'italic', 'line_height', 'markup', 'max_lines', 'mipmap', 'motion_filter', 'opacity', 'outline_color', 'outline_width',
# 'padding', 'padding_x', 'padding_y', 'parent', 'pos', 'pos_hint', 'refs', 'right', 'shorten', 'shorten_from', 'size',
# 'size_hint', 'size_hint_max', 'size_hint_max_x', 'size_hint_max_y', 'size_hint_min', 'size_hint_min_x', 'size_hint_min_y',
# 'size_hint_x', 'size_hint_y', 'split_str', 'strikethrough', 'strip', 'text', 'text_language', 'text_size', 'texture',
# 'texture_size', 'top', 'underline', 'unicode_errors', 'valign', 'width', 'x', 'y']
    # logo = filedialog.askopenfilename()
