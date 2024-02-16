from PIL import Image

import src.base_classes.gui
import customtkinter
import dxcam

from src.relic_scanner import screenshot
from src.relic_scanner.ocr_functions import get_box_values


class BoxEditorGui(src.base_classes.gui.Tab):
    def __init__(self, master, user_config, **kwargs):
        super().__init__(master, user_config, **kwargs)

        self.f_nav_bar.set_current_tab(2)
        self.f_main_interaction = MainFrame(master=self, user_config=user_config)
        self.f_main_interaction.grid(row=0, column=1, sticky='nsew')


class MainFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, user_config, **kwargs):
        super().__init__(master, **kwargs)
        self.camera = dxcam.create()
        self.user_config = user_config
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

    def create_boxes(self, max_column_count):
        areas_array = []
        for entry in self.user_config['Bounding Boxes']:
            f_area = BoxContainer(self, user_config=self.user_config,
                                  fg_color=self.user_config['Appearance']['primary'],
                                  label_text=entry, area=entry, camera=self.camera)
            areas_array.append(f_area)

        max_column_count = max_column_count  # 3 is prolly the best number

        current_column = 0
        current_row = 0
        for area in areas_array:
            if current_column == max_column_count:
                current_row += 1
                current_column = 0

            area.grid(column=current_column, row=current_row)

            current_column += 1


def callback(P):
    try:
        float(P)
        if float(P) > 1 or float(P) < 0:
            return False
        return True
    except ValueError:
        return False


class BoxContainer(customtkinter.CTkFrame):
    def __init__(self, master, user_config, label_text, area, camera, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.l_box_name = customtkinter.CTkLabel(self, text_color='black', text=label_text)
        self.l_box_name.grid(columnspan=2, column=0, row=0)

        self.v_screenshot = screenshot.capure_screenshot(camera, user_config, 'relic_area')

        if area == 'menu_area':
            self.v_screenshot = screenshot.capure_screenshot(camera, user_config, 'menu_area')

        if area != 'menu_area' and area != 'relic_area':
            height, width, channels = self.v_screenshot.shape
            x, y, w, h = get_box_values(width=width, height=height, bounding_box=user_config['Bounding Boxes'][area])
            self.v_screenshot = self.v_screenshot[y:y + h, x:x + w]

        self.v_screenshot_width, self.v_screenshot_height, self.v_screenshot_channels = self.v_screenshot.shape

        self.i_screenshot = customtkinter.CTkImage(dark_image=Image.fromarray(self.v_screenshot),
                                                   size=(self.v_screenshot_height, self.v_screenshot_width))
  
        self.l_screenshot = None

        self.e_left = EntryContainer(self, user_config=user_config, area=area, label_text='left',
                                     fg_color='transparent')
        self.e_top = EntryContainer(self, user_config=user_config, area=area, label_text='top', fg_color='transparent')
        self.e_width = EntryContainer(self, user_config=user_config, area=area, label_text='width',
                                      fg_color='transparent')
        self.e_height = EntryContainer(self, user_config=user_config, area=area, label_text='height',
                                       fg_color='transparent')

        self.e_left.grid(column=0, row=2, sticky='ew')
        self.e_top.grid(column=1, row=2, sticky='ew')
        self.e_width.grid(column=0, row=3, sticky='ew')
        self.e_height.grid(column=1, row=3, sticky='ew')

    def display_screenshot(self):
        self.l_screenshot = customtkinter.CTkLabel(self, image=self.i_screenshot, text='')
        self.l_screenshot.grid(columnspan=2, column=0, row=1)



class EntryContainer(customtkinter.CTkFrame):
    def __init__(self, master, user_config, label_text, area, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        vcmd = (self.register(callback))

        self.v_entry_width = 40
        self.e_entry = customtkinter.CTkEntry(self, validate='all',
                                              validatecommand=(vcmd, '%P'),
                                              placeholder_text=user_config["Bounding Boxes"][
                                                  area].as_float(label_text), width=self.v_entry_width)

        self.l_label = customtkinter.CTkLabel(self, text=label_text, text_color='black')

        self.l_label.grid(row=0, column=0, sticky='w', padx=5)
        self.e_entry.grid(row=0, column=1, sticky='e')

    def get_input_number(self):
        return self.e_entry.cget('placeholder_text')
