import cProfile
import io
import pstats
import random
import threading
from io import BytesIO
from os.path import exists

import mysql.connector
from kivy import Config
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color, Line
from kivy.properties import NumericProperty, Clock
from kivy.properties import OptionProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput

All_games=[]
All_games_backup=[]
class Game:
    def __init__(self, name, year, genre, subject, rating, developer, publisher, logo=None):
        self.name=name
        self.year=year
        self.genre=genre
        self.subject=subject
        self.rating=rating
        self.developer=developer
        self.publisher=publisher
        self.logo=logo


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData
def convertToJpeg(img):
    data = io.BytesIO(img)
    img = CoreImage(data, ext="bmp").texture
    return img

class DBconnection:
    def __init__(self):
       self.connection = mysql.connector.connect(host='localhost',
                                             database='games',
                                             user='Lorenc',
                                             password='SAhara137797!')
       self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()
        self.cursor.close()
    def getGamesByTitle(self,title):
        print("Fetching games by title")
        try:
            All_games.clear()
            if(title==""):
               All_games.extend(All_games_backup.copy())
            else:
                for game in All_games_backup:
                    if title.lower() in game.name.lower():
                        All_games.append(game)
            print("Succesfully fetched games by title")
        except Exception as e:
            print(e)
            print("error trying to get games by title")
    def getGamesByGenre(self,genre):
        print("Fetching games by genre")
        try:
            All_games.clear()
            if(genre==""):
               All_games.extend(All_games_backup.copy())
            else:
                for game in All_games_backup:
                    if genre.lower() in game.genre.lower():
                        All_games.append(game)
            print("Succesfully fetched games by genre")
        except Exception as e:
            print(e)
            print("error trying to get games by genre")
    def getGamesByRating(self,rating):
        print("Fetching games by rating")
        try:
            All_games.clear()
            if(rating==""):
               All_games.extend(All_games_backup.copy())
            else:
                for game in All_games_backup:
                    if rating == game.rating:
                        All_games.append(game)
            print("Succesfully fetched games by rating")
        except Exception as e:
            print(e)
            print("error trying to get games by rating")
    def getGamesByYear(self,year):
        print("Fetching games by year")
        try:
            All_games.clear()
            if(year==""):
               All_games.extend(All_games_backup.copy())
            else:
                for game in All_games_backup:
                    if year == game.year:
                        All_games.append(game)
            print("Succesfully fetched games by year")
        except Exception as e:
            print(e)
            print("error trying to get games by year")
    def getGamesBySubject(self,Subject):
        print("Fetching games by tags")
        try:
            All_games.clear()
            if(Subject==""):
               All_games.extend(All_games_backup.copy())
            else:
                for game in All_games_backup:
                    if Subject.lower() in game.subject.lower():
                        All_games.append(game)
            print("Succesfully fetched games by tags")
        except Exception as e:
            print(e)
            print("error trying to get games by tags")
    def getGamesByDeveloper(self,developer):
        print("Fetching games by developer")
        try:
            All_games.clear()
            if(developer==""):
               All_games.extend(All_games_backup.copy())
            else:
                for game in All_games_backup:
                    if developer.lower() in game.developer.lower():
                        All_games.append(game)
            print("Succesfully fetched games by this developer")
        except Exception as e:
            print(e)
            print("error trying to get games from this developer")
    def getGamesByPublisher(self,publisher):
        print("Fetching games by publisher")
        try:
            All_games.clear()
            if(publisher==""):
               All_games.extend(All_games_backup.copy())
            else:
                for game in All_games_backup:
                    if publisher.lower() in game.publisher.lower():
                        All_games.append(game)
            print("Succesfully fetched games by this publisher")
        except Exception as e:
            print(e)
            print("error trying to get games from this publisher")
    def getAllGames(self):
        print("Fetching all games")
        try:
            query = """SELECT * FROM games.games"""
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            for game in result:
                All_games.append(Game(*game))
            All_games_backup.extend(All_games.copy())
            print("Succesfully fetched all data")
        except Exception as e:
            print(e)
            print("error trying to get all games")
    # def getRandomGame(self):
    #     print("Fetching random game")
    #     try:
    #         query = """SELECT * FROM games.games ORDER BY RAND() LIMIT 1"""
    #         self.cursor.execute(query)
    #         result = self.cursor.fetchall()
    #         for game in result:
    #             All_games.append(Game(*game))
    #         print("Succesfully fetched all data")
    #     except Exception as e:
    #         print(e)
    #         print("error trying to get random game")
    def insertBLOB(self, name, year, genre, asubject, rating, developer, publisher, logo):
        print("Adding new game to DB")
        try:

            sql_insert_blob_query = """ INSERT INTO games
                              (name, year, genre,subject,rating, developer,publisher,logo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                              ON DUPLICATE KEY UPDATE name=VALUES(name),year=VALUES(year),genre=VALUES(genre),
                              subject=VALUES(subject),rating=VALUES(rating),developer=VALUES(developer),
                              publisher=VALUES(publisher),logo=VALUES(logo)"""
            sql_update_blob_query = """ INSERT INTO games
                              (year, genre,subject,rating, developer,publisher,logo) VALUES (%s,%s,%s,%s,%s,%s,%s) Where name=%s"""

            empPicture = convertToBinaryData(logo)

            # Convert data into tuple format

            insert_blob_tuple = (name, year, genre, asubject, rating, developer, publisher, empPicture)
            result = self.cursor.execute(sql_insert_blob_query, insert_blob_tuple)
            self.connection.commit()
            print("Succesfully inserted data into DB: ", result)

            pop = popupSuccesfullInsert()
            pop.open()
            return True

        except mysql.connector.Error as error:
            print("Failed inserting data into MySQL table {}".format(error))

        finally:
            if self.connection.is_connected():

                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")


