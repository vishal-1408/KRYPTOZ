from kivy.config import Config
Config.set('graphics', 'width',  800)
Config.set('graphics', 'height', 600)
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.core.window import Window
from kivy.uix.popup import Popup
from random import randint
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty, AliasProperty, NumericProperty, DictProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.clock import Clock 
import pyperclip
import os
#------Imports from the modules---------------------
from client import *
from kivy.animation import Animation
from functools import partial
#--------------------------------------------------
#---------------App Parameters------------------#
Window.clearcolor = (27/255, 34/255, 36/255, 1)
Window.bind(on_request_close=sendLogout)
#------------------------------------------------#

#---------------Global Variables and Global functions------------------#
separator="*****seperator*****"
refresh_group_list = None
chamber_name_and_code = ''
username = ''
ECC_Key = None
Sender_Key = generate_AES_key()
print(Sender_Key)

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
class CustomTextInput(TextInput):
	def keyboard_on_key_down(self, window, keycode, text, modifiers):
		if keycode[0] == 13:
			print('ENTER WAS PRESSED ENTER WAS PRESSED ENTER WAS PRESSED 1')
			self.press_enter(self, self.text)
		super().keyboard_on_key_down(window, keycode, text, modifiers)
	def press_enter(self, instance, text):
		print('ENTER WAS PRESSED ENTER WAS PRESSED ENTER WAS PRESSED 2')
		pass
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
		try:
			Credential_List=return_credentials()
		except:
			print('a')
			return False
		else:
			for i in range(0,len(Credential_List),2):
				if Credential_List[i] == hashed_username and Credential_List[i+1]==hashed_password:
					global username, ECC_Key
					username = self.ids.username.text
					ECC_Key = get_key(self.ids.username.text, self.ids.password.text)
					print(ECC_Key)
					return True

	def login_error(self):
		if not self.login() and not os.path.isfile(Return_App_Path('UserCredentials.txt')) :
			quick_message("Login Error", True, "You need to sign-up first")
		elif not self.login():
			quick_message("Login Error", True, "You have entered the wrong credentials. Try again!")
			return False
		else:
			try:
				global ECC_Key,Sender_Key
				print('called')
				client_initialize()
				print(self.ids.username.text)
				sendName(read_code_from_file(self.ids.username.text),[ECC_Key.pointQ.x,ECC_Key.pointQ.y], ECC_Key.d,Sender_Key)
				self.ids.username.text=''
				self.ids.password.text=''
				return True
			except Exception as e:
				print(e)
				quick_message("Login Error", True, "The connection was not established with the server. Try again!")
				return False
	
	def transition_after_login(self, *args):
		app = App.get_running_app()
		if self.login_error():
			app.root.transition = SlideTransition(direction = 'left')
			app.root.current = 'join_or_create' 

class JoinOrCreate(Screen):
	def client_close(self):
		sendLogout()

class CreateGroup(Screen):
	allow_password = BooleanProperty(True)
	def requirements(self):
		if self.ids.members.text.isnumeric():
			if len(self.ids.name.text)>=3 and len(self.ids.name.text)<=15:
				if len(self.ids.password.text)>=5:
					if self.ids.password.text==self.ids.c_password.text:
						if int(self.ids.members.text)>=2 and int(self.ids.members.text)<=100:
							return True
						else:
							quick_message("Add your friends!", True, "Add more than 2 and less than 100 members in the chamber.")
							return False
					else:
						quick_message("Meh! don't you wanna be secure", True, "Passwords so not match!")
						return False
				else:
						quick_message("Meh! don't you wanna be secure", True, "Passwords should be of 5 characters minimum.")
						return False
			else:
				quick_message("Oh darn!", True, "The Chamber Name should be atleast 3 characters and maximum 15.")
				return False
		else:
			quick_message("Oh darn!", True, "The Chamber Name should be atleast 3 characters and maximum 15.")
			return False

	def submit(self, *args):
		if self.requirements():
			global separator
			sep = separator 
			randlist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']
			randomlen=len(randlist)
			group_code=''
			for i in range (6):
				group_code+=randlist[randint(0,randomlen-1)]
			group_string = self.ids.name.text.strip() + sep + str(hash_str(self.ids.password.text)) + sep + self.ids.members.text.strip() + sep + group_code
			#print(group_string)
			sendCreate(group_string)
			global chamber_name_and_code
			chamber_name_and_code  = self.ids.name.text + group_code #Assigning the group name to global variable so that we can access it in chatwin
			print(chamber_name_and_code+ 'FROM GUI CHAMBER INFO')
			self.manager.transition=SlideTransition(direction="down")
			self.manager.current = 'chatwin'
			#clearing textinputs
			self.ids.name.text=''
			self.ids.password.text=''
			self.ids.c_password.text=''
			self.ids.members.text=''
			#self.manager.transition=SlideTransition(direction="right")

