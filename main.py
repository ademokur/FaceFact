# coding: utf-8
import os
from kivy.app import App
from kivy.graphics import Color,Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from models import Person
from kivy.uix.anchorlayout import AnchorLayout
from  kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from  kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from time import sleep

import random
import face_rect as face


pointer = face.dlib_pointer()

class PersonInfo(BoxLayout):
    def __init__(self,isMouthOpen=True, isEyesOpen=True,isSmile=True, image_path=""):
        super().__init__()
        self.orientation = "vertical"
        self.size_hint_y = .2
        self.size_hint_x = .3
        #Values
        self.isMouthOpen = isMouthOpen
        self.isEyesOpen = isEyesOpen
        self.isSmile = isSmile

        #Labels
        self.isMouthOpen = Label(text ="Is Mouth Open : {}".format(isMouthOpen))
        self.isEyesOpen = Label(text ="Is Eyes Open : {}".format(isEyesOpen))
        self.isSmile = Label(text ="Is Smile Open : {}".format(isSmile))
        self.image_pathLabel = Label(text=" Image Path : {}".format(image_path))

        #Adding Widget
        self.add_widget(self.isMouthOpen)
        self.add_widget(self.isEyesOpen)
        self.add_widget(self.isSmile)
        self.add_widget(self.image_pathLabel)


#buttons
class NextWindow(FloatLayout):
    def __init__(self):
        super().__init__()
        #Prepare Buttons
        self.next = Button(text = "Next")
        self.next.size_hint = .4, .1
        self.next.pos_hint = {"x":.5, "y":.1}
        self.previous = Button(text="Previous")
        self.previous.size_hint = .4, .1
        self.previous.pos_hint = {"x": .1, "y": .1}


        self.iter = 0
        # functionEvent
        self.imageLayout = BoxLayout(orientation="vertical")

        self.image_viewer1 = Image(size_hint=(1,1))
        self.image_viewer2 = Image(size_hint=(1,1))
        #Bind buttons to functions
        self.next.bind(on_press=self.iter_forward)
        self.previous.bind(on_press=self.iter_back)

        self.add_widget(self.next)
        self.add_widget(self.previous)

        self.add_widget(self.imageLayout)
        self.imageLayout.add_widget(self.image_viewer1)
        self.imageLayout.add_widget(self.image_viewer2)

    def button_active(self):
        # if self.iter <= 0:
        #     self.iter = 1
        # elif self.iter > 6:
        #     self.iter = 6

        self.iter=+1


        try:
            if os.path.exists("Foto/{}.jpg".format(self.iter)):
                path = "Foto/{}.jpg".format(self.iter)
            else:
                path = "Foto/{}.png".format(self.iter)
            self.image_viewer.source = path
            print(path)
            face.on_path(path)
        except:
            print(self.iter)
        pass
        # self.add_widget(Image(source="Foto/bac.png"))
        # if os.path.exists("Foto/{}.jpg".format(self.iter)):
        #     self.add_widget(Image(source="Foto/{}.jpg".format(self.iter)))
        # else:
        #     self.add_widget(Image(source= "Foto/{}.png".format(self.iter)))

    def iter_forward(self, event):
        self.iter +=1
        self.button_active()


    def iter_back(self, event):
        self.iter -= 1
        self.button_active()


class Program(App):
    def build(self):
        # Main Interface
        self.govde = BoxLayout()
        self._ImageSide = AnchorLayout()
        self._infoSide = AnchorLayout()
        self.buttons = NextWindow()

        #Buttons
        self.iter = 0
        self.person = PersonInfo(image_path="__path")

        #Inferface of People
        self.govde.add_widget(self._ImageSide)
        self.govde.add_widget(self._infoSide)

        self._infoSide.add_widget(self.person)
        self._infoSide.add_widget(self.buttons)

        return self.govde

Program().run()