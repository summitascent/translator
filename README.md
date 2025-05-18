# SummitAscent Translator
This is Brian and Ryan's submission for the May 2025 Supercell AI Hackathon.

## Usage Instructions
These instructions apply to Windows 11 users (Linux and Mac should have similar steps).

Make sure you have Python 3.13 installed as this project was developed using Python 3.13.
Clone this GitHub repository and in the command line, open this repository's directory and run:

For Windows 11
```
py -3.13 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

For Linux and Mac
```
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Afterwards run:
```
python ./translator.py
```
or 
```
./translator.py --verbose
```
to access the command line GUI. Press '=' every time you want to send the request for a translation (this can be changed in ```controls.py```). You can change the voice to one supported by ChatGPT as well in ```controls.py```.

## Submission Description
### Describe the problem it solves
Our project is a universal dialogue translator which aims to make games more accessible with regards to language barrier. For example, some games will only provide Japanese voices. In this case, for an English user, our project will translate the dialogue into English.

### What real-world impact does it have
There are many games, especially smaller games with lower budget, that only have voice overs in one language. Allowing users to translate the dialogue on-the-spot to their own mother tongue will make the gaming experience more enticing to many. 

### What technologies did you use to make it
This project was written completely in Python. For LLMs, we only used the ChatGPT API.

### Future plans regarding the project
During this Hackathon, we've thought of many possibilities for the future of this project which include but are not limited to
1. Integrating custom voices reflecting the different characters in the conversation (ideally the output voice would be as close as possible to the original)
    - The ChatGPT API used for this project currently offers 11 preset voices and no option for custom voices but there are definitely other options that we haven't explored yet
2. Making the output audio natural and automatic
    - Currently a button needs to be pressed for the translation of the previous dialogue section
    - Thought of trying to use voice detection and timings based off of that to automatically output audio during the hackathon but ended up using the manual method due to time constraints (we find this to be an interesting and difficult problem to explore in the future)
    - Some languages (like Japanese) require a situational understanding in order to more accurately translate. Otherwise, the nuances will be lost in translation. Ideally, the translator would remember relevent recent dialogue content to keep the nuances during word selection when translating new sentences. 
3. Inspired by Challenge 1 (Turning Public Information into Game-Smart Tools), improve the situational understanding and personality of the translations by using web scraping
    - There are many public Wiki pages online for games (for example [Steins;Gate Wiki](https://steins-gate.fandom.com/wiki/Steins;Gate_Wiki)) with information on the characters. These pages can be scraped for data and used to help more accurately create personas for the characters in (1).
4. Provide an option to completely replace the original audio with the translation
    - Ideally, the translation would replace the original audio completely (this is a non-trivial problem because the original audio contains background music/sounds as well as the voices of characters so we cannot simply mute the original audio or else we would be missing the background music/sounds in the translation)
5. Improve GUI
    - Add language choices (Japanese->English, English->Japanese, French->English etc.)
    - Make the GUI an actual standalone .exe program instead of running it through the command line
6. Make the response time of the program faster
    - Currently bottlenecked by ChatGPT API response time
        - Sometimes it is faster than other times (and this is often unpredictable)
        - We found that when the response time was faster, our user experience was much better
7. Include functionality for text translation as well
    - To make this a universal functionality, we would need to use computer vision
    - For things like visual novels (which usually have side by side both text and speech), we can combine the text extracted with computer vision as well as the text extracted from speech to make a more accurate final translation

