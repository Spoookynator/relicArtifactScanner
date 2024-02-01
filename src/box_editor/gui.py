import customtkinter


class BoxEditor(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=10)

        self.f_nav_bar = NavBarContainer(self)
        self.f_nav_bar.grid(row=0, column=0, sticky='nsw')


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


# TODO finish this
class MainInteractionContainer(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)