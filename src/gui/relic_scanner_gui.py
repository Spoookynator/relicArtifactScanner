import logging

import src.base_classes.gui
import customtkinter


class RelicScannerGui(src.base_classes.gui.Tab):
    def __init__(self, master, user_config, **kwargs):
        super().__init__(master, user_config, **kwargs)

        self.f_main_interaction = MainFrame(master=self, user_config=user_config)
        self.f_main_interaction.grid(row=0, column=1, sticky='nsew')

    def set_status_msg(self, text):
        self.f_main_interaction.f_stats.f_current_status.var_status_text.set(text)

    def set_relic_successes(self, text):
        self.f_main_interaction.f_stats.f_success_rate.var_status_text.set(text)

    def set_relic_amount(self, text):
        self.f_main_interaction.f_stats.f_scanned_relics.var_status_text.set(text)

    def set_time_elapsed(self, text):
        self.f_main_interaction.f_stats.f_time_elapsed.var_status_text.set(text)

    def enable_scan_button(self):
        self.f_main_interaction.btn_start_scan.configure(self, state='normal')
        logging.debug('Disabled scan button')

    def disable_scan_button(self):
        self.f_main_interaction.btn_start_scan.configure(self, state='disabled')
        logging.debug('Enabled scan button')


class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master, user_config, **kwargs):
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