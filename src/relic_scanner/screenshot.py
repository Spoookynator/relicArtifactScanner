import logging


def capure_screenshot(camera, app_config, area_name):
    width = app_config["GENERAL"].as_int("main_screen_width")
    height = app_config["GENERAL"].as_int("main_screen_height")

    left = round(width * app_config['Bounding Boxes'][area_name].as_float("left"))
    top = round(height * app_config['Bounding Boxes'][area_name].as_float("top"))
    right = round(width * app_config['Bounding Boxes'][area_name].as_float("width"))
    bottom = round(height * app_config['Bounding Boxes'][area_name].as_float("height"))

    logging.debug(f'Captured Screenshot. Region = (left: {left}, top: {top}, right:{right}, bottom: {bottom})')
    region = (left, top, right, bottom)
    return camera.grab(region=region)
