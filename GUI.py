from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.core.window import Window
from kivy.uix.popup import Popup
from random import randint
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty, AliasProperty, NumericProperty, DictProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.clock import Clock
#------Imports from the modules---------------------
from EncryptionHashing import hash_str
from FileManage import *
from client import *

#--------------------------------------------------
#---------------App Parameters------------------#
Window.clearcolor = (27/255, 34/255, 36/255, 1)
#------------------------------------------------#

#---------------Global Variables and Global functions------------------#
separator="*****seperator*****"

def error_color(textinput):
	textinput.background_color=(1,120/255,120/255,1)
	textinput.text=''
	textinput.hint_text_color=(216/255,0/255,12/255,1)
	textinput.foreground_color=(0,0,0,1)
def color_fix(textinput):
	textinput.background_color=(40/255,50/255,54/255,1)
	textinput.text=''
	textinput.hint_text_color=(95/255,93/255,98/255,1)
	textinput.foreground_color=(150/255,150/255,150/255,1)
def quick_message(title, multiple_allow, message ):
		design=QuickMessage_pop()
		app=App.get_running_app()
		app.popup_200(design, title, multiple_allow, message)
		design.ids.okay.bind(on_release=app.close_popup)
#------------------------------------------------#

#---------------Custom Widgets------------------#

#------------------------------------------------#

class Login(Screen):
	def Sign_Up(self):
		design = SignUp_pop()
		popup=CustomPopup(
								title='', 
								background="img/popup400.png",
								title_align="center", 
								separator_height=0,
								title_color=[110/255,110/255,110/255,1], 
								content=design, 
								size_hint=(None, None), 
								size=(400,400)
							)
		popup.open()
		design.ids.btn_back.bind(on_release=popup.dismiss)
		design.win.bind(on_dismiss=popup.dismiss)
	
	def login(self):
		hashed_username=str(hash_str(self.ids.username.text))
		hashed_password=str(hash_str(self.ids.password.text))
		Credential_List=return_credentials()
		for i in range(0,len(Credential_List),2):
			if Credential_List[i] == hashed_username and Credential_List[i+1]==hashed_password:
				return True
		return False
	def login_error(self):
		if not self.login():
			quick_message("Login Error", True, "You have entered the wrong credentials. Try again!")
			return False
		else:
			try:
				print('called')
				client_initialize()
				print(self.ids.username.text)
				sendName(self.ids.username.text)
				self.ids.username.text=''
				self.ids.password.text=''
				return True
			except:
				quick_message("Login Error", True, "The connection was not established with the server. Try again!")
				return False
class JoinOrCreate(Screen):
	def client_close(self):
		close()

class CreateGroup(Screen):
	allow_password = BooleanProperty(True)
	def requirements(self):
		if len(self.ids.name.text)>=3:
			if len(self.ids.password.text)<=5:
				if self.ids.password.text==self.ids.c_password.text:
					if int(self.ids.members.text)>=2 and int(self.ids.members.text)<=100:
						return True
					else:
						quick_message("Add your friends!", True, "Add more than 2 and less than 100 members in the chamber.")
						return False
				else:
					quick_message("Meh! don't you wann be secure", True, "Passwords so not match!")
					return False
			else:
					quick_message("Meh! don't you wann be secure", True, "Passwords should be of 5 characters minimum.")
					return False
		else:
			quick_message("Oh darn!", True, "The Chamber Name should be atleast 3 characters.")
			return False

	def submit(self):
		if self.requirements():
			global separator
			sep = separator 
			randlist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']
			randomlen=len(randlist)
			group_code=''
			for i in range (6):
				group_code+=randlist[randint(0,randomlen-1)]
			group_string = self.ids.name.text + group_code + sep + str(hash_str(self.ids.password.text)) + sep + self.ids.members.text + sep + group_code
			sendCreate(group_string)
			self.manager.transition=SlideTransition()
			self.manager.current = 'chatwin'
			self.ids.name.text=''
			self.ids.password.text
			self.ids.c_password.text
			self.ids.members.text
class SelectGroup(Screen):
	activegroups = ListProperty()
	def add_data(self):#Might have to change for efficiency
		sendGroups()
		print("these are the details")
		Clock.schedule_once(self.schedule_details)
	def schedule_details(self, *args):	
		self.detail_list=return_details()
		for group in self.detail_list:
			group_data = {'group_name': group[0][:-6], 'password': group[1], 'members': group[2], 'group_code': group[3], 'owner': self}
			self.activegroups.append(group_data)
	def clear_recycleview(self):
		self.activegroups=[]


