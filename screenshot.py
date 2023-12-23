def capture_relic(camera, BOUNDING_BOXES, CONFIG):
    width = CONFIG["GENERAL"]["screen_width"]
    height = CONFIG["GENERAL"]["screen_height"]

    left = round(width * BOUNDING_BOXES["left"])
    top = round(height * BOUNDING_BOXES["top"])
    right = round(width * BOUNDING_BOXES["right"])
    bottom = round(height * BOUNDING_BOXES["bottom"])

    region = (left, top, right, bottom)
    image = camera.grab(region=region)

    return image


def inventory_menu(camera, BOUNDING_BOXES, CONFIG):
    width = CONFIG["GENERAL"]["screen_width"]
    height = CONFIG["GENERAL"]["screen_height"]

    left = round(width * BOUNDING_BOXES["left"])
    top = round(height * BOUNDING_BOXES["top"])
    right = round(width * BOUNDING_BOXES["right"])
    bottom = round(height * BOUNDING_BOXES["bottom"])

    region = (left, top, right, bottom)
    return camera.grab(region=region)