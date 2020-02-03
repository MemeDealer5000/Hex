import argparse
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

my_screen = curses.initscr()

def build_dump(args):
    offset = 0
    chunks = []
    with open(args.file, 'rb') as f:
        with open(args.file + ".dump", "w") as out_file:
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

def show_menu(chunks):
    my_screen.erase()
    my_screen.addstr(1, 1, "========================================")
    my_screen.addstr(2, 1, "                Hex Editor")
    my_screen.addstr(3, 1, "========================================")
    my_screen.addstr(4, 1, "  1 - Show File in Currently Directory")
    my_screen.addstr(5, 1, "  0 - Exit")
    my_screen.addstr(6, 1, "========================================")
    my_screen.addstr(7, 1, "  Enter a selection: ")
    my_screen.refresh()
    wait_for_input(chunks)

def print_chunks(chunks, affordable_chunks):
    my_screen.erase()
    key = my_screen.getch()
    act_chunks = chunks[:39]
    i = 0
    for chunk in act_chunks:
        my_screen.addstr(i, 1, chunk)
        i+=1
    while True:
        cursor_pos_x, cursor_pos_y = my_screen.getyx()
        if key == KEY_UP:
            cursor_pos_x+=1
        elif key == KEY_DOWN:
            cursor_pos_x-=1
        elif key == KEY_RIGHT:
            cursor_pos_y+=1
        elif key == KEY_LEFT:
            cursor_pos_y-=1
        my_screen.move(cursor_pos_x,cursor_pos_y)
        my_screen.refresh()
        key = my_screen.getch()

def wait_for_input(chunks):
    key = 'X'
    chunks_len = len(chunks)
    affordable_chunks = chunks_len // 39
    while key != ord('0'):
        key = my_screen.getch(7, 22)
        if key == ord('1'):
            print_chunks(chunks, affordable_chunks)
            break
    my_screen.refresh()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Specify a filepath")
    parser.add_argument('-o', '--output', help="Print output to a termonal"
                            , action="store_true")
    args = parser.parse_args()

    if args.file:
        chunks = build_dump(args)
    else:
        print(parser.usage)
    curses.noecho()
    curses.cbreak()
    curses.resize_term(40,125)
    curses.curs_set(2)
    show_menu(chunks)
    curses.endwin()

if __name__ == '__main__':
    main()