class AllGamesView(BoxLayout):
    def __init__(self, **kwargs):
        super(AllGamesView, self).__init__(**kwargs)
        self.orientation="vertical"
        navbar=BoxLayout(height=200,size_hint=[1, 0.1])
        navbar.orientation="horizontal"
        navbar.add_widget(Button(text="<-", on_press=self.wstecz,size_hint=[0.5, 1]))
        navbar.add_widget(Button(text="->", on_press=self.wprzód, size_hint=[0.5, 1]))


        self.add_widget(navbar)
        scroll=ScrollView()
        stack=StackLayout()
        stack.bind(height=stack.setter('height'))
        stack.spacing=[10, 10]
        for game in All_games:
            stack.add_widget(ImageButton(size_hint=[None, None], size=(375, 375), texture=convertToJpeg(game.logo),
                                         allow_stretch=True,name=game.name,year=game.year,genre=game.genre,subject=game.subject,
                                         rating=game.rating,developer=game.developer,publisher=game.publisher))


        stack.orientation="lr-tb"
        stack.size_hint = [1,None]
        #stack.height=stack.minimum_height
        stack.bind(minimum_height = stack.setter("height"))
        scroll.add_widget(stack)
        self.add_widget(scroll)
    def wstecz(self,obj):
        app.screen_manager.current = "Add"
    def wprzód(self,obj):
        app.screen_manager.current = "Lookup"
    def imageClick(self,obj,game):
        print(game.name)
class ImageButton(ButtonBehavior, Image,Game):
    def on_press(self):
        print (LookupView.counter)
        LookupView.counter=1
        app.screen_manager.current = "Lookup"
class MainView(FloatLayout):

    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        with self.canvas:
            self.bg = Rectangle(source='omage.png', pos=self.pos, size=self.size)
        self.bind(pos=self.update_backgroundg)
        self.bind(size=self.update_backgroundg)

        anchor_top = AnchorLayout(pos_hint={'x':0, 'y':.35})
        box_middle = BoxLayout(pos_hint={'x':0, 'y':.3})
        anchor_top.add_widget(Label(text="Game Selector",color=[0,1,0,1],font_size=40,pos=[0.5,0]))
        box_middle.add_widget(Button(text="Dodaj Grę",size_hint=[0.2,0.2],on_press=self.transition1,font_size=20,
                                     background_color =[0.1, 0.7, 1, 1]))
        box_middle.add_widget(Button(text="Przeglądaj gry",size_hint=[0.2,0.2],on_press=self.transition2,font_size=20,
                                     background_color =[0.1, 0.7, 1, 1]))
        box_middle.add_widget(Button(text="Wybór Tytułu",size_hint=[0.2,0.2],on_press=self.transition3,font_size=20,
                                     background_color =[0.1, 0.7, 1, 1]))
        self.add_widget(box_middle)
        self.add_widget(anchor_top)
    def transition1(self,obj):
        app.screen_manager.current="Add"
    def transition2(self,obj):

        app.screen_manager.current="AllGames"
    def transition3(self,obj):
        app.screen_manager.current="Lookup"
    def update_backgroundg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

