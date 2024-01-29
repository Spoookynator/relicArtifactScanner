import numpy as np

import box_editor
import screenshot
import dxcam
import vgamepad as vg
import time
import assemble_relic

import keyboard
from ocr_functions import get_menu


def scan_loop(App):

    camera = dxcam.create()

    msg_status = App.scanner_frame.main_interaction_container.stats_container.current_status.status_text
    msg_relic_count = App.scanner_frame.main_interaction_container.stats_container.scanned_relics_label.status_text
    msg_success_rate = App.scanner_frame.main_interaction_container.stats_container.scanned_relics_success_rate.status_text
    msg_time_elapsed = App.scanner_frame.main_interaction_container.stats_container.scanned_relics_time_elapsed.status_text

    current_menu = get_menu(screenshot.inventory_menu(camera, App.user_config))
    if current_menu != "Relics":
        msg_status.set('Error: Please navigate to the relic Screen')
        return

    gamepad = init_gamepad()

    if not gamepad:
        msg_status.set('Error: Gamepad couldnt be initalized')

    msg_status.set('Please focus Starrail')
    time.sleep(3)
    for i in range(5):
        msg_status.set(f'Starting in {5-i}')
        time.sleep(1)

    # Set the threshold for consecutive identical screenshots
    consecutive_threshold = App.user_config["ADVANCED"]["consecutive_threshold"]
    SCAN_LIMIT = App.user_config["GENERAL"]["scan_limit"]
    index = 1
    consecutive_count = 1  # Counter for consecutive identical screenshots
    relics_without_error = 0
    current_screenshot = screenshot.capture_relic(camera, App.user_config)

    relics_list = []

    starting_relic, errors_found = assemble_relic.convert_img_to_relic(current_screenshot,App.user_config)
    relics_list.append(starting_relic)

    if not errors_found:
        relics_without_error += 1


    # Display current relic
    msg_relic_count.set(f'{index}')
    msg_success_rate.set(
        f'{round((relics_without_error / index), 4) * 100}%')

    start_time = time.perf_counter()

    while consecutive_count < consecutive_threshold and index < SCAN_LIMIT:
        if keyboard.is_pressed("F1"):
            print("Exiting scan")
            break

        index += 1

        goto_next_relic(gamepad)

        new_screenshot = screenshot.capture_relic(camera, App.user_config)

        if new_screenshot is None:
            new_screenshot = current_screenshot

        if np.array_equal(new_screenshot, current_screenshot):
            consecutive_count += 1
        else:
            consecutive_count = 1

        loop_relic, errors_found = assemble_relic.convert_img_to_relic(new_screenshot, App.user_config)
        relics_list.append(loop_relic)

        if not errors_found:
            relics_without_error += 1

        current_time = time.perf_counter()

        # Display current relic
        msg_status.set(f'{index}')
        msg_status.set(f'{round((relics_without_error / index), 4) * 100}%')
        msg_time_elapsed.set(f'{current_time}s')

        # Update the current screenshot for the next iteration
        current_screenshot = new_screenshot

    del gamepad
    if consecutive_count == consecutive_threshold:
        msg_status('Scan Sucessful')
        for i in range(consecutive_threshold - 1):
            relics_list.pop()
            relics_without_error -= 1
            index -= 1

    else:
        msg_status(f"Limit of {SCAN_LIMIT} reached. Stopping scan.")

    end_time = time.perf_counter()

    msg_time_elapsed(f'{end_time}s')
    directory = App.user_config["GENERAL"]["relic_output_dir"]

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
