import json
import os
import datetime

import src.relic_scanner.ocr_functions as ocr_functions
import src.relic_scanner.whitelist_check as whitelist_check
import src.relic_scanner.clean_extracted_information as clean_extracted_information
import re

def convert_img_to_relic(INPUT_IMAGE, APP_CONFIG):
    # is true when there is no error
    error_list = [None] * 9
    # the whitelists used to filter out relic sets and stats
    WHITELIST_MAIN_STAT_NAMES = APP_CONFIG['Whitelist']["relic_main_stat_names"]
    WHITELIST_POSSIBLE_PERCENT = APP_CONFIG['Whitelist']["possible_percent"]
    WHITELIST_SET = APP_CONFIG['Whitelist']["relic_sets"]
    WHITELIST_SLOT = APP_CONFIG['Whitelist']["slots"]
    WHITELIST_SUB_STAT_NAMES = APP_CONFIG['Whitelist']["sub_stat_names"]

    # uses ocr on the image, to get all the differenct relic parts into variables
    # bounding boxes are used to only analyze a certain part of the image

    relic_sub_stat_num_config = APP_CONFIG['Bounding Boxes']["sub_stat_numbers"]
    relic_sub_stat_name_config = APP_CONFIG['Bounding Boxes']["sub_stat_names"]
    relic_main_stat_name_config = APP_CONFIG['Bounding Boxes']["relic_main_stat_name"]
    relic_level_config = APP_CONFIG['Bounding Boxes']["relic_level"]
    relic_set_name_config = APP_CONFIG['Bounding Boxes']["relic_set"]
    relic_slot_name_config = APP_CONFIG['Bounding Boxes']["relic_slot"]

    relic_sub_stat_num_tesseract = APP_CONFIG['Tesseract']['relic_sub_stat_num']
    relic_sub_stat_name_tesseract = APP_CONFIG['Tesseract']['relic_sub_stat_name']
    relic_main_stat_name_1_tesseract = APP_CONFIG['Tesseract']['relic_main_stat_name_1']
    relic_main_stat_name_2_tesseract = APP_CONFIG['Tesseract']['relic_main_stat_name_2']
    relic_level_tesseract = APP_CONFIG['Tesseract']['relic_level']
    relic_set_name_tesseract = APP_CONFIG['Tesseract']['relic_set_name']
    relic_slot_name_tesseract = APP_CONFIG['Tesseract']['relic_slot_name']

    raw_sub_stat_numbers = ocr_functions.img_to_string(INPUT_IMAGE,
                                                       relic_sub_stat_num_config,
                                                       relic_sub_stat_num_tesseract)
    raw_sub_stat_names = ocr_functions.img_to_string(INPUT_IMAGE,
                                                     relic_sub_stat_name_config,
                                                     relic_sub_stat_name_tesseract
                                                     )
    raw_main_stat_name = ocr_functions.img_to_string(INPUT_IMAGE,
                                                     relic_main_stat_name_config,
                                                     relic_main_stat_name_1_tesseract,
                                                     relic_main_stat_name_2_tesseract,
                                                     True
                                                     )
    raw_set_name = ocr_functions.img_to_string(INPUT_IMAGE, relic_set_name_config, relic_set_name_tesseract)
    raw_slot_name = ocr_functions.img_to_string(INPUT_IMAGE, relic_slot_name_config, relic_slot_name_tesseract)
    raw_level = ocr_functions.img_to_string(INPUT_IMAGE, relic_level_config, relic_level_tesseract)

    slot_name, error_list[0] = whitelist_check.filter_slot_names(raw_slot_name,
                                                                 WHITELIST_SLOT)
    filtered_sub_stat_names, error_list[1] = whitelist_check.filter_sub_stat_names(raw_sub_stat_names,
                                                                                   WHITELIST_SUB_STAT_NAMES
                                                                                   )
    main_stat_name, error_list[2] = whitelist_check.check_main_stat_name(raw_main_stat_name,
                                                                         WHITELIST_MAIN_STAT_NAMES,
                                                                         WHITELIST_POSSIBLE_PERCENT,
                                                                         slot_name
                                                                         )
    set_name, error_list[3] = whitelist_check.check_set_name(raw_set_name, WHITELIST_SET)

    sub_stat_numbers, error_list[4] = clean_extracted_information.clean_sub_stat_numbers(raw_sub_stat_numbers)

    level, error_list[5] = clean_extracted_information.clean_level(raw_level)
    sub_stats_complete, error_list[6] = clean_extracted_information.sub_stats_flat_or_percent(filtered_sub_stat_names,
                                                                                              sub_stat_numbers,
                                                                                              WHITELIST_POSSIBLE_PERCENT
                                                                                              )
    sub_stat_object_list = []

    try:
        for i in range(len(sub_stats_complete["names"])):
            sub_stat_object = {"name": sub_stats_complete["names"][i], "value": sub_stats_complete["values"][i]}
            sub_stat_object_list.append(sub_stat_object)
            error_list[7] = True

    except Exception as e:
        error_list[7] = e

    final_relic = {"MainStat": main_stat_name, "Set": set_name, "Slot": slot_name, "Level": level,
                   "SubStats": sub_stat_object_list}

    true_final_relic, error_list[8] = convert_to_right_case(final_relic)

    return true_final_relic, check_if_error(error_list)


def check_if_error(input_list):
    errors = 0
    for entry in input_list:
        if entry != True:
            errors += 1
    return errors


def convert_to_right_case(relic):
    try:
        relic["MainStat"] = to_snake_case(relic["MainStat"])
        relic["Set"] = to_snake_case(relic["Set"])
        relic["Slot"] = to_snake_case(relic["Slot"])
        for element in relic["SubStats"]:
            element["name"] = to_snake_case(element["name"])
        return relic, True
    except Exception as e:
        return relic, e


def to_snake_case(input_string):
    # Replace "-", ":", and spaces with "_"
    modified_string = re.sub(r'[-:\s]', '_', input_string)

    # Replace other special characters with an empty string, except "_" and "%"
    modified_string = re.sub(r'[^\w%]', '', modified_string)

    lower_string = modified_string.lower()

    lower_string = lower_string.replace("__", "_")
    return lower_string


def write_relics_to_file(relics_list, directory, msg_status):
    try:
        relics_list_json = json.dumps(relics_list, indent=4)

        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

        path = f'{directory}{formatted_datetime}_relics.json'

        os.makedirs(directory, exist_ok=True)

        with open(path, "w") as f:
            f.write(relics_list_json)

        msg_status.set(f'Saved {len(relics_list)} relics to\n "{path}"')
    except Exception as e:
        msg_status.set("Failed to write relics to file.")
        print(f"Error: {format(e)}")
