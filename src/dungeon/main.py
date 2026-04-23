"""Entry point for Dungeon Delver."""

from dungeon.game import Game


def main():
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
