import kivy
import Lyric_Finder
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from subprocess import Popen, PIPE

class SearchPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2

        self.add_widget(Label(text = "Song:"))

        self.song = TextInput(multiline = False)
        self.add_widget(self.song)

        self.add_widget(Label(text = "Artist:"))

        self.artist = TextInput(multiline = False)
        self.add_widget(self.artist)

        self.submit = Button(text = "Search")
        
        self.add_widget(self.submit)
        self.submit.bind(on_press = self.onButtonPress)

    def onButtonPress(self, event):
        self.lyrics = Lyric_Finder.browserInstance_faster(self.artist.text, self.song.text)

        while self.lyrics == "Try again" or self.lyrics is None:
            self.lyrics = Lyric_Finder.browserInstance_faster(self.artist.text, self.song.text)

        lyrics_file = open('versuri.adi', 'w')
        lyrics_file.write(self.lyrics)
        lyrics_file.close()

        process = Popen(['python3', 'lyrics.py'], stdout=PIPE, stderr=PIPE)

    def getLyrics(self):
        return self.lyrics

class Menu(App):
    def build(self):
        return SearchPage()

if __name__ == "__main__":
    Menu().run()