#-*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty 
from kivy.uix.boxlayout import BoxLayout

class PopupMenu(BoxLayout):
    popup_close = ObjectProperty(None)

class TextWidget(BoxLayout):
    text = StringProperty()    # プロパティの追加

    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)
        self.text = ''

    def buttonClicked(self):
        self.text = 'Good morning'

    def buttonClicked2(self):
        self.text = 'Hello'

    def buttonClicked3(self):
        self.text = 'Good evening'

    def popup_open(self):
        content = PopupMenu(popup_close=self.popup_close)
        self.popup = Popup(title='Popup Test', content=content, size_hint=(0.5, 0.5), auto_dismiss=False)
        self.popup.open()

    def popup_close(self):
        self.popup.dismiss()


class TimerApp(App):
    def __init__(self, **kwargs):
        super(TimerApp, self).__init__(**kwargs)
        self.title = 'greeting'

    def build(self):
        return TextWidget()

if __name__ == '__main__':
    TimerApp().run()

