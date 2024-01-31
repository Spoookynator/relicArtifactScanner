import app
from relic_scanner.controls import start_scan_loop_thread


def testerer():
    print('test')


def main():
    app.fist_time_startup()
    App = app.App()

    App.scanner_frame.main_interaction_container.start_scan_button.configure(command=lambda: start_scan_loop_thread(App))

    App.mainloop()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        input()
