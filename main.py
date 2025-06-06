import gui

if __name__ == "__main__":
    app = gui.Gui()
    loggedin = app.login()
    if not loggedin:
        app.run()