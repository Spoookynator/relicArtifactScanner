import logging

import customtkinter


class Tab(customtkinter.CTkFrame):
    def __init__(self, master, user_config, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=3)

        self.user_config = user_config


class NavBar(customtkinter.CTkFrame):
    def __init__(self, master, user_config, **kwargs):
        super().__init__(master, **kwargs)

        self.user_config = user_config

        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.v_relic_inventory = NavBarOption(self, fg_color='transparent', dispay_text='Inventory', user_config=self.user_config)
        self.v_relic_inventory.grid(row=0, column=0, sticky='ns')

        self.v_relic_scanner = NavBarOption(self, fg_color='transparent', dispay_text='Scanner', user_config=self.user_config)
        self.v_relic_scanner.grid(row=1, column=0, sticky='ns')

        self.v_box_editor = NavBarOption(self, fg_color='transparent', dispay_text='Editor', user_config=self.user_config)
        self.v_box_editor.grid(row=2, column=0, sticky='ns')

        self.v_settings = NavBarOption(self, fg_color='transparent', dispay_text='Settings', user_config=self.user_config)
        self.v_settings.grid(row=3, column=0, sticky='ns')

    def disable_all_navigation(self):
        self.v_relic_inventory.disable_navigation()
        self.v_relic_scanner.disable_navigation()
        self.v_box_editor.disable_navigation()
        self.v_settings.disable_navigation()

    def enable_all_navigation(self):
        self.v_relic_inventory.enable_navigation()
        self.v_relic_scanner.enable_navigation()
        self.v_box_editor.enable_navigation()
        self.v_settings.enable_navigation()

    def set_current_tab(self, position: int):
        self.enable_all_navigation()

        match position:
            case 0:
                self.v_relic_inventory.disable_navigation()
            case 1:
                self.v_relic_scanner.disable_navigation()
            case 2:
                self.v_box_editor.disable_navigation()
            case 3:
                self.v_settings.disable_navigation()
            case _:
                logging.warning('Tab not found')


class NavBarOption(customtkinter.CTkFrame):
    def __init__(self, master, dispay_text, user_config, **kwargs):
        super().__init__(master, **kwargs)

        self.user_config = user_config

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.btn_switch_view = customtkinter.CTkButton(self,
                                                       text=dispay_text,
                                                       corner_radius=0,
                                                       state='normal',
                                                       fg_color='transparent',
                                                       hover_color=self.user_config['Appearance']['accent'],
                                                       text_color=self.user_config['Appearance']['text']
                                                       )
        self.btn_switch_view.grid(row=0, column=0, sticky='nesw')

    def disable_navigation(self):
        self.btn_switch_view.configure(self, state='disabled')

    def enable_navigation(self):
        self.btn_switch_view.configure(self, state='normal')
