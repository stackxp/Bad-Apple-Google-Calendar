# Bad-Apple-Google-Calendar

Play Bad Apple!! (or any other video file) in [Google Calendar](https://calendar.google.com/)

![Bad Apple in the Google Calendar](docs/badapple.png)

## Setup

1. Download this repo anywhere on your computer
2. Install additional pip packages by running `pip install -r requirements.txt`.
3. Log into [Google Calendar](https://calendar.google.com/), select *year* in the top-right corner or press [Y] on your keyboard.
4. right-click anywhere on the page and select *Save Page as...*
5. Navigate to the path, where you downloaded this repo in and save it as "index.html".
6. A folder called "index_files" will be created along with the file. You can delete all of its contents, except:
    - calendar_*[something]*.png
    - Every .css file
    - unnamed.png
    - unnamed_*[something]*.png
7. *Aquire* a copy of the Bad Apple!! MP4 from [The Internet Archive](https://archive.org/details/TouhouBadApple)
8. Insert the following code at the top of `index.html`:
```html
<script src="/badapple.js"></script>
```
9. Run `python3 main.py --video-path [path to bad apple]`.
10. Open http://localhost:8000/ in a web browser.
11. Open the developer console (method varies per browser) and switch to the console tab.
12. Ignore all the warnings and type `init()`. If you did everything right, all the days should light up blue.
13. Now type `run()`. A preview window should open and the days in the calendar should start changing to the video.

> [!TIP]
> Run `python3 main.py` without arguments to see all command-line options available.

## How it works

The main.py script start a Flask and a WebSocket server. The Flask server serves the `index.html` file, `badapple.js` and the `index_files` folder.
The WebSocket server waits for a connection from the hosted webpage and then sends all the frames of the video as strings of ones and zeroes.

`badapple.js` is responsible for the web browser side.
When running `init()`, it organizes all of the calendar days into a list and sets their background color to blue.
And when `run()` is executed, the script establishes a connection to the Python WebSocket-Server and updates every days' color to match the video's pixels.

## TODO
- Add audio playback to main.py
- Compress the data sent to the browser
- Make the days RGB (fancy)
