import json
import logging
import os
import datetime

import src.relic_scanner.ocr_functions as ocr_functions
import src.relic_scanner.whitelist_check as whitelist_check
import src.relic_scanner.clean_extracted_information as clean_extracted_information
import re
from src.base_classes.relic import Relic


def img_to_relic(INPUT_IMAGE, APP_CONFIG, INDEX):
    WHITELIST_CNF = APP_CONFIG['Whitelist']
    BOUNDING_BOXES_CNF = APP_CONFIG['Bounding Boxes']
    TESSERACT_CNF = APP_CONFIG['Tesseract']

    raw_sub_stat_numbers = ocr_functions.img_to_string(
        input_img=INPUT_IMAGE,
        bounding_box=BOUNDING_BOXES_CNF['sub_stat_numbers'],
        tesseract_config=TESSERACT_CNF['relic_sub_stat_num'])

    raw_sub_stat_names = ocr_functions.img_to_string(
        input_img=INPUT_IMAGE,
        bounding_box=BOUNDING_BOXES_CNF['sub_stat_names'],
        tesseract_config=TESSERACT_CNF['relic_sub_stat_name']
    )
    raw_main_stat_name = ocr_functions.img_to_string(
        input_img=INPUT_IMAGE,
        bounding_box=BOUNDING_BOXES_CNF['relic_main_stat_name'],
        tesseract_config=TESSERACT_CNF['relic_main_stat_name_1'],
        tesseract_config_2=TESSERACT_CNF['relic_main_stat_name_2'],
        double_check=True
    )
    raw_set_name = ocr_functions.img_to_string(
        input_img=INPUT_IMAGE,
        bounding_box=BOUNDING_BOXES_CNF['relic_set'],
        tesseract_config=TESSERACT_CNF['relic_set_name'])

    raw_slot_name = ocr_functions.img_to_string(
        input_img=INPUT_IMAGE,
        bounding_box=BOUNDING_BOXES_CNF['relic_slot'],
        tesseract_config=TESSERACT_CNF['relic_slot_name'])

    raw_level = ocr_functions.img_to_string(
        input_img=INPUT_IMAGE,
        bounding_box=BOUNDING_BOXES_CNF['relic_level'],
        tesseract_config=TESSERACT_CNF['relic_level'])

    try:
        slot_name = whitelist_check.filter_slot_names(raw_slot_name, WHITELIST_CNF['slots'])
        filtered_sub_stat_names = whitelist_check.filter_sub_stat_names(raw_sub_stat_names,
                                                                        WHITELIST_CNF['sub_stat_names'])
        main_stat_name = whitelist_check.check_main_stat_name(raw_main_stat_name,
                                                              WHITELIST_CNF['relic_main_stat_names'],
                                                              WHITELIST_CNF['possible_percent'],
                                                              slot_name
                                                              )
        set_name = whitelist_check.check_set_name(raw_set_name, WHITELIST_CNF['relic_sets'])

        sub_stat_numbers = clean_extracted_information.clean_sub_stat_numbers(raw_sub_stat_numbers)

        level = clean_extracted_information.clean_level(raw_level)

        sub_stats_complete = clean_extracted_information.sub_stats_flat_or_percent(filtered_sub_stat_names,
                                                                                   sub_stat_numbers,
                                                                                   WHITELIST_CNF['possible_percent'])

        sub_stat_object_list = []
        for i in range(len(sub_stats_complete["names"])):
            sub_stat_object = {"name": to_snake_case(sub_stats_complete["names"][i]), "value": sub_stats_complete["values"][i]}
            sub_stat_object_list.append(sub_stat_object)

        current_datetime = datetime.datetime.now()
        current_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

        relic = Relic(
            scan_datetime=current_datetime,
            main_stat_name=to_snake_case(main_stat_name),
            sub_stats=sub_stat_object_list,
            level=level,
            slot=Relic.Slot[to_snake_case(slot_name)],
            state=Relic.State.none,
            inventory_position=INDEX,
            set_name=to_snake_case(set_name)
        )

        return relic
    except Exception as e:
        logging.error(e)
        raise e


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
        relic_dicts = [relic.to_dict() for relic in relics_list]
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

        path = f'{directory}{formatted_datetime}_relics.json'

        os.makedirs(directory, exist_ok=True)

        with open(path, "w") as f:
            json.dump(relic_dicts, f, indent=4)

        msg_status.set(f'Saved {len(relics_list)} relics to\n "{path}"')
    except Exception as e:
        msg_status.set("Failed to write relics to file.")
        print(f"Error: {format(e)}")
