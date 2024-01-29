def capture_relic(camera, APP_CONFIG):
    width = APP_CONFIG["ADVANCED"]["main_screen_width"]
    height = APP_CONFIG["ADVANCED"]["main_screen_height"]

    left = round(width * APP_CONFIG['Bounding Boxeds']['relic_area'].as_float("left"))
    top = round(height * APP_CONFIG['Bounding Boxeds']['relic_area'].as_float("top"))
    right = round(width * APP_CONFIG['Bounding Boxeds']['relic_area'].as_float("right"))
    bottom = round(height * APP_CONFIG['Bounding Boxeds']['relic_area'].as_float("bottom"))

    region = (left, top, right, bottom)
    image = camera.grab(region=region)

    return image


def inventory_menu(camera, app_config):
    width = app_config["ADVANCED"].as_int("main_screen_width")
    height = app_config["ADVANCED"].as_int("main_screen_height")

    left = round(width * app_config['Bounding Boxes']['menu_area'].as_float("left"))
    top = round(height * app_config['Bounding Boxes']['menu_area'].as_float("top"))
    right = round(width * app_config['Bounding Boxes']['menu_area'].as_float("right"))
    bottom = round(height * app_config['Bounding Boxes']['menu_area'].as_float("bottom"))

    region = (left, top, right, bottom)
    return camera.grab(region=region)
