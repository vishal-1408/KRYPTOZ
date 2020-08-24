from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.lang import Builder
kv='''
Design:
    Button:
        text: "open popup"
        size_hint: (0.5,0.5)
        pos_hint: {"center_x":0.5, "center_y":0.5}
        on_release:
            root.open_temp_popup()
<TempPopup>:
    TextInput:
        size_hint: (0.5,0.2)
        pos_hint: {"center_x":0.5, "top": 0.8}
    TextInput:
        size_hint: (0.5,0.2)
        pos_hint: {"center_x":0.5, "top": 0.55}
    TextInput:
        size_hint: (0.5,0.2)
        pos_hint: {"center_x":0.5, "top": 0.3}
'''
class Design(FloatLayout):
    def open_temp_popup(self):
        design= TempPopup()
        win=Popup(title="temp popup", content= design, size_hint=(None, None), size= (400,400))
        win.open()
class TempPopup(FloatLayout):
    pass
class MyApp(App):
    def build(self):
        return Builder.load_string(kv)
MyApp().run()