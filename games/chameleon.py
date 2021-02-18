## Chameleon
## A game by Big Potato Games
## Adapted for Telegram by Sam Ettinger ettingersam@gmail.com

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import random
from games import config

# The game data is in a separate file that I will *not* be putting online because it's the main content of the game that Big Potato is selling, so it's not right for me to hand it out for free
from games.chameleon_data import cards

# Set up new entry for games config file
gameDict = {}
gameDict['intro'] = '''
In each round, a list of sixteen related things is shown to all the players. One of these sixteen things is selected at random and DMed to all but one of the players. The remaining player merely knows that they are the Chameleon for this round! The Chameleon's goals are to (1) not get caught, (2) figure out what the subject is.

Players take turns saying a single word that relates to the thing they were given. The Chameleon has to bluff. After everyone has said their single word, the players can grill each other to get more details or explanations, while trying not to give away the subject of the round.

At the end of the discussion, players vote on who they think is the Chameleon. If the players guess incorrectly, the Chameleon wins! If the players guess correctly, the Chameleon gets to guess what the subject of the round was. If the Chameleon guesses correctly, they win! Otherwise, the other players all win.

Available in-game commands:
<code>/newgame</code> &mdash; Starts a fresh game.
<code>/newround</code> &mdash; Begins a round with all the players that have joined.
'''

# Lazy shorthand for sending markdown text
def formatsend(update: Update, message: str) -> None:
  update.message.reply_text(message, parse_mode="HTML")

# Set up game logic, initialization function, game commands
def init() -> None:
  config.players = []
  config.cards = cards
  config.playingGame = False

def formatted(card) -> str:
  message = ''
  message += '<b>Category: ' + card[0].upper() + '</b>\n'
  for entry in card[1]:
    message += entry + '\n'
  return message

def newgame_command(update: Update, context: CallbackContext) -> None:
  config.players = []
  config.playingGame = True
  formatsend(update, 'Starting a new game! DM <code>/join</code> to the bot to be added to the game.')

def DM_command(update: Update, context: CallbackContext) -> None:
  if not config.playingGame:
    return
  if 'join' in update.message.text.lower():
    if update.message.chat_id not in config.players:
      config.players += [update.message.chat_id]
      formatsend(update, 'You have joined the game!')
    else:
      formatsend(update, 'You have already joined the game.')

def newround_command(update: Update, context: CallbackContext) -> None:
  if not config.playingGame:
    return
  chosenCard = random.sample(config.cards, 1)[0]
  # message the channel with the chosen card
  formatsend(update, formatted(chosenCard))

  # Pick the secret and the chameleon
  secret = random.sample(chosenCard[1], 1)[0]
  random.shuffle(config.players)
  chameleon = config.players[0]

  # DM each player
  config.bot.send_message(chat_id=chameleon, text="You are the Chameleon!", parse_mode='HTML')
  for player in config.players[1:]:
    config.bot.send_message(chat_id=player, text=f"The secret topic is: <b>{secret}</b>", parse_mode='HTML')

# Set up command handlers
gameDict['init'] = init
gameDict['commands'] = [
  CommandHandler("newgame", newgame_command),
  CommandHandler("newround", newround_command),
  MessageHandler(Filters.text & ~Filters.command, DM_command)
  ]

# Add entry to games config file
config.loadedGames['Chameleon'] = gameDict