class SelectGroup(Screen):
	activegroups = ListProperty()

	def on_search(self):
		sendGroups() #Test this and remove 
		#sendMembers() #Test this and remove
		Clock.schedule_once(self.search_refresh)
		global refresh_group_list
		refresh_group_list =  Clock.schedule_interval(self.search_refresh, 1)

	def search_refresh(self, *args):
		sendGroups()
		search_text = self.ids.search_box.text.strip() #remove whitepaces in beg and end
		search_text = search_text.lower() #all lower for search efficiency
		self.activegroups = []
		self.detail_list =  return_details()
		for group_name, value in self.detail_list.items():
			if search_text in group_name.lower(): #substring searching
				group_found = {'group_name': group_name[0:value[1]], 'limit': value[0],
								'group_code': group_name[value[1]:], 'members_online':return_members()[group_name],
								'owner': self} #if substring match is successful the group is added to the rv
				self.activegroups.append(group_found)

	def unschedule(self):
		global refresh_group_list
		refresh_group_list.cancel()


class RecycleGroups(RecycleDataViewBehavior,BoxLayout):
	owner =  ObjectProperty()
	group_name = StringProperty()
	group_code = StringProperty()
	limit = NumericProperty()
	members_online = NumericProperty()
	password = StringProperty()
	index = NumericProperty()
	auth = None
	full = None
	group_details = ListProperty()

	def update_online_members(self, *args): 
		#sendMembers()
		members_online = return_members()
		try:
			self.design.ids.members.text = "Members Online: " + "[color=#E0744C]" + str(members_online[self.design.chambername]) + "[color=#E0744C]"
		except:
			self.design.ids.members.text = "Members Online: " + "[color=#E0744C]0[color=#E0744C]"
	def AuthenticateAndJoin(self):
		self.design = GroupVerifyAndJoin()
		self.design.chambername = self.group_name+self.group_code
		self.design.ids.title.text = "Enter the password of: "
		self.design.ids.name.text = "[color=#E0744C]" +  str(self.design.chambername) + "[color=#E0744C]"
		self.update_online_members()
		self.refresh_members = Clock.schedule_interval(self.update_online_members, 1)
		self.authwin = CustomPopup(
								title='', 
								background="img/authentication.png",
								title_align="center", 
								separator_height=0,
								separator_color=(22/255,160/255,133/255,1), 
								content=self.design, 
								size_hint=(None, None), 
								size=(400,400),
								auto_dismiss=False
							)
		self.authwin.open()
		self.authwin.bind(on_dismiss = self.cancel)
		self.design.ids.back.bind(on_release=self.authwin.dismiss)
		self.design.ids.submit.bind(on_release=self.join_result)
	def cancel(self, dt):
		self.refresh_members.cancel()

	def join_result(self,*args):
		self.refresh_members.cancel()
		self.authwin.dismiss()
		if len(return_details())!=0:
			self.design.Authenticate_Client_Gui()
			self.auth_and_full()
			self.conditions()
		else:
			quick_message("Chamber was abandoned", True, "The group has been removed due to inactivity." )

	def conditions(self, *args):
		group_deleted = False		
		#print(str(self.auth)+'\t'+str(self.full)+' 2')
		return_details_list = return_details()
		if len(return_details_list) == 0:
			group_deleted= True
			self.refresh_members.cancel()
		else:
			for group in return_details_list:
				if self.group_name+self.group_code!= group:
					print('\ngroup deleted entered here ' + str(group))
					group_deleted = True
				else:
					group_deleted = False
					print('\ngroup deleted entered here asdfsdf ' + str(group))
					break
		print('group deleted: '+ str(group_deleted))
		if not group_deleted:
			if self.auth and not self.full:
				auth_design = QuickMessage_pop()
				auth_design.ids.message.text = 'The password was verified press okay to continue.'
				self.success_auth = CustomPopup(title='Success',
										title_align='center',
										separator_color=(22/255,160/255,133/255,1), 
										content=auth_design,
										size_hint=(None,None),
										size=(400,200),
										auto_dismiss=False
										)
				self.success_auth.open()
				global chamber_name_and_code
				chamber_name_and_code =self.design.chambername
				auth_design.ids.okay.bind(on_release=self.transition)
				self.refresh_members.cancel()
				global refresh_group_list
				refresh_group_list.cancel()
			elif self.group_dead:
				quick_message("Chamber was abandoned", True, "The group has been removed due to inactivity." )
			elif self.full:
				quick_message("Ah! You are late", True, "The chamber is currently full.")
					
			elif not self.auth:
				quick_message("Oops!", True, "Wrong password was entered.")
			
		else:
			quick_message("Chamber was abandoned", True, "The group has been removed due to inactivity." )
	
	def auth_and_full(self, *args):
		self.auth=None
		self.full=None
		self.group_dead = None
		set_group_dead()
		makeNone()
		while (self.auth==None or self.full==None) and (self.group_dead!= True) :
			#print("loop")
			self.group_dead = return_groupdead()
			self.auth = return_authenticate()
			self.full = return_groupfull()
			#print(str(self.auth)+'\t'+str(self.full)+' 1')
		print(self.group_dead)
	def transition(self, instance):
		self.success_auth.dismiss()
		app=App.get_running_app()
		app.root.transition = SlideTransition(direction='left')
		app.root.current = 'chatwin'
		join = app.root.get_screen('join')
		join.unschedule()

	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		return super(RecycleGroups, self).refresh_view_attrs(rv, index, data)

