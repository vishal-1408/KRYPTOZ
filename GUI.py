from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.core.window import Window
from kivy.uix.popup import Popup
#---------------App Parameters------------------#
Window.clearcolor = (27/255, 34/255, 36/255, 1)
#------------------------------------------------#

#---------------Global Variables------------------#

#------------------------------------------------#

class Login(Screen):
	def Sign_Up(self):
		design = SignUp_pop()
		app=App.get_running_app()
		app.popup_400(design, "Sign-Up", False)

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
	def __init__(self, **kwargs):
		super(CustomPopup, self).__init__(**kwargs)
		self.size_hint=(None,None)
		self.size=(400,400)
class SignUp_pop(BoxLayout):
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
		popup = CustomPopup(title=title, content=content, size_hint=(None, None), size=(400,400))
		popup.open()
		self.popups.append(popup)
if __name__ == '__main__':
    ChatApp().run()