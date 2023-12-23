import os

import numpy as np

import box_editor
import screenshot
import dxcam
import vgamepad as vg
import time
import assemble_relic

import keyboard
from ocr_functions import get_menu


def menu(BOUNDING_BOXES, WHITELIST, CONFIG):
    while True:
        print("S = Scan, E = Exit, O = Show Boxes")
        user_input = input("Input Command\n")
        # press 'q' to exit
        match user_input:
            case "E":
                print("Exiting...")
                time.sleep(1)
                break
            case "S":
                print("Select Relic to start from")
                time.sleep(1)
                print("DO NOT USE MOUSE OR KEYBOARD WHILE SCAN IS IN PROGRESS")
                time.sleep(1)
                print("If run as administrator, you can cancel with F1")
                time.sleep(1)
                print("This could take a while, please be patient...")
                time.sleep(2)

                scan_loop(BOUNDING_BOXES, WHITELIST, CONFIG)
            case "O":
                print("Focus Starrail")
                time.sleep(1)
                print("Generating images...")
                box_editor.create_curent_box_imgs(BOUNDING_BOXES, CONFIG)
                print(f"Images generated in '{CONFIG['GENERAL']['box_editor_dir']}'")


def scan_loop(BOUNDING_BOXES, WHITELIST, CONFIG):
    camera = dxcam.create()
    current_menu = get_menu(screenshot.inventory_menu(camera, BOUNDING_BOXES["MENU"], CONFIG))

    if current_menu != "Relics":
        print("Error: Please navigate to the relic Screen")
        return
    os.system('cls')
    gamepad = init_gamepad()

    # Set the threshold for consecutive identical screenshots
    consecutive_threshold = CONFIG["GENERAL"]["consecutive_threshold"]
    SCAN_LIMIT = CONFIG["GENERAL"]["scan_limit"]
    index = 1
    consecutive_count = 1  # Counter for consecutive identical screenshots
    relics_without_error = 0
    current_screenshot = screenshot.capture_relic(camera, BOUNDING_BOXES["RELIC"], CONFIG)

    relics_list = []

    starting_relic, errors_found = assemble_relic.convert_img_to_relic(INPUT_IMAGE=current_screenshot, WHITELIST=WHITELIST, BOUNDING_BOXES=BOUNDING_BOXES)
    relics_list.append(starting_relic)

    if not errors_found:
        relics_without_error += 1

    print("====Relic 1====")
    print(f"{relics_without_error}/{index} successfully scanned ({round((relics_without_error/index),4) * 100}%)")
    print("===============")
    start_time = time.perf_counter()

    while consecutive_count < consecutive_threshold and index < SCAN_LIMIT:
        if keyboard.is_pressed("F1"):
            print("Exiting scan")
            break

        index += 1

        goto_next_relic(gamepad)

        new_screenshot = screenshot.capture_relic(camera, BOUNDING_BOXES["RELIC"], CONFIG)

        if new_screenshot is None:
            new_screenshot = current_screenshot

        if np.array_equal(new_screenshot, current_screenshot):
            consecutive_count += 1
        else:
            consecutive_count = 1

        loop_relic, errors_found = assemble_relic.convert_img_to_relic(INPUT_IMAGE=new_screenshot, WHITELIST=WHITELIST, BOUNDING_BOXES=BOUNDING_BOXES)
        relics_list.append(loop_relic)

        if not errors_found:
            relics_without_error += 1

        current_time = time.perf_counter()
        os.system('cls')

        relic_header_string = f"====Relic {index}===="
        print(relic_header_string)
        print(f"Time elapsed: {round(current_time - start_time, 2)}s")
        print(f"{relics_without_error}/{index} successfully scanned ({round((relics_without_error/index),4) * 100}%)")
        relic_footer_string = len(relic_header_string) * "="
        print(relic_footer_string)

        # Update the current screenshot for the next iteration
        current_screenshot = new_screenshot

    del gamepad
    if consecutive_count == consecutive_threshold:
        print(f"The same screenshot was fed to the array {consecutive_threshold} times in a row. "
              f"Deleting last {consecutive_threshold - 1} entries")
        for i in range(consecutive_threshold - 1):
            relics_list.pop()
            relics_without_error -= 1
            index -= 1

    else:
        print(f"Limit of {SCAN_LIMIT} reached. Stopping scan.")

    end_time = time.perf_counter()

    print(f"Scanned {len(relics_list)} relics in {round((end_time-start_time), 2)}s. Success rate: {relics_without_error}/{index} ({round((relics_without_error/index),4) * 100}%)")
    directory = CONFIG["GENERAL"]["json_output_dir"]

    assemble_relic.write_relics_to_file(relics_list, directory)


def init_gamepad():
    gamepad = vg.VX360Gamepad()

    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(2)
    return gamepad


def goto_next_relic(gamepad):
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
    gamepad.update()
    time.sleep(0.05)
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
    gamepad.update()
    time.sleep(0.05)


def check_if_error(input_list):
    errors = 0
    for entry in input_list:
        if entry != True:
            errors += 1
    return errors