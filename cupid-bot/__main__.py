"""Cupid bot entry point."""
import logging

from . import bot, config


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    config.load()
    bot.CupidBot()