class LookupView(GridLayout):

    counter=0

    def __init__(self, **kwargs):
        super(LookupView, self).__init__(**kwargs)
        # dbconnector=DBconnection()
        # dbconnector.getAllGames()
        random.shuffle(All_games)
        self.cols = 1
        x = random.choices(range(0, len(All_games)), k=1)
        LookupView.counter=x[0]
        game = All_games[LookupView.counter]
        menubar = BoxLayout(height=200, size_hint=[1, 0.05])
        menubar.orientation="horizontal"
        menubar.add_widget(Button(text="Menu główne",on_press=self.backToMainMenu, size_hint=[0.33, 1]))
        menubar.add_widget(Button(text="Tytuł", on_release=self.filterByTitle, size_hint=[0.33, 1]))
        menubar.add_widget(Button(text="Rok wydania", on_release=self.filterByYear, size_hint=[0.33, 1]))
        menubar.add_widget(Button(text="Gatunek", on_release=self.filterByGenre, size_hint=[0.33, 1]))
        menubar.add_widget(Button(text="Tagi", on_release=self.filterBySubject, size_hint=[0.33, 1]))
        menubar.add_widget(Button(text="Ocena", on_release=self.filterByRating, size_hint=[0.33, 1]))
        menubar.add_widget(Button(text="Deweloper", on_release=self.filterByDeveloper, size_hint=[0.33, 1]))
        menubar.add_widget(Button(text="Wydawca", on_release=self.filterByPublisher, size_hint=[0.33, 1]))
        self.add_widget(menubar)
        navbar=BoxLayout(height=200,size_hint=[1, 0.05])
        navbar.orientation="horizontal"
        navbar.add_widget(Button(text="<-", on_release=self.previous, size_hint=[0.33, 1]))
        navbar.add_widget(Button(text="Random", on_release=self.random, size_hint=[0.34, 1]))
        navbar.add_widget(Button(text="->", on_release=self.next, size_hint=[0.33, 1]))
        self.add_widget(navbar)

        grid=GridLayout(cols=2)
        boxlayout=BoxLayout(size_hint=[0.3,1]) #lista cech
        boxlayout.orientation="vertical"
        anchor=AnchorLayout() #obrazek

        self.labelName=Button(background_color=[15/255,252/255,3/255,1],
                                 background_normal='',color=[0,0,0,1],halign="center",font_size='20sp')
        self.labelName.text_size = [self.labelName.width*2, None]
        boxlayout.add_widget(self.labelName)
        self.labelYear=Button(background_color=[217/255,28/255,56/255,1],
                                 background_normal='',color=[0,0,0,1],halign="center",font_size='20sp')
        self.labelYear.text_size = [self.labelYear.width*2, None]
        boxlayout.add_widget(self.labelYear)
        self.labelGenre=Button(background_color=[15/255,252/255,3/255,1],
                                 background_normal='',color=[0,0,0,1],halign="center",font_size='20sp')
        self.labelGenre.text_size = [self.labelGenre.width*2, None]
        boxlayout.add_widget(self.labelGenre)
        self.labelSubject=Button(background_color=[217/255,28/255,56/255,1],
                                 background_normal='',color=[0,0,0,1],halign="center",font_size='20sp')
        self.labelSubject.text_size=[self.labelSubject.width*3,None]

        boxlayout.add_widget(self.labelSubject)
        self.labelRating=Button(background_color=[15/255,252/255,3/255,1],
                                 background_normal='',color=[0,0,0,1],halign="center",font_size='20sp')
        self.labelRating.text_size = [self.labelRating.width*2, None]
        boxlayout.add_widget(self.labelRating)
        self.labelDeveloper=Button(background_color=[217/255,28/255,56/255,1],
                                 background_normal='',color=[0,0,0,1],halign="center",font_size='20sp')
        self.labelDeveloper.text_size = [self.labelDeveloper.width*2, None]
        boxlayout.add_widget(self.labelDeveloper)
        self.labelPublisher=Button(background_color=[15/255,252/255,3/255,1],
                                 background_normal='',color=[0,0,0,1],halign="center",font_size='20sp')
        self.labelPublisher.text_size = [self.labelPublisher.width*2, None]
        boxlayout.add_widget(self.labelPublisher)

        data = io.BytesIO(game.logo)
        img=CoreImage(data, ext="jpeg").texture
        self.new_img = Image()
        self.new_img.texture = img
        self.new_img.allow_stretch=True
        self.labelName.text=game.name
        self.labelPublisher.text=game.publisher
        self.labelDeveloper.text=game.developer
        self.labelRating.text = "Ocena: " + game.rating + "/10" if game.rating else "Brak Oceny"
        self.labelSubject.text=game.subject.replace(",", ", ")
        self.labelGenre.text=game.genre
        self.labelYear.text=game.year
        self.new_img.texture = img
        if(exists(game.name.lower()+'.mp3')):
            sound = SoundLoader.load(game.name.lower()+'.mp3')
            if sound:
                sound.loop=True
                sound.play()
        #anchor.add_widget(self.new_img)
        grid.add_widget(boxlayout)
        grid.add_widget(self.new_img)
        grid.padding=[5,5,5,5]
        self.add_widget(grid)

    def backToMainMenu(self,obj):
        app.screen_manager.current = "Main"
    def filterByTitle(self,obj):
        pop=popupTitle()
        self.counter=0
        pop.open()
    def filterByYear(self,obj):
        pop=popupYear()
        self.counter=0
        pop.open()
    def filterByRating(self,obj):
        pop=popupRating()
        self.counter=0
        pop.open()
    def filterByGenre(self,obj):
        pop=popupGenre()
        self.counter=0
        pop.open()
    def filterBySubject(self,obj):
        pop=popupSubject()
        self.counter=0
        pop.open()
    def filterByDeveloper(self,obj):
        pop=popupDeveloper()
        self.counter=0
        pop.open()
    def filterByPublisher(self,obj):
        pop=popupPublisher()
        self.counter=0
        pop.open()
    def previous(self,obj):
        if(len(All_games)<1): return
        LookupView.counter-=1
        if (LookupView.counter < 0): LookupView.counter = len(All_games)-1
        game=All_games[LookupView.counter]
        self.labelName.text=game.name
        self.labelPublisher.text=game.publisher
        self.labelDeveloper.text=game.developer
        self.labelRating.text = "Ocena: " + game.rating + "/10" if game.rating else "Brak Oceny"
        self.labelSubject.text=game.subject.replace(",", ", ")
        self.labelGenre.text=game.genre
        self.labelYear.text=game.year
        data = io.BytesIO(game.logo)
        img=CoreImage(data, ext="jpeg").texture
        self.new_img.texture = img
        if(exists(game.name.lower()+'.mp3')):
            print("zanlazł ale nie odtwarza")
            sound = SoundLoader.load(game.name.lower()+'.mp3')
            if sound:
                sound.loop=True
                sound.play()
    def next(self,obj):
        if (len(All_games) < 1): return
        LookupView.counter+=1
        if (LookupView.counter >= len(All_games)): LookupView.counter = 0
        game = All_games[LookupView.counter]
        self.labelName.text=game.name
        self.labelPublisher.text=game.publisher
        self.labelDeveloper.text=game.developer
        self.labelRating.text = "Ocena: " + game.rating + "/10" if game.rating else "Brak Oceny"
        self.labelSubject.text=game.subject.replace(",", ", ")
        self.labelGenre.text=game.genre
        self.labelYear.text=game.year
        data = io.BytesIO(game.logo)
        img=CoreImage(data, ext="jpeg").texture
        self.new_img.texture = img
        if(exists(game.name.lower()+'.mp3')):
            sound = SoundLoader.load(game.name.lower()+'.mp3')
            if sound:
                sound.loop=True
                sound.play()
    def random(self,obj):
        if (len(All_games) < 1): return
        x = random.choices(range(0, len(All_games)), k=1)
        self.counter=x[0]
        game = All_games[self.counter]
        self.labelName.text=game.name
        self.labelPublisher.text=game.publisher
        self.labelDeveloper.text=game.developer
        self.labelRating.text = "Ocena: " + game.rating + "/10" if game.rating else "Brak Oceny"
        self.labelSubject.text=game.subject.replace(",", ", ")
        self.labelGenre.text=game.genre
        self.labelYear.text=game.year
        data = io.BytesIO(game.logo)
        img=CoreImage(data, ext="jpeg").texture
        self.new_img.texture = img

