import tkinter
import customtkinter
import configobj
import os


def fist_time_startup():

    if not os.path.isfile('config.ini'):
        set_default_config_values()


def set_default_config_values():
    root = tkinter.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    config = configobj.ConfigObj('config.ini')
    config['GENERAL'] = {
         'scan_limit': 1000,
         'relic_output_dir': 'relics/',
         'box_editor_output_dir': 'boxes/',
         'app_window_scale': 0.6
    }
    config['ADVANCED'] = {
        'consecutive_threshold': 3,
        'main_screen_width': screen_width,
        'main_screen_height': screen_height
    }
    config['Bounding Boxes'] = {
        'relic_set': {'left': 0, 'top': 0.85, 'width': 1, 'height': 0.14},
        'sub_stat_names': {'left': 0.11, 'top': 0.6, 'width': 0.4, 'height': 0.3},
        'sub_stat_numbers': {'left': 0.76, 'top': 0.61, 'width': 0.4, 'height': 0.28},
        'relic_main_stat_name': {'left': 0.11, 'top': 0.53, 'width': 0.6, 'height': 0.07},
        'relic_slot': {'left': 0.05, 'top': 0.3, 'width': 0.4, 'height': 0.07},
        'relic_level': {'left': 0.07, 'top': 0.38, 'width': 0.2, 'height': 0.07},
        'relic_area': {'left': 0.72, 'top': 0.98, 'width': 0.1, 'height': 0.6},
        'menu_area': {'left': 0.05, 'top': 0.06, 'width': 0.15, 'height': 0.1},
    }

    config.write()
def init_app():
    config = configobj.ConfigObj('config.ini')

    customtkinter.set_appearance_mode('System')
    customtkinter.set_default_color_theme('blue')
    root = customtkinter.CTk()
    root.title('Relic Scanner')

    # set screen resolution
    window_width = round(config['ADVANCED'].as_int('main_screen_width') * config['GENERAL'].as_float('app_window_scale'))
    widow_height = round(config['ADVANCED'].as_int('main_screen_height') * config['GENERAL'].as_float('app_window_scale'))

    screen_resolution = f'{window_width}x{widow_height}'
    root.geometry(screen_resolution)

    root.mainloop()
