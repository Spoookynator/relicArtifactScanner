import logging

import app
import src.init
from relic_scanner.controls import start_scan_loop_thread


def testerer():
    print('test')


def main():
    logging.basicConfig(format="[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")
    src.init.fist_time_startup()
    App = app.App()

    App.f_scanner.f_interaction.btn_start_scan.configure(command=lambda: start_scan_loop_thread(App))
    App.mainloop()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        input()
