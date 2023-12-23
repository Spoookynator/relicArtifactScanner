import tkinter

import config_handler


def load_config():
    try:
        BOUNDING_BOXES = config_handler.read_bounding_box_file("./config/advanced_options/relic_bounding_boxes.bbox")
        WHITELIST = config_handler.read_whitelist_file("./config/advanced_options/whitelist.whtlst")
        CONFIG = config_handler.read_config_file("./config/config.user")

        return BOUNDING_BOXES, WHITELIST, CONFIG

    except FileNotFoundError:
        print(f"Critical Error: One ore more configs not found")
        return None, None, None


def first_time_setup():
    config_path = "./config/config.user"
    CONFIG = config_handler.read_config_file(config_path)

    if CONFIG["GENERAL"]["completed_first_startup"]:
        return

    screen_dimensions = get_screen_size()

    CONFIG["GENERAL"]["screen_width"] = screen_dimensions["width"]
    CONFIG["GENERAL"]["screen_height"] = screen_dimensions["height"]

    CONFIG["GENERAL"]["completed_first_startup"] = True

    config_handler.write_config_file(config_path, CONFIG)
    return


def get_screen_size():
    root = tkinter.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    return {"width": screen_width, "height": screen_height}
