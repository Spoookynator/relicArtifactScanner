# TODO: Pan-Cosmic Commercial Enterprise isnt getting recognized
def check_set_name(ocr_raw_text, whitelist_set_names):

    is_found = False
    found_name = ""
    for line in whitelist_set_names:
        if line in ocr_raw_text or line.lower() in ocr_raw_text.lower():
            is_found = True
            found_name = line
    if is_found:
        return found_name, True
    else:
        return None, "Error: Set name not found"


# chatgpt, splits the raw input by new line, and then compares the lower version to the control array lower version
# returns list of substat names
# TODO: Wasterlander set sub stats aren`t recognized for some reason, pan-cosmic as well
def filter_sub_stat_names(ocr_raw_text, whitelist_sub_stat_names):

    sub_stats = ocr_raw_text.split("\n")
    sub_stats = list(filter(None, sub_stats))

    whitelist_array_lower = [word.lower() for word in whitelist_sub_stat_names]

    filtered_words = [word for word in sub_stats if word.lower() in whitelist_array_lower]

    # Check if there are any allowed words
    if not filtered_words:
        return [None], "Filtered words not found"

    return filtered_words, True


# this basically cleans out any trash chars as well, since the stat is getting copied from the whitelist
def check_main_stat_name(ocr_raw_text, whitelist_main_stats, whitelist_possible_percent_in_name, slot_name):

    is_found = False
    found_name = ""
    for line in whitelist_main_stats:
        if line in ocr_raw_text or line.lower() in ocr_raw_text.lower():
            is_found = True
            found_name = line

    if is_found:

        if found_name in whitelist_possible_percent_in_name and not slot_name.lower() in ["head", "hands"]:
            found_name += "%"
        return found_name, True
    else:
        return None, "Error: Main stat name not found"


def filter_slot_names(ocr_raw_text, whitelist_slots):
    is_found = False
    found_name = ""
    for line in whitelist_slots:
        if line.lower() in ocr_raw_text.lower():
            is_found = True
            found_name = line

    if is_found:
        return found_name, True
    else:
        return None, "Error: Slot name not found"
