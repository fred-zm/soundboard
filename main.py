import gui

if __name__ == "__main__":
    app = gui.Gui()
    while not app.is_logged_in: 
        app.login()
    if app.is_logged_in:
        app.run()