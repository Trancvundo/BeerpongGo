from kivy.app import App
from kivy import utils
from kivy.lang import Builder
import json
import requests
import os
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, NoTransition
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import BooleanProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.network.urlrequest import UrlRequest
from kivy.factory import Factory
import sys
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
from json import dumps
#import os.path
#import urllib.request
#import urllib.error
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivy.core.window import Window
from kivy.uix.image import Image
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
import certifi
#Window.size = (412, 732)


class WelcomeScreen(Screen):
    pass

class SigninScreen(Screen):
    InvalidMessage = ""
    def signin(self, email, password):
        my_data = dict()
        my_data["email"] = email
        my_data["password"] = password
        my_data["returnSecureToken"] = True
        firebase_apikey = ""
        json_data = json.dumps(my_data).encode()	
        request = ("https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key="+firebase_apikey)
        
      		
        UrlRequest(request,
                   req_body = json_data,
                   on_success = self.succesLogin,
                   on_failure = self.failureLogin,
                   on_error = self.errorLogin,
                   ca_file = certifi.where(),
                   verify=True
                   )
      
    def succesLogin(self, urlrequest, log_in_data):
        player.refresh_token = log_in_data["refreshToken"]
        player.localId = log_in_data["localId"]
        player.idToken = log_in_data["idToken"]
        MainApp().getJ()
        if not (MainApp.checkData.get(player.localId) is None): #check if first time login, create nickname
            self.parent.current = 'main_screen'
        else:
            MainApp().patchJ('{"' + player.localId + '":{"username":"Temp","total_score":"0","total_earned":"0","games_won":"0","games_played":"0","normal_ping_pong_ball":"0","great_ping_pong_ball":"0","love_ping_pong_ball":"0","triangle_ping_pong_ball":"0","trick":"0","cupofdeath":"0","average_winning":"0","average_lost":"0","highest_winning":"0","highest_lost":"0","adje_solidair":"0"}}')
            self.parent.current = 'set_nickname_screen'
        
    def failureLogin(self, urlrequest, failure_data):
        message = failure_data['error']['message']
        SigninScreen.InvalidMessage = message
        MainApp().show_Invalid()
    def errorLogin(self, *args):
        print("error")        
   

class CreateAccountScreen(Screen):
    def register(self, email, password):

        my_data = dict()
        my_data["email"] = email
        my_data["password"] = password
        my_data["returnSecureToken"] = True
        firebase_apikey = ""
        json_data = json.dumps(my_data).encode()
        request = ("https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key="+firebase_apikey)

        UrlRequest(request,
                   req_body = json_data,
                   on_success = self.succesCreate,
                   on_failure = self.failureCreate,
                   on_error = self.errorCreate,
                   ca_file = certifi.where(),
                   verify=True
                   )
      
    def succesCreate(self, urlrequest, log_in_data):
        MainApp().show_SuccesCreated()
        self.parent.current = 'signin_screen'
    def failureCreate(self, urlrequest, failure_data):
        message = failure_data['error']['message']
        SigninScreen.InvalidMessage = message
        MainApp().show_Invalid()
    def errorCreate(self, *args):
        print("error")        
    

class MainScreen(Screen):
    usernamev = ObjectProperty(None)
    total_scorev = ObjectProperty(None)
    stats = ObjectProperty(None)
    def on_enter(self, *args):
        MainApp().getValues()
        self.usernamev.text = player.usernamev
        self.total_scorev.text = "ExP = " + player.total_scorev

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        menu_main = [{"icon":"","text": "Log out"},
                      {"icon":"","text": "Change username"}
                      ]
        self.menu1 = MDDropdownMenu(
            caller=self.ids.menubtn, items=menu_main, width_mult=4, callback=self.menu_callbackM
        )
    
    def menu_callbackM(self, instance):
        option_menu = instance.text
        print(option_menu)
        self.menu1.dismiss()                
        if option_menu == "Log out":
            MainApp().show_LogoutM()        
        if option_menu == "Change username":
            MainApp().show_change()

