# Evently
<https://t.me/event_handler_bot>

Evently is going to help you manage your events!!!


* Omer Daniel
* Gal Hadad

you can create your event, ask your friends items to bring with them and let the bot ask your friends for ascendancy. 

## Screenshots

![SCREESHOT DECSRIPTION](screenshots/evently.png)

## How to Run This Bot
### Prerequisites
* Python 3.7 or 3.8
* pipenv
* {ADD MORE DEPENDENCIES HERE - FOR EXAMPLE MONGODB OR ANYTHING ELSE}

### Setup
* Clone this repo from github
* Install dependencies: `pipenv install`
* Get a BOT ID from the [botfather](https://telegram.me/BotFather).
* Create a `secrets.py` file:

        BOT_TOKEN = "your-bot-token-here"

### Run
To run the bot use:

    pipenv run python bot.py

### Running tests
First make sure to install all dev dependencies:

    pipenv install --dev

To run all test  use:

    pipenv run pytest

(Or just `pytest` if running in a pipenv shell.)

## Credits and References
* [Telegram Docs](https://core.telegram.org/bots)
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* {ADD MORE REFERENCES TO LIBRARIES, APIS AND CODE SNIPPETS HERE}
