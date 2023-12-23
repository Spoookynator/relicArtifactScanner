import pytesseract


def get_set_name(INPUT_IMAGE, BOUNDING_BOXES):
    height, width, channels = INPUT_IMAGE.shape

    x = round(width * BOUNDING_BOXES["left"])
    y = round(height * BOUNDING_BOXES["top"])

    w = round(width * BOUNDING_BOXES["width"])
    h = round(height * BOUNDING_BOXES["height"])

    crop_img = INPUT_IMAGE[y:y + h, x:x + w]

    img_string = pytesseract.image_to_string(crop_img)

    return img_string


def get_sub_stats_names(INPUT_IMAGE, BOUNDING_BOXES):
    height, width, channels = INPUT_IMAGE.shape

    x = round(width * BOUNDING_BOXES["left"])
    y = round(height * BOUNDING_BOXES["top"])

    w = round(width * BOUNDING_BOXES["width"])
    h = round(height * BOUNDING_BOXES["height"])

    crop_img = INPUT_IMAGE[y:y + h, x:x + w]

    img_string = pytesseract.image_to_string(crop_img, config="--psm 12")

    # print(img_string)
    # cv2.imshow('testo', crop_img)
    # cv2.waitKey(0)
    return img_string


def get_sub_stats_numbers(INPUT_IMAGE, BOUNDING_BOXES):
    height, width, channels = INPUT_IMAGE.shape

    x = round(width * BOUNDING_BOXES["left"])
    y = round(height * BOUNDING_BOXES["top"])

    w = round(width * BOUNDING_BOXES["width"])
    h = round(height * BOUNDING_BOXES["height"])

    crop_img = INPUT_IMAGE[y:y + h, x:x + w]

    img_string = pytesseract.image_to_string(crop_img, config="--psm 6")

    # print(img_string)
    # cv2.imshow('testo', crop_img)
    # cv2.waitKey(0)
    return img_string


def get_main_stat_name(INPUT_IMAGE, BOUNDING_BOXES):
    height, width, channels = INPUT_IMAGE.shape

    x = round(width * BOUNDING_BOXES["left"])
    y = round(height * BOUNDING_BOXES["top"])

    w = round(width * BOUNDING_BOXES["width"])
    h = round(height * BOUNDING_BOXES["height"])

    crop_img = INPUT_IMAGE[y:y + h, x:x + w]

    # two different images, since DEF got ignored by the first one (was too short)
    # so the second one checks for all the smaller words (gets checked later anyway, so trash can go in)
    img_string = pytesseract.image_to_string(crop_img, config="--psm 7")
    img_string2 = pytesseract.image_to_string(crop_img, config="--psm 8")

    full_img_string = img_string2 + img_string

    # cv2.imshow('testo', crop_img)
    # cv2.waitKey(0)
    return full_img_string


# noinspection SpellCheckingInspection
def get_main_stat_number(INPUT_IMAGE, BOUNDING_BOXES):
    height, width, channels = INPUT_IMAGE.shape

    x = round(width * BOUNDING_BOXES["left"])
    y = round(height * BOUNDING_BOXES["top"])

    w = round(width * BOUNDING_BOXES["width"])
    h = round(height * BOUNDING_BOXES["height"])

    crop_img = INPUT_IMAGE[y:y + h, x:x + w]

    # this just whitelists all numbers/symbols that could be in the number
    img_string = pytesseract.image_to_string(crop_img, config="tessedit_char_whitelist=0123456789%.")

    # print(img_string)
    # print("-----")

    # cv2.imshow('testo', crop_img)
    # cv2.waitKey(0)
    return img_string


def get_slot_name(INPUT_IMAGE, BOUNDING_BOXES):
    height, width, channels = INPUT_IMAGE.shape

    x = round(width * BOUNDING_BOXES["left"])
    y = round(height * BOUNDING_BOXES["top"])

    w = round(width * BOUNDING_BOXES["width"])
    h = round(height * BOUNDING_BOXES["height"])

    crop_img = INPUT_IMAGE[y:y + h, x:x + w]

    # this just whitelists all numbers/symbols that could be in the number
    img_string = pytesseract.image_to_string(crop_img)

    # print(img_string)
    # print("-----")
    #
    # cv2.imshow('testo', crop_img)
    # cv2.waitKey(0)
    return img_string


# noinspection SpellCheckingInspection
def get_level(INPUT_IMAGE, BOUNDING_BOXES):
    height, width, channels = INPUT_IMAGE.shape

    x = round(width * BOUNDING_BOXES["left"])
    y = round(height * BOUNDING_BOXES["top"])

    w = round(width * BOUNDING_BOXES["width"])
    h = round(height * BOUNDING_BOXES["height"])

    crop_img = INPUT_IMAGE[y:y + h, x:x + w]

    # this just whitelists all numbers/symbols that could be in the number
    img_string = pytesseract.image_to_string(crop_img, config="tessedit_char_whitelist=0123456789 --psm 12")

    return img_string


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