class SoloGameScreen(Screen):

    usernamev = ObjectProperty(None)
    total_scorev = ObjectProperty(None)
    cup = ObjectProperty(None)

    image_source = StringProperty()
    red10_opi = ObjectProperty(1)
    red9_opi = ObjectProperty(1)
    red8_opi = ObjectProperty(1)
    red7_opi = ObjectProperty(1)
    red6_opi = ObjectProperty(1)
    red5_opi = ObjectProperty(1)
    red4_opi = ObjectProperty(1)
    red3_opi = ObjectProperty(1)
    red2_opi = ObjectProperty(1)
    red1_opi = ObjectProperty(1)

    def on_enter(self, *args):
        MainApp.selecteditem = "Normal"
        player.cup = 10
        MainApp().getValues()
        player.cup = str(player.cup)
        self.usernamev.text = player.usernamev
        self.total_scorev.text = "ExP = " + player.total_scorev
        self.cup.text = "Cups left: " + player.cup
        self.image_source == "normalpp.png"
        for i in range(1,11):
            x = "self.red" + str(i) + "_opi = 1"
            exec(x)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image_source = 'normalpp.png'
        menu_enemy = [{"viewclass": "MDMenuItem", "text": "Enemy uses revive","icon":""},
                      {"viewclass": "MDMenuItem", "text": "Adje solidair","icon":""},
                      {"viewclass": "MDMenuItem", "text": "Enemy has won","icon":""}
                      ]
        menu_menu = [{"icon":"","text": "Log out"},
                      {"icon":"","text": "Change username"},
                      {"icon":"","text": "Give Up"}
                      ]
        self.menu2 = MDDropdownMenu(
            caller=self.ids.enemybtn, items=menu_enemy, width_mult=4, callback=self.menu_callback
        )
        self.menu3 = MDDropdownMenu(
            caller=self.ids.menubtn, items=menu_menu, position="auto", width_mult=4, callback=self.menu_callback
        )

    def menu_callback(self, instance):
        option_menu = instance.text
        print(option_menu)
        self.menu2.dismiss()                
        self.menu3.dismiss()
        if option_menu == "Enemy uses revive":
            player.cup = int(player.cup)
            player.cup += 1
            self.cup.text = "Cups left: " + str(player.cup)
            x = "self.red" + str(player.cup) + "_opi = 1"
            exec(x)            
            toast("Enemy uses revive",1)
        if option_menu == "Adje solidair":
            player.total_scorev = int(player.total_scorev)
            player.total_scorev -= 50
            player.total_scorev = str(player.total_scorev)
            self.total_scorev.text = "ExP = " + player.total_scorev 
            toast("Enemy uses Adje solidair",1)
        if option_menu == "Enemy has won":

            player.games_playedv = str(int(player.games_playedv) + 1)
            player.average_lostv = int(player.average_lostv)
            player.cup = int(player.cup)
            player.average_lostv = player.average_lostv + player.cup
            player.highest_lostv = int(player.highest_lostv)
            if player.cup > player.highest_lostv:
                player.highest_lostv = player.cup 
            MainApp().patchAll()
            self.parent.current = "main_screen"
            toast("Enemy has won",1)
        if option_menu == "Log out":
            MainApp().show_Logout()        
        if option_menu == "Change username":
            MainApp().show_change()
 

    def changeName(self):
        self.usernamev.text = player.usernamev

    def changeImage(self, *args):
        if MainApp.selecteditem == "Normal":
            self.image_source = "normalpp.png"
        if MainApp.selecteditem == "Great":
            self.image_source = 'greatpp.png'
        if MainApp.selecteditem == "Love":
            self.image_source = 'lovepp.png'
        if MainApp.selecteditem == "Triangle":
            self.image_source = 'trianglepp.png'
        if MainApp.selecteditem == "Trick":
            self.image_source = 'trickpp.png'
        if MainApp.selecteditem == "Cup of Death":
            self.image_source = 'deathpp.png'
        if MainApp.selecteditem == "Ellenboogh":
            self.image_source = 'elbow.png'
        if MainApp.selecteditem == "Extra worp":
            self.image_source = 'extraworp.png'
        if MainApp.selecteditem == "Disperse":
            self.image_source = 'disperse.png'
        if MainApp.selecteditem == "Adje solidair":
            self.image_source = 'adjesolidair.png'
        if MainApp.selecteditem == "Confusion":
            self.image_source = 'confusion.png'
        if MainApp.selecteditem == "+1":
            self.image_source = 'plusone.png'
        if MainApp.selecteditem == "Revive":
            self.image_source = 'revive.png'
        if MainApp.selecteditem == "Master ball":
            self.image_source = 'master.png'
        if MainApp.selecteditem == "Rearrange":
            self.image_source = "rearrange.png"


    def actionbtn(self):
        if MainApp.selecteditem == "Normal":
            player.total_scorev = int(player.total_scorev)
            player.cup = int(player.cup)
            player.normal_ping_pong_ballv = int(player.normal_ping_pong_ballv)
            player.total_earnedv = int(player.total_earnedv)
            player.total_earnedv += 10
            player.total_scorev += 10
            player.cup -= 1
            player.normal_ping_pong_ballv += 1
            player.total_scorev = str(player.total_scorev)
            player.normal_ping_pong_ballv = str(player.normal_ping_pong_ballv)
            self.total_scorev.text = "ExP = " + player.total_scorev
            self.cup.text = "Cups left: " + str(player.cup)
            toast("+10 ExP", 1)
            for i in range(int(player.cup)+1,11):
                x = "self.red" + str(i) + "_opi = 0"
                exec(x)

            if int(player.cup) < 1:
                MainApp().patchAll()
                self.parent.current = "won_screen"
                MainApp().show_won()

        
        if MainApp.selecteditem == "Great":
            if int(player.cup) > 1:
                player.total_scorev = int(player.total_scorev)
                player.cup = int(player.cup)
                player.great_ping_pong_ballv = int(player.great_ping_pong_ballv)
                player.total_earnedv = int(player.total_earnedv)
                player.total_earnedv += 20
                player.total_scorev += 20
                player.cup -= 2
                player.great_ping_pong_ballv += 1
                self.total_scorev.text = "ExP = " + str(player.total_scorev)
                self.cup.text = "Cups left: " + str(player.cup)
                toast("+20 ExP", 1)
                for i in range(int(player.cup)+1,11):
                    x = "self.red" + str(i) + "_opi = 0"
                    exec(x)

                if int(player.cup) < 1:
                    MainApp().patchAll()
                    self.parent.current = "won_screen"
                    MainApp().show_won()
    
        if MainApp.selecteditem == "Trick":
            player.total_scorev = int(player.total_scorev)
            player.total_scorev += 75
            player.total_earnedv = int(player.total_earnedv)
            player.total_earnedv += 75
            self.total_scorev.text = "ExP = " + str(player.total_scorev)
            toast("+75 ExP + ? ExP", 1)
            
                   
        if MainApp.selecteditem == "Triangle":
            if int(player.cup) > 2:
                player.total_scorev = int(player.total_scorev)
                player.cup = int(player.cup)
                player.triangle_ping_pong_ballv = int(player.triangle_ping_pong_ballv)
                player.total_earnedv = int(player.total_earnedv)
                player.total_earnedv += 100
                player.total_scorev += 100
                player.cup -= 3
                player.triangle_ping_pong_ballv += 1
                self.total_scorev.text = "ExP = " + str(player.total_scorev)
                self.cup.text = "Cups left: " + str(player.cup)
                toast("+100 ExP", 1)
                for i in range(int(player.cup)+1,11):
                    x = "self.red" + str(i) + "_opi = 0"
                    exec(x)
                if int(player.cup) < 1:
                    MainApp().patchAll()
                    self.parent.current = "won_screen"
                    MainApp().show_won()                
                    
        if MainApp.selecteditem == "Love":
            player.love_ping_pong_ballv = int(player.love_ping_pong_ballv)
            player.love_ping_pong_ballv += 1
            player.cup = int(player.cup)
            player.cup -= 1
            self.cup.text = "Cups left: " + str(player.cup)
            toast("+0 ExP", 1)
            for i in range(int(player.cup)+1,11):
                x = "self.red" + str(i) + "_opi = 0"
                exec(x)
            if int(player.cup) < 1:
                MainApp().patchAll()
                self.parent.current = "won_screen"
                MainApp().show_won()

            
        if MainApp.selecteditem == "Cup of Death":
            player.total_scorev = int(player.total_scorev)
            player.cup = int(player.cup)
            player.cupofdeathv = int(player.cupofdeathv)
            player.total_scorev += (10 * player.cup) + 75
            player.total_earnedv = int(player.total_earnedv)
            player.total_earnedv += (10 * player.cup) + 75
            cups = player.cup
            player.cup -= player.cup
            player.cupofdeathv += 1
            self.total_scorev.text = "ExP = " + str(player.total_scorev)
            self.cup.text = "Cups left: " + str(player.cup)
            toast("+" + str(cups) + "0 ExP", 1)
            for i in range(int(player.cup)+1,11):
                x = "self.red" + str(i) + "_opi = 0"
                exec(x)

            if int(player.cup) < 1:
                MainApp().patchAll()
                self.parent.current = "won_screen"
                MainApp().show_won()
                
        if MainApp.selecteditem == "Ellenboogh":
            if int(player.total_scorev) > 30:
                player.total_scorev = int(player.total_scorev)
                player.total_scorev -= 30
                self.total_scorev.text = "ExP = " + str(player.total_scorev)
                toast("-30 ExP",1)
                
        if MainApp.selecteditem == "Extra worp":
            if int(player.total_scorev) > 20:
                player.total_scorev = int(player.total_scorev)
                player.total_scorev -= 20
                self.total_scorev.text = "ExP = " + str(player.total_scorev)
                toast("-20 ExP",1)
 
        if MainApp.selecteditem == "Disperse":
           if int(player.total_scorev) > 40:
                player.total_scorev = int(player.total_scorev)
                player.total_scorev -= 40
                self.total_scorev.text = "ExP = " + str(player.total_scorev)
                toast("-40 ExP",1)
                
        if MainApp.selecteditem == "Adje solidair":
            if int(player.total_scorev) > 0:
                player.total_scorev = int(player.total_scorev)
                player.total_scorev += 50
                self.total_scorev.text = "ExP = " + str(player.total_scorev)
                toast("+50 ExP",1)
                
        if MainApp.selecteditem == "Confusion":
            if int(player.total_scorev) > 20:
                player.total_scorev = int(player.total_scorev)
                player.total_scorev -= 20
                self.total_scorev.text = "ExP = " + str(player.total_scorev)
                toast("-20 ExP",1)
                
        if MainApp.selecteditem == "+1":
            if int(player.total_scorev) > 75:
                player.total_scorev = int(player.total_scorev)
                player.total_scorev -= 75
                self.total_scorev.text = "ExP = " + str(player.total_scorev)
                toast("-75 ExP",1)

        if MainApp.selecteditem == "Revive":
            if int(player.total_scorev) > 30:
                player.total_scorev = int(player.total_scorev)
                player.total_scorev -= 30
                self.total_scorev.text = "ExP = " + str(player.total_scorev)
                toast("-30 ExP",1)

        if MainApp.selecteditem == "Master ball":
            if int(player.total_scorev) > 150:
                player.total_scorev = int(player.total_scorev)
                player.total_scorev -= 140
                self.total_scorev.text = "ExP = " + player.total_scorev
                toast("-150 ExP, +10 ExP", 1)
                player.cup = int(player.cup)
                player.cup -= 1
                self.cup.text = "Cups left: " + str(player.cup)
                for i in range(int(player.cup)+1,11):
                    x = "self.red" + str(i) + "_opi = 0"
                    exec(x)
    
                if int(player.cup) < 1:
                    MainApp().patchAll()
                    self.parent.current = "won_screen"
                    MainApp().show_won()



