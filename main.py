import controls
import time
import init


def main():
    init.first_time_setup()
    BOUNDING_BOXES, WHITELIST, CONFIG = init.load_config()

    if BOUNDING_BOXES is None or WHITELIST is None or CONFIG is None:
        print("Error, extiting...")
        time.sleep(2)
        return -1

    controls.menu(BOUNDING_BOXES, WHITELIST, CONFIG)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        input()
