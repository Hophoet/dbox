""" main file of the progam """
#! python
# coding: utf-8

from train import OpenDBoxApp, Register, Manager, ContainerScreen, LoginScreen, IconLeftSampleWidget

#main execution not as module importation
if __name__ == '__main__':
    #runing of the application with the run method
    OpenDBoxApp().run()