class SetNicknameScreen(Screen):   
    def setnickname(self, nickname):
        nick = nickname
        MainApp().getValues()
        player.usernamev = nick        
        MainApp().patchAll()
        self.parent.current = 'main_screen'

class WonScreen(Screen):
    usernamev = ObjectProperty(None)
    
    def on_enter(self, *args):
        MainApp().getValues()
        self.usernamev.text = player.usernamev


    def update(self):
        MainApp().getValues()
        player.total_scorev = int(player.total_scorev)
        player.total_earnedv = int(player.total_earnedv)
        player.total_scorev += int(player.cupleft) * 10
        player.total_earnedv += int(player.cupleft) * 10
        player.games_wonv = str(int(player.games_wonv) + 1)
        player.games_playedv = str(int(player.games_playedv) + 1)
        player.average_winningv = int(player.average_winningv)
        player.cupleft = int(player.cupleft)
        player.average_winningv = player.average_winningv + player.cupleft
        player.highest_winningv = int(player.highest_winningv)
        if player.cupleft > player.highest_winningv:
            player.highest_winningv = player.cupleft 
        MainApp().patchAll()
        
class ContentNick(BoxLayout):
    pass

class ContentWon(BoxLayout):
    pass

class MainApp(MDApp):
    checkData = ""
    leaderstr = ""
    selecteditem = ""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Red"
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome_screen"))
        sm.add_widget(SigninScreen(name="signin_screen"))
        sm.add_widget(CreateAccountScreen(name="create_account_screen"))
        sm.add_widget(MainScreen(name="main_screen"))
        sm.add_widget(SoloGameScreen(name="solo_game_screen"))
        sm.add_widget(SetNicknameScreen(name="set_nickname_screen"))
        sm.add_widget(WonScreen(name="won_screen"))
        sm.current = "welcome_screen"

        
        return sm
                

    url = '' # You must add .json to the end of the URL
    
    def patchJ(self, JSON):
        to_database = json.loads(JSON)
        requests.patch(url = self.url, json = to_database)
    
    def postJ(self, JSON):
        to_database = json.loads(JSON)
        requests.post(url = self.url, json = to_database)
    
    def putJ(self, JSON):
        to_database = json.loads(JSON)
        requests.put(url = self.url, json = to_database)
    
    def deleteJ(self, JSON):
        requests.delete(url = self.url[:-5] + JSON + ".json")
    
    auth_key = 'WsqPsgYYGle1c7wGSs2t0XgtcG66OqsvGW6OAjZH' # Refer to the YouTube video on where to find this.
    
    def getJ(self):
        request = requests.get(self.url + '?auth=' + self.auth_key)
        MainApp.checkData = request.json()

    def patchAll(self):
        JSON = '{"' + str(player.localId) + '":{"username":"' + str(player.usernamev) + '","total_score":"' + str(player.total_scorev) + '","total_earned":"' + str(player.total_earnedv) + '","games_won":"' + str(player.games_wonv) + '","games_played":"' + str(player.games_playedv) +'","normal_ping_pong_ball":"' + str(player.normal_ping_pong_ballv) +'","great_ping_pong_ball":"' + str(player.great_ping_pong_ballv) +'","love_ping_pong_ball":"' + str(player.love_ping_pong_ballv) +'","triangle_ping_pong_ball":"' + str(player.triangle_ping_pong_ballv) +'","trick":"' + str(player.trickv) +'","cupofdeath":"' + str(player.cupofdeathv) +'","average_winning":"' + str(player.average_winningv) +'","average_lost":"' + str(player.average_lostv) +'","highest_winning":"' + str(player.highest_winningv) +'","highest_lost":"' + str(player.highest_lostv) +'","adje_solidair":"' + str(player.adje_solidairv) +'"}}'
        to_database = json.loads(JSON)
        requests.patch(url = self.url, json = to_database)
    
    def getValues(self):
        MainApp().getJ()
        player.usernamev = MainApp.checkData[player.localId]["username"]
        player.total_scorev = MainApp.checkData[player.localId]["total_score"]
        player.total_earnedv = MainApp.checkData[player.localId]["total_earned"]
        player.games_wonv  = MainApp.checkData[player.localId]["games_won"]
        player.games_playedv  = MainApp.checkData[player.localId]["games_played"]
        player.normal_ping_pong_ballv  = MainApp.checkData[player.localId]["normal_ping_pong_ball"]
        player.great_ping_pong_ballv  = MainApp.checkData[player.localId]["great_ping_pong_ball"]
        player.love_ping_pong_ballv  = MainApp.checkData[player.localId]["love_ping_pong_ball"]
        player.triangle_ping_pong_ballv  = MainApp.checkData[player.localId]["triangle_ping_pong_ball"]
        player.trickv  = MainApp.checkData[player.localId]["trick"]
        player.cupofdeathv  = MainApp.checkData[player.localId]["cupofdeath"]
        player.average_winningv = MainApp.checkData[player.localId]["average_winning"]
        player.average_lostv = MainApp.checkData[player.localId]["average_lost"]
        player.highest_winningv = MainApp.checkData[player.localId]["highest_winning"]
        player.highest_lostv = MainApp.checkData[player.localId]["highest_lost"]
        player.adje_solidairv = MainApp.checkData[player.localId]["adje_solidair"]         


    def getLeader(self):
        MainApp().getJ()
        leaderlst = []
        MainApp.leaderstr = ""
        ind = 1
        for i in MainApp.checkData:
            x = MainApp.checkData[i]["username"]
            y = MainApp.checkData[i]["total_score"]
            leaderlst.append([x,int(y)])
        def takeSecond(elem):
            return elem[1]
        leaderlst.sort(key=takeSecond, reverse=True)
        for i in leaderlst:
            MainApp.leaderstr += str(ind) + ". " + str(i[0]) + ": " + str(i[1]) + " ExP\n"
            ind += 1

        
    def show_Stats(self, *args):   
        MainApp().getstats()
        self.dialog = MDDialog(
            title="Stats",
            text = player.stats,
            size_hint=(0.9,0.9),
            buttons=[
                MDFlatButton(
                    text="Close", on_release = self.dialog_handler
                ),
            ],
        )
        self.dialog.open()

    def show_Multiplayer(self, *args):
        self.dialog = MDDialog(
            title="Message",
            text = "Coming Soon (Probably not)",
            auto_dismiss=False,
            size_hint=(0.9,0.9),
            buttons=[
                MDFlatButton(
                    text="Close", on_release = self.dialog_handler
                ),
            ],
        )
        self.dialog.open()    

    def show_Leaderboard(self, *args):
        self.dialog = MDDialog(
            title="Leaderboard",
            text = MainApp.leaderstr,
            auto_dismiss=False,
            size_hint=(0.9,0.9),
            buttons=[
                MDFlatButton(
                    text="Close", on_release = self.dialog_handler
                ),
            ],
        )
        self.dialog.open()    
    
    def show_Invalid(self,*args):
        
        self.dialog = MDDialog(
            title = "Invalid",
            text = SigninScreen.InvalidMessage,
            auto_dismiss=False,
            size_hint=(0.9,0.9),
            buttons=[
                MDFlatButton(
                    text="Close", on_release = self.dialog_handler
                ),
            ],           
        )
        self.dialog.open()

    def show_SuccesCreated(self,*args):
        self.dialog = MDDialog(
            title = "Succes!",
            text = "Succesful created a new account",
            auto_dismiss = False,
            size_hint=(0.9,0.9),
            buttons=[
                MDFlatButton(
                    text="Close", on_release = self.dialog_handler
                ),
            ],           
        )
        self.dialog.open()

    def show_Logout(self,*args):
        self.dialog = MDDialog(
            title = "Log Out",
            text = "Are you sure?\nUse the Enemy button if you are defeated",
            auto_dismiss = False,
            size_hint=(0.9,0.9),
            buttons=[
                MDFlatButton(
                    text="Close", on_release = self.dialog_handler
                ),
                MDFlatButton(
                    text="Log out", on_release = self.dialog_handler
                ),
            ],           
        )
        self.dialog.open()

    def show_LogoutM(self,*args):
        self.dialog = MDDialog(
            title = "Log Out",
            text = "Are you sure?",
            auto_dismiss = False,
            size_hint=(0.9,0.9),
            buttons=[
                MDFlatButton(
                    text="Close", on_release = self.dialog_handler
                ),
                MDFlatButton(
                    text="Log out", on_release = self.dialog_handler
                ),
            ],           
        )
        self.dialog.open()

    def show_change(self):
        self.dialog = MDDialog(
            title="Change Username",
            auto_dismiss = False,
            size_hint=(0.9,0.9),
            type="custom",
            content_cls=ContentNick(),
            buttons=[
                MDFlatButton(
                    text="Cancel",  on_release= self.dialog_handler
                ),
                MDFlatButton(
                    text="Change",  on_release=self.dialog_handler
                ),
            ],
        )
        self.dialog.open()            


    def show_won(self):
        self.dialog = MDDialog(
            title="You have won!",
            auto_dismiss = False,
            size_hint=(0.9,0.9),
            type="custom",
            content_cls=ContentWon(),
            buttons=[
                MDFlatButton(
                    text="Submit",  on_release=self.dialog_handler
                ),
            ],
        )
        self.dialog.open()            

         
         
    
    def dialog_handler(self, widget):
        print(widget.text)
        if widget.text == "Close":
            self.dialog.dismiss()
        if widget.text == "Log out":
            MDApp.get_running_app().stop()
        if widget.text == "Change":
            for obj in self.dialog.content_cls.children:
                if isinstance(obj, MDTextField):
                    print(obj.text)
                    username = obj.text
            if username != "":
                player.usernamev = username        
                MainApp().patchAll()
                self.dialog.dismiss()
        if widget.text == "Cancel":
            self.dialog.dismiss()
        if widget.text == "Submit":
            for obj in self.dialog.content_cls.children:
                if isinstance(obj, MDTextField):
                    print(obj.text)
                    player.cupleft = ""
                    player.cupleft = obj.text
            if int(player.cupleft) > 0 and int(player.cupleft) < 11:
                WonScreen().update()
                self.dialog.dismiss()
                
    def callback_for_menu_items(self, *args):

        MainApp.selecteditem = args[0]
        SoloGameScreen().changeImage()


    def show_ball_grid_bottom_sheet(self):
        bottom_sheet_menu = MDGridBottomSheet()
        data = {
            "Normal": "normalppM.png",
            "Great": "greatppM.png",
            "Love": "loveppM.png",
            "Triangle": "triangleppM.png",
            "Trick": "trickppM.png",
            "Cup of Death": "deathppM.png"
        }
        for item in data.items():
            bottom_sheet_menu.add_item(
                item[0],
                lambda x, y=item[0]: self.callback_for_menu_items(y),
                icon_src=item[1],
            )
        bottom_sheet_menu.open()

    def show_item_grid_bottom_sheet(self):
        bottom_sheet_menu = MDGridBottomSheet()
        data = {
            "Ellenboogh": "elbowM.png",
            "Rearrange": "rearrangeM.png",
            "Extra worp": "extraworpM.png",
            "Disperse": "disperseM.png",
            "Adje solidair": "adjesolidairM.png",
            "Confusion": "confusionM.png",
            "+1": "plusoneM.png",
            "Revive": "reviveM.png",
            "Master ball": "masterM.png"
        }
        for item in data.items():
            bottom_sheet_menu.add_item(
                item[0],
                lambda x, y=item[0]: self.callback_for_menu_items(y),
                icon_src=item[1],
            )
        bottom_sheet_menu.open()

    def getstats(self):
        try:
            x = int(player.average_winningv) / int(player.games_wonv)
        except:
            x = 0
        else:
            x = round(int(player.average_winningv) / int(player.games_wonv),2)
        try:
            y = int(player.average_lostv) / (int(player.games_playedv) - int(player.games_wonv))
        except:
            y = 0
        else:
            y = int(player.average_lostv) / (int(player.games_playedv) - int(player.games_wonv))

            
        player.stats = ("Username: " + str(player.usernamev) + 
         "\nTotal ExP: " + str(player.total_scorev) + 
         "\nExP earned: " + str(player.total_earnedv) + 
         "\nGames won: " + str(player.games_wonv) + 
         "\nGames played: " + str(player.games_playedv) + 
         "\nNormal Ping-Pong Ball: " + str(player.normal_ping_pong_ballv) + 
         "\nGreat Ping-Pong Ball: " + str(player.great_ping_pong_ballv) + 
         "\nLove Ping-Pong Ball: " + str(player.love_ping_pong_ballv) +
         "\nTriangle Ping-Pong Ball: " + str(player.triangle_ping_pong_ballv) +
         "\nTrick Ping-Pong Ball: " + str(player.trickv) +
         "\nCup of Death: " + str(player.cupofdeathv) +
         "\nAverage win: " + str(x) +
         "\nAverage lost: " + str(y) +
         "\nHighest win: " + str(player.highest_winningv) +
         "\nHighest lost: " + str(player.highest_lostv) +
         "\nAdje solidair: " + str(player.adje_solidairv))  

class player:
    localId = ""
    refresh_token = ""
    idToken = ""
    usernamev = ""
    total_scorev = ""  
    total_earnedv = "" 
    games_wonv  = "" 
    games_playedv  = "" 
    normal_ping_pong_ballv  = "" 
    great_ping_pong_ballv  = "" 
    love_ping_pong_ballv  = "" 
    triangle_ping_pong_ballv  = ""  
    trickv = ""
    cupofdeathv  = "" 
    average_winningv = ""  
    average_lostv = "" 
    highest_winningv = "" 
    highest_lostv = "" 
    adje_solidairv = ""
    cup = ""
    cupleft = ""    
    stats = ""

    

        
if __name__ == "__main__":
     MainApp().run()