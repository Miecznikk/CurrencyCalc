from kivymd.app import MDApp
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFlatButton, MDFillRoundFlatButton
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField
from kivy.network.urlrequest import UrlRequest
from kivymd.theming import ThemeManager
import re
from api import NbpApi
from functools import partial


NBP_API = NbpApi()


class MyToggleButton(MDFlatButton,MDToggleButton):
    def __init__(self,*args,**kwargs):
        super(MyToggleButton, self).__init__(*args,**kwargs)
        self.background_down = self.theme_cls.primary_color

class FloatInput(MDTextField):
    pat = re.compile('[^0-9]')
    multiline = False
    halign = "center"

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat,'',substring)
        else:
            s='.'.join(re.sub(pat,'',s) for s in substring.split('.',1))
        return super().insert_text(s,from_undo=from_undo)


class MainScreen(MDScreen):
    def __init__(self,**kwargs):
        super(MainScreen, self).__init__(**kwargs)


class CurrencyScreen(MDScreen):
    to_pln = False
    current_rate = 0
    code = ""

    def __init__(self,**kwargs):
        super(CurrencyScreen, self).__init__(**kwargs)

    def switch(self):
        if not self.to_pln:
            self.to_pln = True
            self.ids.input.hint_text = "Podaj wartość w PLN"
        else:
            self.to_pln = False
            self.ids.input.hint_text = f"Podaj wartość w {self.code}"

    def calc(self):
        if self.ids.input.text!='':
            if not self.to_pln:
                self.ids.result.text = f'{round(float(self.ids.input.text) * self.current_rate,2)} PLN'
            else:
                self.ids.result.text = f'{round(float(self.ids.input.text) * 1 / self.current_rate,2)} {self.code}'

class UsdScreen(CurrencyScreen):
    def __init__(self,**kwargs):
        super(UsdScreen, self).__init__(**kwargs)
        self.name = 'usd'
        self.code = "USD"
        self.current_rate=NBP_API.actual_rates['USD']
        #self.current_rate = 4.3811



class AudScreen(CurrencyScreen):
    def __init__(self, **kwargs):
        super(AudScreen, self).__init__(**kwargs)
        self.name ='aud'
        self.code = "AUD"
        self.current_rate = NBP_API.actual_rates['AUD']
        #self.current_rate = 2.9767

class EurScreen(CurrencyScreen):
    def __init__(self, **kwargs):
        super(EurScreen, self).__init__(**kwargs)
        self.name = 'eur'
        self.code = "EUR"
        self.current_rate = NBP_API.actual_rates['EUR']
        #self.current_rate = 4.6784

class CurrencyChartScreen(MDScreen):
    image_path = "foo.png"
    code=''

    def __init__(self,**kwargs):
        super(CurrencyChartScreen, self).__init__(**kwargs)

    def change_image(self,instance,value):
        if value == 'down':
            self.ids.chart_image.source = f'images/{self.code}/{instance.text.lower()}.png'

class WindowManager(MDScreenManager):
    pass


class UsdChartScreen(CurrencyChartScreen):
    def __init__(self, **kwargs):
        super(UsdChartScreen, self).__init__(**kwargs)
        self.code = 'USD'
        self.name = "usd_chart"
        self.image_path = 'images/USD/1m.png'


class AudChartScreen(CurrencyChartScreen):
    def __init__(self, **kwargs):
        super(AudChartScreen, self).__init__(**kwargs)
        self.code="AUD"
        self.name = "aud_chart"
        self.image_path = 'images/AUD/1m.png'


class EurChartScreen(CurrencyChartScreen):
    def __init__(self, **kwargs):
        super(EurChartScreen, self).__init__(**kwargs)
        self.code="EUR"
        self.name = "eur_chart"
        self.image_path = 'images/EUR/1m.png'

class MainApp(MDApp):
    def build(self):
        self.theme_cls = ThemeManager()
        self.theme_cls.theme_style="Light"
        self.theme_cls.primary_palette="Blue"
        return Builder.load_file('apka.kv')

if __name__ == '__main__':
    MainApp().run()