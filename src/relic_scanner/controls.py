import logging
import math

import numpy as np

import src.relic_scanner.screenshot as screenshot
import vgamepad as vg
import time
import src.relic_scanner.assemble_relic as assemble_relic
import keyboard
from src.relic_scanner.ocr_functions import get_menu
from threading import Thread


def start_scan_loop_thread(App):
    t = Thread(target=lambda: scan_loop(App), daemon=True)
    t.start()


def scan_loop(App):
    App.f_scanner.disable_scan_button()

    current_menu = get_menu(screenshot.capure_screenshot(App.camera, App.UserConfig, 'menu_area'))
    if current_menu != "Relics":
        App.f_scanner.set_status_msg('Error: Please navigate to the relic Screen')
        App.f_scanner.enable_scan_button()

        return
    App.f_scanner.set_status_msg('Initializing Gamepad...')
    gamepad = init_gamepad()
    if not gamepad:
        App.f_scanner.set_status_msg('Error: Gamepad couldnt be initalized')
        App.f_scanner.enable_scan_button()

    App.f_scanner.set_status_msg('Done!')
    time.sleep(0.1)

    App.f_scanner.set_status_msg('Please focus Starrail')
    time.sleep(1)

    # Set the threshold for consecutive identical screenshots
    consecutive_threshold = App.UserConfig["GENERAL"].as_int("consecutive_threshold")
    SCAN_LIMIT = App.UserConfig["GENERAL"].as_int("scan_limit")
    index = 1
    consecutive_count = 1  # Counter for consecutive identical screenshots
    relics_without_error = 0

    App.f_scanner.set_status_msg('Taking Screenshot...')

    current_screenshot = screenshot.capure_screenshot(App.camera, App.UserConfig, 'relic_area')

    relics_list = []

    App.f_scanner.set_status_msg('Extract Data...')
    try:
        starting_relic = assemble_relic.img_to_relic(current_screenshot, App.UserConfig, index)
        relics_list.append(starting_relic)
        relics_without_error += 1
    except Exception as e:
        logging.error(e)

    # Display current relic
    App.f_scanner.set_relic_amount(f'{index}')
    App.f_scanner.set_relic_successes(
        f'{round((relics_without_error / index), 4) * 100}%')

    start_time = time.time()

    times = []

    while consecutive_count < consecutive_threshold and index < SCAN_LIMIT:
        if keyboard.is_pressed("F1"):
            print("Exiting scan")
            break
        relic_time = time.time()
        index += 1
        App.f_scanner.set_status_msg('Switching Relic...')
        goto_next_relic(gamepad)

        App.f_scanner.set_status_msg('Taking Screenshot...')
        new_screenshot = screenshot.capure_screenshot(App.camera, App.UserConfig, 'relic_area')

        if new_screenshot is None:
            new_screenshot = current_screenshot

        if np.array_equal(new_screenshot, current_screenshot):
            consecutive_count += 1
        else:
            consecutive_count = 1

        App.f_scanner.set_status_msg('Extract Data...')
        try:
            loop_relic = assemble_relic.img_to_relic(new_screenshot, App.UserConfig, index)
            relics_list.append(loop_relic)
            relics_without_error += 1
        except Exception as e:
            logging.error(e)

        current_time = time.time()

        times.append(current_time - relic_time)

        # Display current relic
        App.f_scanner.set_relic_amount(f'{index}')
        App.f_scanner.set_relic_successes(f'{round((relics_without_error / index), 4) * 100}%')

        timer_string = f'{math.floor((current_time - start_time) / 60)}:'

        if (round((current_time - start_time) % 60)) < 10:
            timer_string += '0'

        timer_string += f'{round((current_time - start_time) % 60)}'
        App.f_scanner.set_time_elapsed(timer_string)

        # Update the current screenshot for the next iteration
        current_screenshot = new_screenshot

    del gamepad

    App.f_scanner.set_relic_amount(f'{index}')

    if consecutive_count == consecutive_threshold:
        App.f_scanner.set_status_msg('Scan Sucessful')
        for i in range(consecutive_threshold - 1):
            relics_list.pop()
            relics_without_error -= 1
            index -= 1
        App.f_scanner.set_relic_amount(f'{len(relics_list)}')

    else:
        App.f_scanner.set_status_msg(f"Limit of {SCAN_LIMIT} reached. Stopping scan.")

    logging.debug(f'Average completion time: {sum(times) / len(times)}')

    end_time = time.perf_counter()

    App.f_scanner.set_time_elapsed(f'{round(end_time - start_time, 2)}s')
    directory = App.UserConfig["GENERAL"]["relic_output_dir"]

    assemble_relic.write_relics_to_file(relics_list, directory, App)
    App.f_scanner.enable_scan_button()


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
