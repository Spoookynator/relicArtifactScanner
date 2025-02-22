import logging

import app
import src.init


def main():
    logging.basicConfig(format="[%(filename)s - %(funcName)s() ] %(message)s", level=logging.DEBUG)
    src.init.fist_time_startup()
    App = app.App()

    App.mainloop()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(format(e))
        input()
