import logging
import re


def clean_sub_stat_numbers(sub_stat_numbers_string):
    numbers_string_list = sub_stat_numbers_string.split("\n")
    numbers_string_list.pop()

    numbers_string_list = list(filter(None, numbers_string_list))
    pattern = re.compile(r'^[0-9.%]+$')

    numbers_string_list = [s for s in numbers_string_list if pattern.match(s)]
    try:
        for i in range(len(numbers_string_list)):
                if "%" in numbers_string_list[i]:
                    numbers_string_list[i] = numbers_string_list[i].replace("%", "")
                    numbers_string_list[i] = float(numbers_string_list[i])
                    numbers_string_list[i] = round(numbers_string_list[i] / 100, 3)
                else:
                    numbers_string_list[i] = int(numbers_string_list[i])

        logging.debug(f'Cleaned string to: {numbers_string_list}')
        return numbers_string_list
    except Exception as e:
        raise e


def sub_stats_flat_or_percent(sub_stat_name_list, sub_stat_numbers_list, WHITELIST):
    if not len(sub_stat_name_list) == len(sub_stat_numbers_list):
        raise Exception("Lists arent the same")

    try:
        for i in range(len(sub_stat_name_list)):
            sub_stat_name_list[i] = stat_flat_or_percent(sub_stat_name_list[i], sub_stat_numbers_list[i], WHITELIST)
    except Exception as e:
        raise e

    sub_stats = {"names": sub_stat_name_list, "values": sub_stat_numbers_list}
    return sub_stats


def stat_flat_or_percent(stat_name, stat_value, WHITELIST):
    try:
        if stat_value < 1 and stat_name in WHITELIST:
            stat_name += "%"
        return stat_name
    except TypeError as e:
        raise e


def clean_level(raw_ocr_level):
    try:
        cleaned_level = raw_ocr_level.replace("+", "").rstrip()
        return int(cleaned_level)
    except Exception as e:
        raise e
