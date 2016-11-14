# -*- coding: UTF-8 -*-

from botanick.commands.parser import Parser
from botanick.const import SPLASH


def main():
    """
    Main entrypoint
    """
    print(SPLASH)
    try:
        parser = Parser()
        command = parser.getCommand()
        args = parser.getArgs()
        if not args:
            command()
        else:
            command(args)
    except KeyboardInterrupt:
        print('Execution aborted by user ! Bye !')


if __name__ == "__main__":
    main()
