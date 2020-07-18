import sys
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.base import runTouchApp
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

Builder.load_file("kiv.kv")

class ScrollableLabel(ScrollView):
	lyrics_file = open('versuri.adi', 'r')
	lyrics = lyrics_file.read()
	lyrics_file.close()
	text = StringProperty(lyrics)

runTouchApp(ScrollableLabel())