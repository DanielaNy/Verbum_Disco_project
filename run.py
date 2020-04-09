from VDP import app
from VDP.config_file import configuration


if __name__ == "__main__":
    if configuration == 'prod':
        app.run(host="0.0.0.0", port="8080")
    else:
        app.run()
