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

#---------------Global Variables------------------#
separator="*****seperator*****"
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
	
	
class JoinOrCreate(BoxLayout):
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
	def authenticate_signup_and_hash(self):
		self.username = self.ids.username.text
		self.password = self.ids.password.text
		self.c_password = self.ids.c_password.text
		if len(self.password)>8 and len(self.username)>0 and self.c_password==self.password:
			username_hash = hash_str(self.username)
			password_hash = hash_str(self.password)
			cred_file= None
			user_exists=False
			if  not os.path.isfile(Return_App_Path("UserCredentials.txt")):
				cred_file = open(Return_App_Path("UserCredentials.txt"), "w")
			else:
				cred_file = open(Return_App_Path("UserCredentials.txt"), "a")
				user_exists = User_Check(str(username_hash), str(password_hash)) # Checks if user exists in the userlist 
			if not user_exists: # if user doesn't not exist in the credential list
				WriteLine(cred_file, str(username_hash))
				WriteLine(cred_file, str(password_hash))
				design=QuickMessage_pop()
				app=App.get_running_app()
				app.popup_200(design, "Success!", True, 'You have Signed up! Proceed to login')
			cred_file.close()

class QuickMessage_pop(BoxLayout):
	pass
#------------------------------------------------#

#-------------main app loop---------#
class ChatApp(App):
	popups = []
	def close_popup(self):
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
								title_color=[110/255,110/255,110/255,1], 
								content=content, 
								size_hint=(None, None), 
								size=(400,400)
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
								title_color=[110/255,110/255,110/255,1], 
								content=content, 
								size_hint=(None, None), 
								size=(400,200)
							)
		popup.open()
		self.popups.append(popup)
if __name__ == '__main__':
    ChatApp().run()