class RecycleGroups(RecycleDataViewBehavior,BoxLayout):
	owner =  ObjectProperty()
	group_name = StringProperty()
	group_code = StringProperty()
	members = NumericProperty()
	password = StringProperty()
	index = NumericProperty()
	
	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		return super(RecycleGroups, self).refresh_view_attrs(rv, index, data)
class ChatWindow(Screen):
	pass

class Screen_Manager(ScreenManager):
	pass

#---------------Popups---------------------------#
class CustomPopup(Popup):
	pass
class SignUp_pop(BoxLayout):
	win = CustomPopup(                                  #Sucess Signup popup defined as data member for on_dismiss callback
						title='Warning',
						title_align="center", 
						separator_color=(22/255,160/255,133/255,1),
						size_hint=(None, None), 
						size=(400,200)
					)
	def authenticate_signup_and_hash(self):
		self.username = self.ids.username.text
		self.password = self.ids.password.text
		self.c_password = self.ids.c_password.text
		if len(self.password)>=8 and len(self.username)>0:  
			if self.c_password==self.password:
				cred_file= None
				user_exists=False
				username_hash = hash_str(self.username)
				password_hash = hash_str(self.password)
				if  not os.path.isfile(Return_App_Path("UserCredentials.txt")): #ON FIRST SIGNUP
					cred_file = open(Return_App_Path("UserCredentials.txt"), "w")
				else:#IF not first SIGN UP
					cred_file = open(Return_App_Path("UserCredentials.txt"), "a")
					user_exists = User_Check(str(username_hash), str(password_hash)) # Checks if user exists in the userlist 
				if not user_exists: # if user doesn't not exist in the credential list
					WriteLine(cred_file, str(username_hash))
					WriteLine(cred_file, str(password_hash))
					cred_file.close()
					color_fix(self.ids.username)
					color_fix(self.ids.password)
					color_fix(self.ids.c_password)
					design=QuickMessage_pop()
					design.ids.message.text="You have signed-up. Proceed to log-in."
					self.win.content=design
					self.win.open()
					design.ids.okay.bind(on_release=self.win.dismiss)
				else:
					quick_message("Warning", True, "A user with the same username exists on this PC. Try a new useraname.")
					error_color(self.ids.username)
			else:
				quick_message("Warning", True, "The passwords do not match. Try again!")
				error_color(self.ids.password)
				error_color(self.ids.c_password)
		else:
			if len(self.username)==0 and len(self.password)<8:
				quick_message("Warning", True, "\u2022The username must be given\n\u2022The password must be 8 characters long.")
				error_color(self.ids.username)
				error_color(self.ids.password)
			elif len(self.ids.password.text)<8:
				quick_message("Warning", True, "The password must be 8 characters long.")
				error_color(self.ids.password)
			elif len(self.ids.username.text)==0:
				quick_message("Warning", True, "The username must be given.")
				error_color(self.ids.username)

	def quick_message(self, title, multiple_allow, message ):
		design=QuickMessage_pop()
		app=App.get_running_app()
		app.popup_200(design, title, multiple_allow, message)
		design.ids.okay.bind(on_release=app.close_popup)

class QuickMessage_pop(BoxLayout):
	pass
#------------------------------------------------#

#-------------main app loop---------#
class ChatApp(App):
	popups = []
	def close_popup(self, *args):
		if self.popups:
			self.popups.pop(-1).dismiss() # dismissing the last popup in the list of popups
	def close_all_popups(self):
		while self.popups:
			self.close_popup() #deleting all the popups one by one 
	def popup_400(self, content, title, multiple_allow):
		if multiple_allow:
			self.close_all_popups()
		popup = CustomPopup(
								title=title, 
								title_align="center", 
								background= "img/popup400.png",
    							separator_color=(22/255,160/255,133/255,1),
								content=content, 
								size_hint=(None, None), 
								size=(400,400),
								auto_dismiss=False
							)
		popup.open()
		self.popups.append(popup)
	def popup_200(self, content, title, multiple_allow, message):
		if multiple_allow:
			self.close_all_popups()
			content.ids.message.text=message
		popup = CustomPopup(
								title=title, 
								title_align="center", 
    							separator_color=(22/255,160/255,133/255,1),
								content=content, 
								size_hint=(None, None), 
								size=(400,200)
							)
		popup.open()
		self.popups.append(popup)
if __name__ == '__main__':
    ChatApp().run()