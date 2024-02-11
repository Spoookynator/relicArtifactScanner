import pytesseract


def img_to_string(input_img, bounding_box, tesseract_config='', tesseract_config_2='', double_check=False):
    height, width, channels = input_img.shape
    x, y, w, h = get_box_values(width, height, bounding_box)

    crop_img = input_img[y:y + h, x:x + w]
    img_string = pytesseract.image_to_string(crop_img, config=tesseract_config)

    if double_check:
        img_string2 = pytesseract.image_to_string(crop_img, config=tesseract_config_2)
        return img_string2 + img_string

    return img_string


def get_box_values(width, height, bounding_box):
    x = round(width * bounding_box.as_float("left"))
    y = round(height * bounding_box.as_float("top"))

    w = round(width * bounding_box.as_float("width"))
    h = round(height * bounding_box.as_float("height"))

    return x, y, w, h


def get_menu(INPUT_IMAGE):
    img_string = pytesseract.image_to_string(INPUT_IMAGE)
    return img_string.strip()