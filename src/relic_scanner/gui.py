import customtkinter


class ScanPage(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # configure grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=10)

        self.f_nav_bar = NavBarContainer(self)
        self.f_nav_bar.grid(row=0, column=0, sticky='nsw')

        self.f_interaction = MainInteractionContainer(self)
        self.f_interaction.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')


class MainInteractionContainer(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.f_stats = StatsContainer(self, fg_color="transparent")
        self.f_stats.grid(column=0, row=0, sticky='nsew', columnspan=3)

        self.btn_start_scan = customtkinter.CTkButton(self, text='Scan Relics', font=('', 50), corner_radius=10)
        self.btn_start_scan.grid(row=1, column=1, sticky='nsew')
        self.btn_start_scan.grid_propagate(False)


class StatsContainer(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.f_scanned_relics = StatInfoContainer(self, 'Relics Scanned', 30)
        self.f_scanned_relics.grid(row=0, column=0, sticky='nesw')
        self.f_scanned_relics.var_status_text.set('--')

        self.f_success_rate = StatInfoContainer(self, 'Success Rate', 30)
        self.f_success_rate.grid(row=0, column=1, sticky='nesw')
        self.f_success_rate.var_status_text.set('--%')

        self.f_time_elapsed = StatInfoContainer(self, 'Time Elapsed', 30)
        self.f_time_elapsed.grid(row=1, column=0, sticky='nesw')
        self.f_time_elapsed.var_status_text.set('--s')

        self.f_current_status = StatInfoContainer(self, 'Status', 30)
        self.f_current_status.grid(row=1, column=1, sticky='nesw')
        self.f_current_status.var_status_text.set('Not running')


class StatInfoContainer(customtkinter.CTkFrame):
    def __init__(self, master, label_text, font_size, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.var_status_text = customtkinter.StringVar()

        self.grid_propagate(False)
        self.lbl_header = customtkinter.CTkLabel(self, text=label_text, font=('', font_size))
        self.lbl_header.grid(row=0, column=0, sticky='news')
        self.lbl_message = customtkinter.CTkLabel(self, font=('', font_size), textvariable=self.var_status_text)
        self.lbl_message.grid(row=1, column=0, sticky='new')


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

        self.btn_relic_inventory = customtkinter.CTkButton(self, text="Relic Inventory", corner_radius=10, fg_color='transparent', hover_color=hover_color)

        self.btn_relic_inventory.grid(row=1, column=0, sticky='ns')

        self.btn_relic_scanner = customtkinter.CTkButton(self, text="Relic Scanner", corner_radius=10, fg_color='transparent', state='normal', hover_color=hover_color)
        self.btn_relic_scanner.grid(row=3, column=0, sticky='ns')

        self.btn_advanced_options = customtkinter.CTkButton(self, text="Advanced", corner_radius=10, fg_color='transparent', hover_color=hover_color)
        self.btn_advanced_options.grid(row=5, column=0, sticky='ns')