class GroupVerifyAndJoin(BoxLayout):
	chambername = StringProperty()
	def Authenticate_Client_Gui(self):
		global separator
		join_string = self.chambername + separator + str(hash_str(self.ids.password.text))
		#print(join_string)
		sendJoin(join_string)

class Username_display_pop(BoxLayout):
	def copy(self):
		pyperclip.copy(self.ids.label.text[:-29]+self.ids.label.text[-13:-8])

class MemberLabels(RecycleDataViewBehavior, BoxLayout):
	text=StringProperty()
	owner = ObjectProperty()
	index = NumericProperty(0)
	color = StringProperty()
	def give_username(self):
		print('give username')
		design = Username_display_pop()
		design.ids.label.text = self.text
		self.pop = ModalView(
					size_hint= (None, None),
					size = (400,80),
					pos_hint = {'x': 0, 'top':1},
					background = 'img/username_pop.png'
				   )
		self.pop.add_widget(design)
		self.pop.open()
		self.pop.bind(on_open=self.dismiss_pop)
		self.pop.bind(on_dismiss=self.cancel_trigger)

	def dismiss_pop(self, instance):
		print('open')
		self.dismiss_trigger = Clock.schedule_once(lambda dt: self.pop.dismiss(), 5)
	
	def cancel_trigger(self, instance):
		print('cancel')
		self.dismiss_trigger.cancel()

	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		return super(MemberLabels, self).refresh_view_attrs(rv, index, data)

class Message(RecycleDataViewBehavior, BoxLayout):
	owner = ObjectProperty()
	index = NumericProperty(0)
	username_color = StringProperty()
	def update_height(self, *_):
		self.height = self.ids.userLabel.texture_size[1] + self.ids.messageLabel.texture_size[1] + 20
	
	def refresh_view_attrs(self, rv, index, data):
		Clock.schedule_once(self.update_height, -1)
		self.index = index
		return super().refresh_view_attrs(rv, index, data)

