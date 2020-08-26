from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.core.window import Window
from kivy.uix.popup import Popup
#------Imports from the modules---------------------
from EncryptionHashing import hash_str
from FileManage import *
#--------------------------------------------------
#---------------App Parameters------------------#
Window.clearcolor = (27/255, 34/255, 36/255, 1)
#------------------------------------------------#

#---------------Global Variables and functions------------------#
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
#------------------------------------------------#

#---------------Custom Widgets------------------#

#------------------------------------------------#

class Login(Screen):
	
	def quick_message(self, title, multiple_allow, message ):
		design=QuickMessage_pop()
		app=App.get_running_app()
		app.popup_200(design, title, multiple_allow, message)
		design.ids.okay.bind(on_release=app.close_popup)

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
			self.quick_message("Login Error", True, "You have entered the wrong credentials. Try again!")
		else:
			self.ids.username.text=''
			self.ids.password.text=''
class JoinOrCreate(Screen):
	pass

class CreateGroup(Screen):
	pass

class SelectGroup(Screen):
	pass

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
					self.quick_message("Warning", True, "A user with the same username exists on this PC. Try a new useraname.")
					error_color(self.ids.username)
			else:
				self.quick_message("Warning", True, "The passwords do not match. Try again!")
				error_color(self.ids.password)
				error_color(self.ids.c_password)
		else:
			if len(self.username)==0 and len(self.password)<8:
				self.quick_message("Warning", True, "\u2022The username must be given\n\u2022The password must be 8 characters long.")
				error_color(self.ids.username)
				error_color(self.ids.password)
			elif len(self.ids.password.text)<8:
				self.quick_message("Warning", True, "The password must be 8 characters long.")
				error_color(self.ids.password)
			elif len(self.ids.username.text)==0:
				self.quick_message("Warning", True, "The username must be given.")
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