class AddView(GridLayout,DBconnection):
    def __init__(self, **kwargs):
        super(AddView, self).__init__(**kwargs)
        self.cols = 2
        Window.clearcolor=(21/255,149/255,234/255,1)
        self.add_widget(Label(text='Nazwa Gry'))
        self.add_widget(Label(text='Rok Produkcji'))
        self.input1=TextInput(multiline=True, write_tab=False)
        self.add_widget(self.input1)
        self.input2 = TextInput(multiline=False, write_tab=False)
        self.add_widget(self.input2)
        self.add_widget(Label(text='Gatunek'))
        self.add_widget(Label(text='Tematyka'))
        self.input3=TextInput(multiline=False, write_tab=False)
        self.add_widget(self.input3)
        self.input4=TextInput(multiline=False, write_tab=False)
        self.add_widget(self.input4)
        self.add_widget(Label(text='Ocena'))
        self.add_widget(Label(text='Deweloper'))

        self.input5=TextInput(multiline=False, write_tab=False)
        self.add_widget(self.input5)
        self.input6=TextInput(multiline=False, write_tab=False)
        self.add_widget(self.input6)
        self.add_widget(Label(text='Wydawca'))
        self.add_widget(Label(text='Okładka'))
        self.input7=TextInput(multiline=False, write_tab=False)
        self.add_widget(self.input7)
        grid=GridLayout()
        grid.cols=2
        self.input8 = TextInput(multiline=True, write_tab=False)
        grid.add_widget(self.input8)
        grid.add_widget(Button(text='Wybierz okładkę',background_normal='',
                               background_color=[217/255,28/255,56/255,1]))
        self.add_widget(grid)

        #self.fileChooser = fileChooser = FileChooserIconView(size_hint_y=None)
        # grid=GridLayout()
        # grid.cols=2
        self.add_widget(Button(text='Zapisz',on_release=self.submit))
        self.add_widget(Button(text='Anuluj', on_release=self.clear))
        #self.add_widget(grid)

    def submit(self,obj):
        #print(self.input1.text+self.input2.text+self.input3.text+self.input4.text+self.input5.text+self.input6.text)
        if(self.input1.text and self.input2.text and self.input3.text and self.input4.text and
                self.input6.text and self.input7.text and self.input8.text):
            dbconnector = DBconnection()
            result=dbconnector.insertBLOB(self.input1.text, self.input2.text, self.input3.text, self.input4.text,
                                    self.input5.text, self.input6.text, self.input7.text, self.input8.text)
            if(result):
                self.input1.text = ""
                self.input2.text = ""
                self.input3.text = ""
                self.input4.text = ""
                self.input5.text = ""
                self.input6.text = ""
                self.input7.text = ""
                self.input8.text = ""
    def clear(self,obj):
        self.input1.text= ""
        self.input2.text = ""
        self.input3.text = ""
        self.input4.text = ""
        self.input5.text = ""
        self.input6.text = ""
        self.input7.text = ""
        self.input8.text = ""
        app.screen_manager.current = "Main"
    def transition(self,obj):
        app.screen_manager.current="Main"

