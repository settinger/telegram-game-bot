## Two of These People Are Lying
## A game by Tom Scott and the Technical Difficulties
## Adapted for Telegram by Sam Ettinger ettingersam@gmail.com

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import random
import unicodedata

from games import config

# Set up new entry for games config file
gameDict = {}
gameDict['intro'] = '''
Each game consists of multiple rounds. In each game, there is a dedicated guesser; everyone else is a player. Before starting a round, every player submits the title of a Wikipedia article by DMing it to the games bot. When the round begins, the bot announces one of the Wikipedia articles at random. It is then up to each player to convince the guesser that they were the one who read and submitted that Wikipedia article. Of course, only one player knows the actual contents of the Wikipedia article; the other players have to bluff!

The guesser must choose which player they think is telling the truth. If the guesser guesses correctly, both the guesser and the picked player get a point. If the guesser guesses incorrectly, the person they guessed still gets a point.

After each round, one of the players (the one whose article was randomly picked) must submit a new Wikipedia article by DMing the games bot again.

Available in-game commands:
<code>/newgame</code> &mdash; Starts a fresh game, discarding any stored players' submissions.
<code>/newround</code> &mdash; Begins a round by picking a submission at random.
'''

# Lazy shorthand for sending markdown text
def formatsend(update: Update, message: str) -> None:
  update.message.reply_text(message, parse_mode="HTML")

# Set up game logic, initialization function, game commands
def init() -> None:
  config.players = {}
  config.playingGame = False
  
def normalized(string: str) -> str:
  decomp = unicodedata.normalize('NFD', string)
  return ''.join([letter for letter in decomp if ord(letter)<0x280]).upper()

def newgame_command(update: Update, context: CallbackContext) -> None:
  config.playingGame = True
  config.players = {}
  formatsend(update, 'Starting a new game! All entries have been cleared. DM the bot to submit your Wikipedia article title.')

def newround_command(update: Update, context: CallbackContext) -> None:
  if not config.playingGame:
    return
  if len(config.players.keys()) > 0:
    # Pick one of the players' entries at random
    randoplayer = random.sample(list(config.players.keys()), 1)[0]
    randotopic = config.players[randoplayer]
    # Remove the rando player from the dictionary of submissions
    config.players.pop(randoplayer, None)
    # Reveal topic to the channel
    formatsend(update, f"The topic is: <code>{randotopic}</code>")

def DM_command(update: Update, context: CallbackContext) -> None:
  if not config.playingGame:
    return
  # Check if the message author *needs* a new topic
  if update.message.from_user in config.players.keys():
    formatsend(update, f"You already submitted the topic {config.players[update.message.from_user]}.")
  # Normalize the string, make it all-caps and add it to the list of topics
  else:
    config.players[update.message.from_user] = normalized(update.message.text)
    formatsend(update, f"Your topic <code>{config.players[update.message.from_user]}</code> has been recorded.")

# Set up Command Handlers
gameDict['init'] = init
gameDict['commands'] = [
  CommandHandler("newgame", newgame_command),
  CommandHandler("newround", newround_command),
  MessageHandler(Filters.text & ~Filters.command, DM_command)
  ]

# Add this game to the config file
config.loadedGames['Two of These People Are Lying'] = gameDict
