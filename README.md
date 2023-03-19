PyCalls
=======

PyCalls is a Python application for managing incoming calls. It uses a modem to receive caller ID (CID) data via serial and provides features such as call logging, contact management, and Telegram notifications. It works with [PyCalls-API](https://github.com/danielecostarella/pycalls-api).

Installation
------------

1.  Clone the repository: `git clone https://github.com/danielecostarella/pycalls.git`
2.  Install dependencies: `pip install -r requirements.txt`
3.  Rename `config-template.py` to `config.py`
4.  Configure the application by editing the `config.py` file.
4.  Run the application: `python main.py`

Features
--------

*   Receive and log CID data from a modem via serial
*   Manage contacts via the PyCalls API
*   Send Telegram notifications for incoming calls
*   Configure application settings via `config.py` file

Usage
-----

PyCalls requires a modem to receive CID data via serial. Once the modem is connected and configured, the application can be started with the `python main.py` command.

The application will automatically connect to the [PyCalls-API](https://github.com/danielecostarella/pycalls-api) and start logging incoming calls. To view call logs or manage contacts, use the PyCalls API endpoints.

License
-------

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Acknowledgments
---------------

*   [Python FastAPI](https://fastapi.tiangolo.com/)
*   [PyCalls API](https://github.com/user/pycalls-api)
*   [Telethon](https://github.com/LonamiWebs/Telethon)