class MyApp(App):
    def load(self):
        Clock.schedule_once(self.gotoMain, 15)
    def gotoMain(self,obj):
        app.screen_manager.current = "Main"
    def build(self):
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        self.icon = 'omage.png'
        self.title = 'Game Selector'
        #Window.fullscreen = 'auto'

        self.screen_manager = ScreenManager()
        '''Creation of login screen'''
        # self.load_page = fileViewer()
        # screen = Screen(name='Loading')
        # screen.add_widget(self.load_page)
        # screen.on_enter(self.load())
        # self.screen_manager.add_widget(screen)

        self.main_page = MainView()
        screen = Screen(name='Main')
        screen.add_widget(self.main_page)
        self.screen_manager.add_widget(screen)

        self.add_page = AddView()
        screen = Screen(name='Add')
        screen.add_widget(self.add_page)
        self.screen_manager.add_widget(screen)

        self.allgames_page = AllGamesView()
        screen = Screen(name='AllGames')
        screen.add_widget(self.allgames_page)
        self.screen_manager.add_widget(screen)

        self.lookup_page = LookupView()
        screen = Screen(name='Lookup')
        screen.add_widget(self.lookup_page)
        self.screen_manager.add_widget(screen)


        return self.screen_manager

class popupSuccesfullInsert(Popup):
    def __init__(self, **kwargs):
        super(popupSuccesfullInsert, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.size_hint=[0.5,0.5]
        self.auto_dismiss=False
        self.title="Potwierdzenie"
        box=BoxLayout()
        box.orientation="vertical"
        self.label1=TextInput(text="Udane Dodanie Gry Do Bazy Danych")
        box.add_widget(self.label1)
        box2=BoxLayout()
        box2.add_widget(Button(text="Zamknij", on_release=self.close))
        box.add_widget(box2)
        self.add_widget(box)
    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40:  # 40 - Enter key pressed
            self.dismiss()
    def close(self,obj):
        self.dismiss()

#TODO
class popupTitle(Popup):
    def __init__(self, **kwargs):
        super(popupTitle, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.size_hint=[0.5,0.5]
        self.auto_dismiss=False
        self.title="Filtruj po tytule"
        box=BoxLayout()
        box.orientation="vertical"
        self.input1=TextInput(input_type='text',multiline=False, write_tab=False)
        self.input1.focus=True
        box.add_widget(self.input1)
        box2=BoxLayout()
        box2.add_widget(Button(text="Szukaj", on_release=self.szukaj))
        box2.add_widget(Button(text="Anuluj", on_release=self.close))
        box.add_widget(box2)
        self.add_widget(box)
    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.input1.focus and keycode == 40:  # 40 - Enter key pressed
            dbconnector = DBconnection()
            dbconnector.getGamesByTitle(self.input1.text)
            self.dismiss()
    def szukaj(self,obj):
        dbconnector=DBconnection()
        dbconnector.getGamesByTitle(self.input1.text)
        self.dismiss()
    def close(self,obj):
        self.dismiss()
class popupYear(Popup):
    def __init__(self, **kwargs):
        super(popupYear, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.size_hint=[0.5,0.5]
        self.auto_dismiss=False
        self.title="Filtruj po roku wydania"
        box=BoxLayout()
        box.orientation="vertical"
        self.input1=TextInput(input_type='number',multiline=False, write_tab=False)
        self.input1.focus = True
        box.add_widget(self.input1)
        box2=BoxLayout()
        box2.add_widget(Button(text="Szukaj", on_release=self.szukaj))
        box2.add_widget(Button(text="Anuluj", on_release=self.close))
        box.add_widget(box2)
        self.add_widget(box)
    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.input1.focus and keycode == 40:  # 40 - Enter key pressed
            dbconnector = DBconnection()
            dbconnector.getGamesByYear(self.input1.text)
            self.dismiss()
    def szukaj(self,obj):
        dbconnector=DBconnection()
        dbconnector.getGamesByYear(self.input1.text)
        self.dismiss()
    def close(self,obj):
        self.dismiss()
class popupGenre(Popup):
    def __init__(self, **kwargs):
        super(popupGenre, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.size_hint=[0.5,0.5]
        self.auto_dismiss=False
        self.title="Filtruj po gatunku"
        box=BoxLayout()
        box.orientation="vertical"
        self.input1=TextInput(input_type='text',multiline=False, write_tab=False)
        self.input1.focus = True
        box.add_widget(self.input1)
        box2=BoxLayout()
        box2.add_widget(Button(text="Szukaj", on_release=self.szukaj))
        box2.add_widget(Button(text="Anuluj", on_release=self.close))
        box.add_widget(box2)
        self.add_widget(box)
    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.input1.focus and keycode == 40:  # 40 - Enter key pressed
            dbconnector = DBconnection()
            dbconnector.getGamesByGenre(self.input1.text)
            self.dismiss()
    def szukaj(self,obj):
        dbconnector=DBconnection()
        dbconnector.getGamesByGenre(self.input1.text)
        self.dismiss()
    def close(self,obj):
        self.dismiss()
class popupRating(Popup):
    def __init__(self, **kwargs):
        super(popupRating, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.size_hint=[0.5,0.5]
        self.auto_dismiss=False
        self.title="Filtruj po ocenie"
        box=BoxLayout()
        box.orientation="vertical"
        self.input1=TextInput(multiline=False, write_tab=False)
        self.input1.focus = True
        box.add_widget(self.input1)
        box2=BoxLayout()
        box2.add_widget(Button(text="Szukaj", on_release=self.szukaj))
        box2.add_widget(Button(text="Anuluj", on_release=self.close))
        box.add_widget(box2)
        self.add_widget(box)
    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.input1.focus and keycode == 40:  # 40 - Enter key pressed
            dbconnector = DBconnection()
            dbconnector.getGamesByRating(self.input1.text)
            self.dismiss()
    def szukaj(self,obj):
        dbconnector=DBconnection()
        dbconnector.getGamesByRating(self.input1.text)
        self.dismiss()
    def close(self,obj):
        self.dismiss()
class popupSubject(Popup):
    def __init__(self, **kwargs):
        super(popupSubject, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.size_hint=[0.5,0.5]
        self.auto_dismiss=False
        self.title="Filtruj po tagach"
        box=BoxLayout()
        box.orientation="vertical"
        self.input1=TextInput(multiline=False, write_tab=False)
        self.input1.focus = True
        box.add_widget(self.input1)
        box2=BoxLayout()
        box2.add_widget(Button(text="Szukaj", on_release=self.szukaj))
        box2.add_widget(Button(text="Anuluj", on_release=self.close))
        box.add_widget(box2)
        self.add_widget(box)
    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.input1.focus and keycode == 40:  # 40 - Enter key pressed
            dbconnector = DBconnection()
            dbconnector.getGamesBySubject(self.input1.text)
            self.dismiss()
    def szukaj(self,obj):
        dbconnector=DBconnection()
        dbconnector.getGamesBySubject(self.input1.text)
        self.dismiss()
    def close(self,obj):
        self.dismiss()
class popupDeveloper(Popup):
    def __init__(self, **kwargs):
        super(popupDeveloper, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.size_hint=[0.5,0.5]
        self.auto_dismiss=False
        self.title="Filtruj po twórcach"
        box=BoxLayout()
        box.orientation="vertical"
        self.input1=TextInput(multiline=False, write_tab=False)
        self.input1.focus = True
        box.add_widget(self.input1)
        box2=BoxLayout()
        box2.add_widget(Button(text="Szukaj", on_release=self.szukaj))
        box2.add_widget(Button(text="Anuluj", on_release=self.close))
        box.add_widget(box2)
        self.add_widget(box)
    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.input1.focus and keycode == 40:  # 40 - Enter key pressed
            dbconnector = DBconnection()
            dbconnector.getGamesByDeveloper(self.input1.text)
            self.dismiss()
    def szukaj(self,obj):
        dbconnector=DBconnection()
        dbconnector.getGamesByDeveloper(self.input1.text)
        self.dismiss()
    def close(self,obj):
        self.dismiss()
class popupPublisher(Popup):
    def __init__(self, **kwargs):
        super(popupPublisher, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.size_hint=[0.5,0.5]
        self.auto_dismiss=False
        self.title="Filtruj po wydawcy"
        box=BoxLayout()
        box.orientation="vertical"
        self.input1=TextInput(multiline=False, write_tab=False)
        self.input1.focus = True
        box.add_widget(self.input1)
        box2=BoxLayout()
        box2.add_widget(Button(text="Szukaj", on_release=self.szukaj))
        box2.add_widget(Button(text="Anuluj", on_release=self.close))
        box.add_widget(box2)
        self.add_widget(box)
    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.input1.focus and keycode == 40:  # 40 - Enter key pressed
            dbconnector = DBconnection()
            dbconnector.getGamesByPublisher(self.input1.text)
            self.dismiss()
    def szukaj(self,obj):
        dbconnector=DBconnection()
        dbconnector.getGamesByPublisher(self.input1.text)
        self.dismiss()
    def close(self,obj):
        self.dismiss()

class fileViewer(GridLayout):
    def __init__(self, **kwargs):
        super(fileViewer, self).__init__(**kwargs)
        self.cols=2
        #self.ids="fileViewer"
        fileviewer=FileChooserIconView(on_selection=self.selected)
        self.add_widget(fileviewer)
        image=Image(source="")
        self.add_widget(image)
    def selected(self, filename):
        try:
            self.ids.image.source = filename[0]
        except:
            pass

if __name__ == '__main__':
    dbconnector = DBconnection()
    dbconnector.getAllGames()
    app = MyApp()
    app.run()

    # with cProfile.Profile() as profile:
    #
    #     ps = pstats.Stats(profile)
    #     ps.print_stats()

    print("Koniec Programu")