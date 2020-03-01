from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivymd.theming import ThemeManager
from kivy.lang import Builder
from kivymd.uix.dialog import MDInputDialog, MDDialog
import datetime
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import TwoLineIconListItem, ILeftBodyTouch

root = Builder.load_file('train.kv')

class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass

class LoginScreen(Screen):
    def validate(self):

        if self.ids.password.text =='root':
            self.manager.current = 'container_screen'
        else:
            if self.ids.password.text == '':
                self.ids.login_label.text = 'Password required'
            else:
                self.ids.login_label.text = 'Incorrect password'

class ContainerScreen(Screen):
    #constructor for initialisation of the data
    def __init__(self, *args, **kwargs):
        Screen.__init__(self, *args, **kwargs)
        print(dir(self))
        #self.display_client()
    #function to dispay clients
    def display_client(self):
        client = Register()
        clients = client.get_clients()
        for key, value in clients:
            self.ids.box.add_widget(TwoLineIconListItem(text=value[0]))

    def client(self):

        name = self.ids.name.text
        motif = self.ids.motif.text
        self.ids.phone_number.markup = True
        phone_number = self.ids.phone_number.text
        name_condition = (not name.isspace() ) and len(name)!=0
        motif_condition = (not motif.isspace()) and len(motif)!=0
        number_condition = (not phone_number.isspace())
        if motif_condition and name_condition and number_condition:
            if (not phone_number.isdigit()) or (not len(phone_number)==8):
                self.ids.error_message.text ='[color=ff0033]invalide phone number[/color]'
            else:
                client = Register(name, motif, phone_number)
                if client.exists():
                    self.ids.error_message.text = '[color=ff0033]Client exist[/color]'
                else:
                    client.set_clients()
                    data = client.get_clients()
                    self.ids.box.add_widget(TwoLineIconListItem(
                    text=self.ids.name.text +'        '+self.ids.motif.text,
                    secondary_text=self.ids.phone_number.text))
                    self.ids.name.text = ''
                    self.ids.motif.text = ''
                    self.ids.phone_number.text = ''

                    self.ids.error_message.text = '[color=00ff33]Save successully![/color]'

                    for key, value in data.items():
                        print(key, value)
        else:
            self.ids.error_message.text = '[color=ff0033]Invalid input[/color]'


class Manager(ScreenManager):
    login_screen = ObjectProperty(None)
    container_screen = ObjectProperty(None)

class Register:
    """class for the client registry"""
    file_path = 'data/data.txt'
    clients_list = {}
    def __init__(self, name='', motif='', phone_number=''):
        """Register constructor for the initilizing"""
        self.name = name
        self.motif = motif
        self.date = datetime.datetime.today()
        self.phone_number = phone_number


    def exists(self):
        data = self.get_clients()
        if self.phone_number in data.keys():
            return True
        else:
            return False

    def get_clients(self):
        file = open(Register.file_path, 'r')
        data = eval(file.read())
        file.close()
        return data

    def set_clients(self):
        data = self.get_clients()
        data[self.phone_number] = (self.name, self.motif, self.date)
        file = open(Register.file_path, 'w')
        file.write(str(data))
        file.close()



class OpenDBoxApp(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Yellow'

    theme_cls.accent_palette = 'Blue'
    theme_cls.accent_palette = 'Orange'
    theme_cls.theme_style = 'Dark'
    def build(self):
        print(dir(self))

        return Manager()



if __name__ == '__main__':
    OpenDBoxApp().run()
