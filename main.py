## Sam's Dumb Game Bot for Discord
## ettingersam@gmail.com
## February 2021

import os
from dotenv import load_dotenv
load_dotenv()

from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from games import config, twolying, chameleon

# Lazy shorthand for sending markdown text
def formatsend(update: Update, message: str) -> None:
  update.message.reply_text(message, parse_mode="HTML")

# Clear any existing game-specific rules that are defined
def clearRules() -> None:
  for rule in config.currRules:
    config.dispatcher.remove_error_handler(rule)
  
# Define what to do when a user types "/setgame [game]"
def setgame_command(update: Update, context: CallbackContext) -> None:
  try:
    arg = ' '.join(context.args).lower()
    haveNewGame = setgame(arg)
    if haveNewGame:
      # Add handlers for game commands
      for rule in config.currRules:
        config.dispatcher.add_handler(rule)
      # Run initialization for game
      config.loadedGames[config.currGame]['init']()
      formatsend(update, f"Active game has been set to <b>{config.currGame}</b>.")
    else:
      formatsend(update, f"No game was found with that title. {config.available_games()}")
  except:
    formatsend(update, f"There was an error. {config.available_games()}")
    return

def setgame(payload: str) -> bool:
  gameFound = False
  for game in config.loadedGames.keys():
    if game.lower().startswith(payload) or payload.startswith(game.lower()):
      gameFound = True
      config.currGame = game
      # Remove existing handlers for the previous game
      clearRules()
      # Set up commands for new game
      config.currRules = config.loadedGames[game]['commands']
  return gameFound

# Define what to do when a user types "/help"
def help_command(update: Update, context: CallbackContext) -> None:
  formatsend(update, config.game_details())

# Test echo
def echo(update: Update, context: CallbackContext) -> None:
  formatsend(update, update.message.text)

def main():
  # Initialize Telegram bot updater and dispatcher
  config.updater = Updater(os.getenv("TELEGRAM_TOKEN"))
  config.dispatcher = config.updater.dispatcher
  config.bot = Bot(token = os.getenv("TELEGRAM_TOKEN"))

  # Add handlers for base (non-game) commands
  config.dispatcher.add_handler(CommandHandler("setgame", setgame_command))
  config.dispatcher.add_handler(CommandHandler("help", help_command))

  # Start the bot
  config.updater.start_polling()
  print("Bot has logged on.")

  # Run until interrupted
  config.updater.idle()

if __name__ == '__main__':
  main()
  
"""
# Get each game that's available, plus the config file
from games import config, chameleon, twolying

  # 5. Look up the $commands defined in the current game
  elif message.content.startswith('$') and message.content.lower() in config.currRules.keys():
    if (not config.channelFocused) or message.channel == config.channelFocus:
      await config.currRules[message.content.lower()](message)

  # 6. (Optional) Look up rules for being DMed by players
  elif 'DM' in config.currRules.keys() and isinstance(message.channel, discord.channel.DMChannel):
    await config.currRules['DM'](message)
"""
