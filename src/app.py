import logging

import customtkinter
import configobj
import dxcam

from src.base_classes.gui import NavBar
from src.gui.box_editor_gui import BoxEditorGui
from src.gui.inventory_gui import InventoryGui
from src.gui.relic_scanner_gui import RelicScannerGui
from src.relic_scanner.controls import start_scan_loop_thread


class App(customtkinter.CTk):
    def __init__(self):
        self.UserConfig = configobj.ConfigObj('config.ini')
        self.camera = dxcam.create()

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
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=3)

        self.f_nav_bar = NavBar(self, fg_color=self.UserConfig['Appearance']['secondary'], width=30, user_config=self.UserConfig)
        self.f_nav_bar.grid(row=0, column=0, sticky='nsw')

        self.f_nav_bar.v_relic_inventory.btn_switch_view.configure(command=lambda: self.set_frame(0))
        self.f_nav_bar.v_relic_scanner.btn_switch_view.configure(command=lambda: self.set_frame(1))
        self.f_nav_bar.v_box_editor.btn_switch_view.configure(command=lambda: self.set_frame(2))
        self.f_nav_bar.v_settings.btn_switch_view.configure(command=lambda: self.set_frame(3))

        self.f_box_editor = BoxEditorGui(master=self, user_config=self.UserConfig, fg_color='transparent', camera=self.camera)
        self.f_box_editor.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        self.f_scanner = RelicScannerGui(master=self, user_config=self.UserConfig, fg_color='transparent')
        self.f_scanner.grid(row=0, column=1, sticky='nsew')

        self.f_inventory = InventoryGui(master=self, user_config=self.UserConfig, fg_color='transparent')
        self.f_inventory.grid(row=0, column=1, sticky='nsew')

        self.set_frame(0)
        self.f_scanner.f_main_interaction.btn_start_scan.configure(command=lambda: start_scan_loop_thread(self))

    def set_frame(self, index: int):
        match index:
            case 0:
                self.f_nav_bar.set_current_tab(0)
                self.f_inventory.tkraise()
                logging.debug("switched to inventory")

            case 1:
                self.f_nav_bar.set_current_tab(1)
                self.f_scanner.tkraise()
                logging.debug("switched to scanner")

            case 2:
                self.f_nav_bar.set_current_tab(2)
                self.f_box_editor.tkraise()
                logging.debug("switched to box_editor")
                self.f_box_editor.f_main_interaction.create_boxes(3)

            case 3:
                self.f_nav_bar.set_current_tab(3)
                logging.debug("switched to settings")

            case _:
                logging.warning('Tab not found')