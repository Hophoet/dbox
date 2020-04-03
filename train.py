""" The program class implementation """
#coding:utf-8
import time
import datetime
from kivy.factory import Factory
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivymd.theming import ThemeManager
from kivy.lang import Builder
from kivymd.uix.dialog import MDInputDialog, MDDialog
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import TwoLineIconListItem,IconLeftWidget, ILeftBodyTouch, OneLineIconListItem
from kivymd.uix.dialog import MDDialog
#import of the database manager
from data_manage import DataBase


#loading of the kv file for the design
ROOT = Builder.load_file('train.kv')

#icon class
class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    """definition for indirect use"""
    """
    def __init__(self, *args, **kwargs):
        ILeftBodyTouch.__init__(self)
        MDIconButton.__init__(self, *args, **kwargs)
        """

class LoginScreen(Screen):
    """The login screen of the application """



    #validate the client input information
    def validate(self):
        """validate function of the client input to login the application """
        #condition. if the password is correct or not
        if self.ids.password.text == 'root':
            self.manager.current = 'app'
            self.manager.transition.direction = 'left'
            self.ids.password.text = ''

        #situation if the textfield is empty or not correct
        else:
            self.ids.login_label.markup = True
            if self.ids.password.text == '':
                self.ids.login_label.text = '[color=ff0033]Password required[/color]'
                self.ids.password.focus = True
            else:
                self.ids.login_label.text = '[color=ff0033]Incorrect password[/color]'
                self.ids.password.focus = True

class DetailScreen(Screen):
    """The detail screen of the customer """
    #redefined of the constructor
    def __init__(self, *args, **kwargs):
        """constructor of the detail screen """
        Screen.__init__(self, *args, **kwargs)
        self.database = DataBase('base')

    def back(self, *args, **kwargs):
        """method use for navigation """
        #self.manager.current = self.manager.previous()
        self.manager.current = 'app'
        self.manager.transition.direction = 'left'

    def get_client(self, number):
        """method to get the clicked customer"""
        client = Register().get_clients().get(number)
        return client
    def on_enter(self):
        """on enter method of the detail view"""
        number = int(self.manager.screen_one.number)
        visits = self.database.get_visits(number)
        visit_size = len(visits)
        #visit string to display (plural of only one)
        if visit_size == 1:
            visit_string = 'visit'
        else:
            visit_string = 'visits'

        customer = self.database.get_customer_by_number(number)
        self.ids.detail_header.text = f'[b]{customer[1]}[/b]'
        self.ids.detail_header.secondary_text  = f'{number}              {visit_size} '+visit_string
        for visit in visits:
            #formating of the date and time of the visits
            visit_date = time.strftime('%d-%m-%Y', time.localtime(visit[2]))
            visit_time = time.strftime('%H:%M', time.localtime(visit[2]))
            #display of the detail with visits
            self.ids.detail_motifs.add_widget(TwoLineIconListItem(
            text=f'{visit[3]}',
            secondary_text=visit_time+' '+visit_date,
            secondary_font_style='Subtitle2',
            divider='Inset',
            disabled=True
            ))

    def on_leave(self):
        self.ids.detail_motifs.clear_widgets()