class ChatWindow(Screen):
	messages = ListProperty()
	members_online = ListProperty()
	user_color = hex_gen()

	def members_online_rv_assignment(self):
		sendMembersList()
		Clock.schedule_once(self.schedule_members_online)
		self.refresh_online_members = Clock.schedule_interval(self.schedule_members_online, 1)

	def schedule_members_online(self, *_):
		#sendMembersList()
		self.member_list=return_memeberslist()
		self.public_keys = return_publickeys()
		#print(self.public_keys)
		#print(self.member_list)
		self.members_online = []
		for member in self.member_list:
			global username
			if username == member[:-4]:
				color =  '#ba4a00'
			else:
				color = '#117a65'  
			self.members_online.append({
				'text': member[:-4]+'[color=#abb2b9] @'+member[-4:]+'[/color]',
				'color': color,
				'owner': self
			})
	
	def unschedule_on_exit(self):
		self.refresh_online_members.cancel()
		self.message_refresh.cancel()

	def assign_chamber_info(self):
		global chamber_name_and_code
		self.ids.info_label.text = "[color=#E0744C]" + chamber_name_and_code[:-6] + "[/color] " + chamber_name_and_code[-6:]
	
	def add_message(self, text, color, name):
		global username
		'''if name == username:
			u_col = (0,1,0,1)
		else:
			u_col = (1,0,0,1)'''
		if name == username:
			u_col = '#e67e22'
		elif name == 'ChatBot':
			u_col = '#a93226'
		else:
			u_col = '#aeb6bf'
		self.messages.append({
			'message_id': len(self.messages),
			'bg_color': color,
			'username': name,
			'username_color': u_col,
			'text': text
		})
		print(username)

	def refresh_messages_scheduler(self):
		self.message_refresh = Clock.schedule_interval(self.refresh_messsages, 0.5)

	def refresh_messsages(self, dt):
		new_messages = return_message()
		for messages in new_messages:
			print (messages)
			self.add_message(messages['message'], messages['colour'], messages['name'])
	
	def send_message(self, *args):
		global username
		if self.ids.message_input.text is not '':
			self.add_message(self.ids.message_input.text, self.user_color, username)
			sendMessage(self.ids.message_input.text, self.user_color)
			self.scroll_bottom()
		Clock.schedule_once(self.clear_message_box)
	
	def clear_message_box(self, dt):
		self.ids.message_input.text=''
	
	def scroll_bottom(self):
		Animation.cancel_all(self.ids.chat_view, 'scroll_y')
		Animation(scroll_y=0, t='out_quad', d=.5).start(self.ids.chat_view)
	
	def exit_chat(self):
		sendLogout()
		self.messages={}
		self.unschedule_on_exit()

	def copytoclipboard(self):
		global chamber_name_and_code
		pyperclip.copy(chamber_name_and_code)

class Screen_Manager(ScreenManager):
	pass





#---------------------------------------------------------------------Popups--------------------------------------------------------------------------#

class CustomPopup(Popup):
	pass

class SignUp_pop(BoxLayout):
	win = CustomPopup(                                  #Sucess Signup popup defined as data member for on_dismiss callback
						title='Success!',
						title_align="center", 
						separator_color=(22/255,160/255,133/255,1),
						size_hint=(None, None), 
						size=(400,200)
					)
	def authenticate_signup_and_hash(self):
		self.username = self.ids.username.text
		self.password = self.ids.password.text
		self.c_password = self.ids.c_password.text
		if len(self.password)>=8 and len(self.username)>0 and len(self.username)<=26:  
			if self.c_password==self.password:
				cred_file= None
				user_exists=False
				username_hash = hash_str(self.username)
				password_hash = hash_str(self.password)
				code_export_file(self.username)
				if  not os.path.isfile(Return_App_Path("UserCredentials.txt")): #ON FIRST SIGNUP
					cred_file = open(Return_App_Path("UserCredentials.txt"), "w")
				else:#IF not first SIGN UP
					cred_file = open(Return_App_Path("UserCredentials.txt"), "a")
					user_exists = User_Check(str(username_hash), str(password_hash)) # Checks if user exists in the userlist 
				if not user_exists: # if user doesn't not exist in the credential list
					WriteLine(cred_file, str(username_hash))
					WriteLine(cred_file, str(password_hash))
					cred_file.close()
					gen_key_export(self.username, self.password) # To generate ECC key
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
				quick_message("Warning", True, "\u2022The username must be in the range of 0 to 26 characters\n\u2022The password must be 8 characters long.")
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
