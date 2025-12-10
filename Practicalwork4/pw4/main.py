#!/usr/bin/env python3
import curses

from domains import UI, System


def main():
    school_system = System()
    ui = UI(school_system)
    curses.wrapper(ui.run)


if __name__ == "__main__":
    main()