import customtkinter
import configobj

from src.relic_scanner.gui import ScanPage


class App(customtkinter.CTk):
    def __init__(self):
        self.user_config = configobj.ConfigObj('config.ini')
        super().__init__()

        # set appearance
        customtkinter.set_appearance_mode('System')
        customtkinter.set_default_color_theme('blue')

        # set screen resolution
        window_width = round(
            self.user_config['GENERAL'].as_int('main_screen_width') * self.user_config['GENERAL'].as_float(
                'app_window_scale'))
        window_height = round(
            self.user_config['GENERAL'].as_int('main_screen_height') * self.user_config['GENERAL'].as_float(
                'app_window_scale'))
        screen_resolution = f'{window_width}x{window_height}'
        self.geometry(screen_resolution)

        # =====rest of the app=====
        self.title('Relic Scanner')

        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        # add frame
        self.f_scanner = ScanPage(master=self, fg_color='transparent')
        self.f_scanner.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    def reload_user_config(self):
        self.user_config = configobj.ConfigObj('config.ini')
