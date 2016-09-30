import config
from app import app, db


if __name__ == '__main__':
    config.reset_system(db=db)
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
