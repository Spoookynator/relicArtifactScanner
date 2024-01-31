import pytesseract


def relic_img_to_string(input_img, bounding_box, tesseract_config='', tesseract_config_2='', double_check=False):
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


def read_config_file(file_path):
    config_data = {}

    try:
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split()
                config_data[key] = float(value)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except ValueError:
        print(f"Error parsing file. Ensure each line has the format 'key value': {file_path}")

    return config_data
