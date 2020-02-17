import random
import kivy
kivy.require("1.11.1")
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.config import Config

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '400')

class Container(FloatLayout):
    pass

class ColorLabel(Label):
    pass

class Main(App):
    def build(self):
        Builder.load_file("main.kv")
        the_grid = GridLayout(cols=11, spacing=1)
        for _ in range(110):
            newLabel = ColorLabel()
            the_grid.add_widget(newLabel)
            if random.choice([True, False]):
                newLabel.bg_color = [0,0,0,1]
        root = Container()
        root.add_widget(the_grid)           
        return root

# Keep everything below this last!      
if __name__ == '__main__':
    Main().run()