import curses
import time
import os
import argparse
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

def print_resize_message(my_screen):
    my_screen.addstr(0, 0, "Please, resize your term to 125 , 40 pixels")
    my_screen.refresh()


def build_dump(args):
    offset = 0
    chunks = []
    with open(args.file, 'rb') as f:
            while True:
                chunk = f.read(16)
                if len(chunk) == 0:
                    break
                text = str(chunk)
                text = ''.join([i if ord(i) < 128 and ord(i) > 32 \
                                    else "." for i in text])
                output = "{:#08x}".format(offset) + ": "
                output += " ".join("{:02X}".format(c) \
                                        for c in chunk[:8])
                output += " | "
                output += " ".join("{:02X}".format(c) \
                                        for c in chunk[8:])
                if len(chunk) % 16 != 0:
                    output += "   "*(16 - len(chunk)) + text
                else:
                    output += " " + text
                if args.output:
                    print(output)
                chunks.append(output)
                offset += 16
    return chunks

def save_dump(my_screen):



def show_menu(my_screen, chunks):
    my_screen.erase()
    if os.name == 'posix':
        h, w = my_screen.getmaxyx()
        while h != 40 or w != 125:
            print_resize_message(my_screen)
            h, w = my_screen.getmaxyx()
    my_screen.erase()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    my_screen.attron(curses.color_pair(1))
    act_chunks = chunks[:39]
    i = 0
    for chunk in act_chunks:
        my_screen.addstr(i, 1, chunk)
        i+=1
    my_screen.attroff(curses.color_pair(1))
    h, w = my_screen.getmaxyx()
    while True:
        key = my_screen.getch()
        cursor_pos_x, cursor_pos_y = my_screen.getyx()
        if key == KEY_UP:
            cursor_pos_x-=1
        elif key == KEY_DOWN:
            cursor_pos_x+=1
        elif key == KEY_RIGHT:
            cursor_pos_y+=1
        elif key == KEY_LEFT:
            cursor_pos_y-=1
        elif key == ord("q"):
            break
        elif key == ord("s"):
            save_dump(my_screen)
        if cursor_pos_x >= h or cursor_pos_x < 0:
            cursor_pos_x = 0
        if cursor_pos_y >= w or cursor_pos_y < 0:
            cursor_pos_y = 0
        character = my_screen.instr(cursor_pos_x,cursor_pos_y, 1)
        character = character.decode('utf-8')[0]
        my_screen.addstr(h-1, 0, f"You selected :{character}")
        my_screen.move(cursor_pos_x,cursor_pos_y)
        my_screen.refresh()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Specify a filepath")
    parser.add_argument('-o', '--output', help="Print output to a terminal"
                            , action="store_true")
    args = parser.parse_args()

    if args.file:
        chunks = build_dump(args)
    else:
        print(parser.usage)
    curses.wrapper(show_menu, chunks)

if __name__ == '__main__':
    main()
