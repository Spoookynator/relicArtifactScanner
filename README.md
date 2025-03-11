# Relic Artifact Scanner
This project enables scanning in-game relics from the game Honkai: Star Rail and saving them to a .json file. This will include all visible stats (so no decimals).
For the first version, there is a binary avaliable, but for the newest one you have to build it yourself.

## How to use
- The program (either binary or IDE) needs administrator permissions, to be able to use the gamepad virtualizer and to overwrite Star Rails "protections" to be able to scan.
- Before starting, look at the config file and adjust the maximum amount of relics scanned for a test attempt and then for future tests
- Simply launch the program and select the scanner page (the others do not work right now)
- Now navigate to the relic page in-game, if you are not on the relic page, you will not be able to start the scan.
- Now start the scan and focus Star Rail
- The scan is not very fast, but it will keep going until it reaches the maximum relic count, or encounters the same relic multiple times

## Possible Future Features
- edit boxes for screenshots, currently they are just hard-coded and wont support many screens
- display saved relics in inventory and sort/filter them
- settings inside the app instead of separate settings file 
