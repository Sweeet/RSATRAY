from infi.systray import SysTrayIcon
from pysdtoken import SDProcess
import configparser
import clipboard
import sys, os

config = configparser.ConfigParser()

def write_file():
   config.write(open('config.ini', 'w'))

def conf_Init():
   if not os.path.exists('config.ini'):
      config['testing'] = {'pin': 'changeme', 'stauto-dir': 'C:\Program Files\RSA SecurID Token Common\stauto32.dll'}
      write_file()
   else:
      config.read('config.ini')
      return config.get('testing', 'pin'), config.get('testing', 'stauto-dir')


def resource_path(relative_path):
   """ Get absolute path to resource, works for dev and for PyInstaller """
   base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
   return os.path.join(base_path, relative_path)

def get_token(systray, next):
    sd = SDProcess(pin_style='PINPad-style', dll_name=settings[1])

    my_token = sd.get_default_token()
    if next == True:
       next_code = my_token.get_next_code(settings[0]).passcode
    #    print(next_code)
       clipboard.copy(next_code)
    else:
        current_code = my_token.get_current_code(settings[0]).passcode
        # print(current_code)
        clipboard.copy(current_code)

if __name__ == "__main__":
   settings = conf_Init()
   image_path = resource_path("lock.ico")
   menu_options = (("Get Token", None, lambda x: get_token(systray, next=False)),("Get Next Token", None, lambda x: get_token(systray, next=True)),)
   systray = SysTrayIcon(image_path, "Example tray icon", menu_options)
   systray.start()
