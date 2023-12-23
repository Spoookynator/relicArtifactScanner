import os

import dxcam
import screenshot
from PIL import Image


def create_curent_box_imgs(BOUNDING_BOXES, CONFIG):
    camera = dxcam.create()
    directory = CONFIG["GENERAL"]["box_editor_dir"]
    os.makedirs(directory, exist_ok=True)

    relic_zone = screenshot.capture_relic(camera, BOUNDING_BOXES["RELIC"], CONFIG)
    save_img(relic_zone, directory, "relic_zone")

    menu_screenshot = screenshot.capture_relic(camera, BOUNDING_BOXES["MENU"], CONFIG)
    save_img(menu_screenshot, directory, "menu_screenshot")

    save_images(relic_zone, BOUNDING_BOXES, directory)


def save_img(img, directory, img_name):
    relic_zone_img = Image.fromarray(img)
    img_path = f"{directory}{img_name}.jpeg"
    relic_zone_img.save(img_path)


def crop_img(INPUT_IMAGE, BOUNDING_BOXES):
    height, width, channels = INPUT_IMAGE.shape

    x = round(width * BOUNDING_BOXES["left"])
    y = round(height * BOUNDING_BOXES["top"])

    w = round(width * BOUNDING_BOXES["width"])
    h = round(height * BOUNDING_BOXES["height"])

    cropped_image = INPUT_IMAGE[y:y + h, x:x + w]
    return cropped_image


def save_images(initial_img, BOUNDING_BOXES, directory):
    for key, value in BOUNDING_BOXES.items():
        if key == "MENU" or key == "RELIC":
            continue

        cropped_img = crop_img(initial_img, value)
        save_img(cropped_img, directory, key.lower())
