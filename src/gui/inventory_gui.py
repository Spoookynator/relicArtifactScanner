import numpy as np

import src.base_classes.gui
import customtkinter
from PIL import Image


class InventoryGui(src.base_classes.gui.Tab):
    def __init__(self, master, user_config, **kwargs):
        super().__init__(master, user_config, **kwargs)
        self.f_main_interaction = MainFrame(master=self, user_config=user_config)
        self.f_main_interaction.grid(row=0, column=1, sticky='nsew')


class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master, user_config, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=40)
        self.grid_rowconfigure(1, weight=100)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=100)
        self.grid_columnconfigure(2, weight=1)

        self.f_inventory_window = InventoryWindow(self,
                                                  fg_color=user_config['Appearance']['secondary'])
        self.f_inventory_window.grid(row=1, column=1, sticky='nsew')


class InventoryWindow(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)
        self.grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.img = np.zeros((50, 500, 3), dtype=np.uint8)
        self.img = Image.fromarray(self.img)
        self.img_test = customtkinter.CTkImage(dark_image=self.img, size=(100, 100))

        self.l_screenshot = customtkinter.CTkLabel(self, image=self.img_test, text='')
        self.l_screenshot.grid(column=0, row=0, padx=10, pady=10)

        self.l_screenshot = customtkinter.CTkLabel(self, image=self.img_test, text='')
        self.l_screenshot.grid(column=0, row=1, padx=10, pady=10)
