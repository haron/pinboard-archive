# Archive your Pinboard links to PDF files

Currently it works on MacOS only and presumes you have Chrome browser installed.

Quick start:

1. Clone this repo.
2. Install the dependencies: `pip install -r requirements.txt`.
3. Get your API token [here](https://pinboard.in/settings/password) and save it to the file `.token`.
4. Run `./pinboard_archive.py` and then see PDF files in `archive/` directory.
5. Add something like this to your crontab:
    ```
    0 10,16 * * * /path/to/pinboard-archive/pinboard_archive.py
    ```