class ContainerScreen(Screen):
    """The principal screen of the application """
    #constructor for initialisation of the data
    def __init__(self, *args, **kwargs):
        """constructor of the principal screen """
        Screen.__init__(self, *args, **kwargs)
        self.database = DataBase('base')



    #creation of methode to_focus for managing the focus stape during the add of customer
    def to_focus(self, textinput):
        """focus manager between the textinputs for the add of customer"""
        #if the textinput name is validate
        if textinput == 'motif':
            self.ids.motif.focus = True
        elif textinput == 'phone_number':
            self.ids.phone_number.focus = True



    def on_enter(self, *args, **kwargs):
        """redefined method """
        self.display_client()
    def on_leave(self):
        self.ids.box.clear_widgets()

    #method to dispay clients
    def display_client(self):
        """method to add the current client as a widget in the view part"""
        customers = self.database.get_all_customers()
        for customer in customers:
            self.ids.box.add_widget(
                TwoLineIconListItem(
                    text='[b]' + customer[1] + '[/b]' ,
                    secondary_text=str(customer[2]),
                    id=str(customer[2]),
                    on_press=self.detail
                    )#.add_widget(IconLeftSampleWidget(icon='account-card-details'))
            )

            #self.ids.list_item.add_widget(IconLeftSampleWidget(icon='account-card-details'))


        #print('000000000000000000000', dir(self.ids.dialog))
    #navigate method
    def navigate(self, nav, *args, **kwargs):
        """method use for navigation """
        self.manager.current = 'login'
        self.ids.box.clear_widgets()
        self.manager.transition.direction = 'right'

    def detail(self, customer=None):
        """method use for navigation """
        self.manager.current = 'detail'
        self.manager.screen_one.number = customer.id
        self.manager.transition.direction = 'right'
        #print(dir(self.ids.box), list(map(lambda x: x.id, self.ids.box.children)))

        #print(dir(self.manager.screen_one))


    def client(self):
        """the principal method for the adding client into the data file """
        #get of the client input information by the widget id
        name = self.ids.name.text
        motif = self.ids.motif.text
        #set the markup of the phone number textfield to True
        self.ids.phone_number.markup = True
        number = self.ids.phone_number.text

        #get of the differents condition of the validation of the client adding
        name_condition = (not name.isspace()) and len(name) != 0
        motif_condition = (not motif.isspace()) and len(motif) != 0
        number_condition = not number.isspace()
        if motif_condition and name_condition and number_condition:
            if (not number.isdigit()) or (not len(number) == 8):
                self.ids.error_message.text = '[color=ff0033]invalide phone number[/color]'
            else:
                #client = Register(name, motif, phone_number)
                #instruction to do if the client exists in the data file
                if self.database.customer_exists(number):
                    self.ids.error_message.text = '[color=ff0033]Client exist[/color]'
                    self.database.set_data(name, motif, number)
                #saving insctruction
                else:

                    self.database.set_data(name, motif, number)
                    #saving message
                    self.ids.error_message.text = '[color=00ff33]Save successully![/color]'

                    #add as widget in the application
                    self.ids.box.add_widget(TwoLineIconListItem(
                    text = '[b]'+self.ids.name.text+'[/b]', secondary_text=self.ids.phone_number.text))
                    #saving in the data file

                #add as widget in the application
                #delete the current input after the save
                self.ids.name.text = ''
                self.ids.motif.text = ''
                self.ids.phone_number.text = ''


        #instruction for an invalid input
        else:
            self.ids.error_message.text = '[color=ff0033]Invalid input[/color]'


class Manager(ScreenManager):
    """The screen manager class"""
    #login screen
    login_screen = ObjectProperty(None)
    #content screen
    container_screen = ObjectProperty(None)
    #detail scree
    detail_screen = ObjectProperty(None)

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
        self.data = self.get_clients()


    def exists(self):
        """client exists testing method """

        if self.phone_number in self.data.keys():
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

        #if the current client alrady exists, add the motif with his date
        #in the database
        if self.exists():
            client_informations = self.data.get(self.phone_number)
            client_informations[1][self.date] = self.motif
        else:
            #set of the current client into the data file
            self.data[self.phone_number] = [self.name, {self.date:self.motif}]
        file = open(Register.file_path, 'w')
        file.write(str(self.data))
        #closing of the file
        file.close()



class OpenDBoxApp(App):
    """application principal class """
    #set of the theme manager and a set of principal theme

    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Blue'
    theme_cls.accent_palette = 'Blue'
    theme_cls.accent_palette = 'Gray'
    theme_cls.theme_style = 'Dark'

    def build(self):
        """method use to display the application"""
        #return the screen manager
        return Manager()


#main execution not as module importation
if __name__ == '__main__':
    #runing of the application with the run method
    OpenDBoxApp().run()
