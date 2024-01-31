import customtkinter
import configobj


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
        self.scanner_frame = ScanPage(master=self, fg_color='transparent')
        self.scanner_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    def reload_user_config(self):
        self.user_config = configobj.ConfigObj('config.ini')


class ScanPage(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # configure grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=10)

        self.nav_bar_container = NavBarContainer(self)
        self.nav_bar_container.grid(row=0, column=0, sticky='nsw')

        self.main_interaction_container = MainInteractionContainer(self)
        self.main_interaction_container.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')


class MainInteractionContainer(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.stats_container = StatsContainer(self, fg_color="transparent")
        self.stats_container.grid(column=0, row=0, sticky='nsew', columnspan=3)

        self.start_scan_button = customtkinter.CTkButton(self, text='Scan Relics', font=('', 50), corner_radius=10)
        self.start_scan_button.grid(row=1, column=1, sticky='nsew')
        self.start_scan_button.grid_propagate(False)


class StatsContainer(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.scanned_relics_label = StatInfoContainer(self, 'Relics Scanned', 30)
        self.scanned_relics_label.grid(row=0, column=0, sticky='nesw')
        self.scanned_relics_label.status_text.set('--')

        self.scanned_relics_success_rate = StatInfoContainer(self, 'Success Rate', 30)
        self.scanned_relics_success_rate.grid(row=0, column=1, sticky='nesw')
        self.scanned_relics_success_rate.status_text.set('--%')

        self.scanned_relics_time_elapsed = StatInfoContainer(self, 'Time Elapsed', 30)
        self.scanned_relics_time_elapsed.grid(row=1, column=0, sticky='nesw')
        self.scanned_relics_time_elapsed.status_text.set('--s')

        self.current_status = StatInfoContainer(self, 'Status', 30)
        self.current_status.grid(row=1, column=1, sticky='nesw')
        self.current_status.status_text.set('Not running')


class StatInfoContainer(customtkinter.CTkFrame):
    def __init__(self, master, label_text, font_size, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.status_text = customtkinter.StringVar()

        self.grid_propagate(False)
        self.label = customtkinter.CTkLabel(self, text=label_text, font=('', font_size))
        self.label.grid(row=0, column=0, sticky='news')
        self.text = customtkinter.CTkLabel(self, font=('', font_size), textvariable=self.status_text)
        self.text.grid(row=1, column=0, sticky='new')



class NavBarContainer(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        hover_color = '#252633'

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=4)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=3)
        self.grid_rowconfigure(6, weight=1)

        self.relic_inventory_button = customtkinter.CTkButton(self, text="Relic Inventory", corner_radius=10, fg_color='transparent', hover_color=hover_color)

        self.relic_inventory_button.grid(row=1, column=0, sticky='ns')

        self.relic_scanner_button = customtkinter.CTkButton(self, text="Relic Scanner", corner_radius=10, fg_color='transparent', state='normal', hover_color=hover_color)
        self.relic_scanner_button.grid(row=3, column=0, sticky='ns')

        self.advanced_option_button = customtkinter.CTkButton(self, text="Advanced", corner_radius=10, fg_color='transparent', hover_color=hover_color)
        self.advanced_option_button.grid(row=5, column=0, sticky='ns')
