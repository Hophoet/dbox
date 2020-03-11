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
from kivymd.uix.list import TwoLineIconListItem, ILeftBodyTouch, ThreeLineAvatarIconListItem, ThreeLineListItem, ThreeLineIconListItem

#loading of the kv file for the design
root = Builder.load_file('train.kv')

#icon class
class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass

class LoginScreen(Screen):
    """The login screen of the application """
    #validate the client input information
    def validate(self):
        """validate function of the client input to login the application """
        #condition. if the password is correct or not
        if self.ids.password.text =='root':
            self.manager.current = 'app'
            self.manager.transition.direction ='left'
            self.ids.password.text = ''

        else:
            #situation if the textfield is empty or not
            if self.ids.password.text == '':
                self.ids.login_label.text = 'Password required'
                print(dir(self.ids.button))
                print(dir(self.ids.button.color))
                self.ids.password.focus = True
            else:
                self.ids.login_label.text = 'Incorrect password'
                self.ids.password.focus = True

class ContainerScreen(Screen):
    """The principal screen of the application """
    #constructor for initialisation of the data
    def __init__(self, *args, **kwargs):
        """constructor of the principal screen """
        Screen.__init__(self, *args, **kwargs)

        #self.display_client()

    def on_enter(self, *args, **kwargs):
        self.display_client()

    #method to dispay clients
    def display_client(self):
        """method to add the current client as a widget in the view part"""
        client = Register()
        clients = client.get_clients()
        print('type', type(clients))
        print(dir(TwoLineIconListItem))
        for key, value in clients.items():
            self.ids.box.add_widget(
                TwoLineIconListItem(
                    text='[b]'+value[0]+'[/b]        '+value[1],
                    secondary_text=str(key),

                    )
            )



    #navigate method
    def navigate(self, *args, **kwargs):
        """method use for navigation """
        self.manager.current = 'login'
        self.manager.transition.direction ='right'


    def client(self):
        """the principal method for the adding client into the data file """
        #get of the client input information by the widget id
        name = self.ids.name.text
        motif = self.ids.motif.text
        #set the markup of the phone number textfield to True
        self.ids.phone_number.markup = True
        phone_number = self.ids.phone_number.text

        #get of the differents condition of the validation of the client adding
        name_condition = (not name.isspace() ) and len(name)!=0
        motif_condition = (not motif.isspace()) and len(motif)!=0
        number_condition = (not phone_number.isspace())
        if motif_condition and name_condition and number_condition:
            if (not phone_number.isdigit()) or (not len(phone_number)==8):
                self.ids.error_message.text ='[color=ff0033]invalide phone number[/color]'
            else:
                client = Register(name, motif, phone_number)
                #instruction to do if the client exists in the data file
                if client.exists():
                    self.ids.error_message.text = '[color=ff0033]Client exist[/color]'
                #saving insctruction
                else:
                    #saving in the data file
                    client.set_clients()
                    data = client.get_clients()
                    #add as widget in the application
                    self.ids.box.add_widget(TwoLineIconListItem(
                    text=self.ids.name.text +'        '+self.ids.motif.text,
                    secondary_text=self.ids.phone_number.text))
                    #delete the current input after the save
                    self.ids.name.text = ''
                    self.ids.motif.text = ''
                    self.ids.phone_number.text = ''
                    #saving message
                    self.ids.error_message.text = '[color=00ff33]Save successully![/color]'

                    for key, value in data.items():
                        print(key, value)
        #instruction for an invalid input
        else:
            self.ids.error_message.text = '[color=ff0033]Invalid input[/color]'


class Manager(ScreenManager):
    """The screen manager class"""
    #login screen
    login_screen = ObjectProperty(None)
    #content screen
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
        """getter of the client in the data file"""
        #open of the file
        file = open(Register.file_path, 'r')
        #convert of the file to dictionnary file
        data = eval(file.read())
        #closing of the file
        file.close()
        #return of the client dictionnary
        return data

    def set_clients(self):
        """client setter into the data file"""
        #get of the clients dictionnary
        data = self.get_clients()
        #set of the current client into the data file
        data[self.phone_number] = (self.name, self.motif, self.date)
        file = open(Register.file_path, 'w')
        file.write(str(data))
        #closing of the file
        file.close()



class OpenDBoxApp(App):
    """application principal class """
    #set of the theme manager and a set of principal theme
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Yellow'
    theme_cls.accent_palette = 'Blue'
    theme_cls.accent_palette = 'Orange'
    theme_cls.theme_style = 'Dark'

    def build(self):
        """method use to display the application"""
        #return the screen manager
        print(dir(Manager()))
        return Manager()


#main execution not as module importation
if __name__ == '__main__':
    #runing of the application with the run method
    OpenDBoxApp().run()
