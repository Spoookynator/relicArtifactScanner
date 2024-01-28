import app


def main():
    app.fist_time_startup()
    App = app.App()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        input()
