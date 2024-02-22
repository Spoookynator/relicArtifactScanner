import customtkinter
import configobj

from src.gui.box_editor_gui import BoxEditorGui
from src.relic_scanner.gui import ScanPage


class App(customtkinter.CTk):
    def __init__(self):
        self.UserConfig = configobj.ConfigObj('config.ini')

        super().__init__()

        # set appearance
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('blue')

        # set screen resolution
        window_width = round(
            self.UserConfig['GENERAL'].as_int('main_screen_width') * self.UserConfig['GENERAL'].as_float(
                'app_window_scale'))
        window_height = round(
            self.UserConfig['GENERAL'].as_int('main_screen_height') * self.UserConfig['GENERAL'].as_float(
                'app_window_scale'))
        screen_resolution = f'{window_width}x{window_height}'
        self.geometry(screen_resolution)

        # =====rest of the app=====
        self.title('Relic Scanner')

        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.f_scanner = ScanPage(master=self, fg_color='transparent')
        self.f_scanner.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        # self.f_box_editor = BoxEditorGui(master=self, user_config=self.UserConfig, fg_color='transparent')
        # self.f_box_editor.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
