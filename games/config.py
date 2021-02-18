## Game Config File
## Begins by asserting no game is set up, and bot listens to every channel. This gets re-written when games get loaded in

channelFocused = False
channelFocus = None
currGame = 'none'
currRules = []
loadedGames = {'none': []}

# List all available games
def available_games():
  return f"Available games are: {', '.join([f'<b>{game}</b>' for game in loadedGames.keys() if game!='none'])}."

# List the currently loaded game
def game_details():
  if currGame == 'none':
    return "No game is active at the moment. Pick a game with <code>/setgame {gamename}.</code>\n" + available_games()
  else:
    return f"Active game is <b>{currGame}</b>." + "\n\n" + loadedGames[currGame]['intro'] + "\n\nOther available bot commands:\n<code>/setgame {gamename}</code> -- Changes the active game.\n<code>/help</code> -- shows this page."
