from api.app import FastApiApp

def create_app():
    app = FastApiApp()
    return app.application