from Model import Model
from Login import Login
from App import App


def main():
    model = Model()
    model.create_connection()
    model.create_database()
    model.create_tables()

    login = Login(model)
    login.run()

    if model.authenticated:
        app = App(model)
        app.run()
    else:
        model.db.close()
        login.destroy()

if __name__ == "__main__":
    main()