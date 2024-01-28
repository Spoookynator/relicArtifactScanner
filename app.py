import tkinter
import customtkinter
import configobj
import os


def fist_time_startup():
    if not os.path.isfile('config.ini'):
        initalize_config_values()


def initalize_config_values():
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

    config['Whitelist'] = {
        'relic_main_stat_names': [
            'ATK', 'Break Effect', 'CRIT DMG', 'CRIT RATE', 'DEF', 'Effect HIT Rate', 'Energy Regeneration Rate',
            'Fire DMG', 'HP', 'Ice DMG', 'Imaginary DMG', 'Lightning DMG', 'Outgoing Healing', 'Physical DMG',
            'Quantum DMG', 'SPD', 'Wind DMG'
        ],
        'possible_percent': [
            'ATK', 'DEF', 'HP'
        ],
        'relic_sets': [
            'Band of Sizzling Thunder', 'Belobog of the Architects', 'Broken Keel', 'Celestial Differentiator',
            'Champion of Streetwise Boxing', 'Eagle of Twilight Line', 'Firesmith of Lava Forging',
            'Firesmith of Lava-Forging', 'Firesmith of Lavaforging', 'Firmament Frontline Glamoth',
            'Firmament Frontline: Glamoth', 'Fleet of the Ageless', 'Genius of Brilliant Stars',
            'Guard of Wuthering Snow', 'Hunter of Glacial Forest', 'Inert Salsotto', 'Knight of Purity Palace',
            'Longevous Disciple', 'Messenger Traversing Hackerspace', 'Musketeer of Wild Wheat',
            'Pan Cosmic Commercial Enterprise', 'Pan-Cosmic Commercial Enterprise', 'Pancosmic Commercial Enterprise',
            'Passerby of Wandering Cloud', 'Penacony Land of the Dreams', 'Penacony, Land of the Dreams',
            'Prisoner in Deep Confinement', 'Rutilant Arena', 'Space Sealing Station', 'Sprightly Vonwacq',
            'Talia Kingdom of Banditry', 'Talia: Kingdom of Banditry', 'The Ashblazing Grand Duke',
            'Thief of Shooting Meteor', 'Wastelander of Banditry Desert', 'TEST LINE DO NOT REMOVE EVERYTHING BREAKS'
        ],
        'slots': [
            'Body', 'Feet', 'Hands', 'Head', 'Rope', 'Sphere'
        ],
        'sub_stat_names': [
            'ATK', 'Break Effect', 'CRIT DMG', 'CRIT Rate', 'DEF', 'Effect HIT Rate', 'Effect RES', 'HP', 'SPD'
        ]
    }

    config.write()


class App(customtkinter.CTk):
    def __init__(self):
        self.user_config = configobj.ConfigObj('config.ini')
        super().__init__()

        customtkinter.set_appearance_mode('System')
        customtkinter.set_default_color_theme('blue')
        self.title('Relic Scanenr')

        # set screen resolution
        window_width = round(
            self.user_config['ADVANCED'].as_int('main_screen_width') * self.user_config['GENERAL'].as_float(
                'app_window_scale'))
        widow_height = round(
            self.user_config['ADVANCED'].as_int('main_screen_height') * self.user_config['GENERAL'].as_float(
                'app_window_scale'))
        screen_resolution = f'{window_width}x{widow_height}'
        self.geometry(screen_resolution)

    def reload_user_config(self):
        self.user_config = configobj.ConfigObj('config.ini')


def add_app_frame():
    print()
