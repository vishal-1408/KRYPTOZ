from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition

class Login(Screen):
	def authenticate(self):
		self.manager.transition=FadeTransition(duration=1.2)
		self.manager.current = 'main'

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

kv=Builder.load_file("Chat.kv")
class ChatApp(App):
    def build(self):
    	return kv

if __name__ == '__main__':
    ChatApp().run()