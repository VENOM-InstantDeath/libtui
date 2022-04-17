import curses
from curses.textpad import rectangle

def label(id, center, fill, color, content):
    return {"id": id,
            "type": "label",
            "content": content,
            "center": center,
            "fill": fill,
            "color": color}

def br():
    return {"type": "br"}

def sep():
    return {"type": "sep"}


def fill(stdscr, y, max_x, color):
    for i in range(max_x):
        stdscr.addch(y, i, " ", curses.color_pair(color))

def wstr(stdscr, pos, obj):
    """{"id": "x1",
        "type": "label",
        "content": "Main",
        "center": True}"""
    x = pos[2][1]*2
    mx = x-5
    cx = pos[2][1]
    color = 0
    if obj["color"]: color = obj["color"]
    if obj["fill"]: fill(stdscr, pos[0], x, color)
    if obj["center"]:
        lines = (len(obj["content"])//mx)+1
        for i in range(lines):
            stdscr.addstr(pos[0], cx-(len(obj["content"][mx*i:mx*(i+1)])//2), obj["content"][mx*i:mx*(i+1)], curses.color_pair(color))
            pos[0] += 1
    else:
        lines = (len(obj["content"])//x)+1
        for i in range(lines):
            stdscr.addstr(pos[0], pos[1], obj["content"][x*i:x*(i+1)], curses.color_pair(color))
            pos[0] += 1

def vlay(stdscr, pos, obj):
    pass

def hlay(stdscr, pos, obj):
    pass

def main(stdscr):
    curses.use_default_colors()
    curses.curs_set(0)
    curses.init_pair(9, 231, 9) # rojo
    curses.init_pair(20, 231, 20) # azul
    y, x = stdscr.getmaxyx()
    pos = [0,0,(y//2,x//2)]
    std = []
    std.append(label('x1', True, True, 20, "Prueba de libtui"))
    std.append(br())
    std.append(label('x2', True, False, 0, "¿Qué es libtui?"))
    std.append(br())
    std.append(label('x3', False, False, 0, "Libtui es una librería para la programación de TUIs programada en Python que usa ncurses. Esta librería facilita el proceso de hacer programas con interfaces de texto brindando widgets y opciones para posicionar los elementos en la pantalla o modificarlos."))
    std.append(br())
    std.append(sep())
    std.append(br())
    std.append(label('x4', False, False, 0, "Dónenme en PayPal, muchachos."))
    for i in std:
        if i["type"] == "label":
            wstr(stdscr, pos, i)
        if i["type"] == "br":
            pos[0] += 1
        if i["type"] == "sep":
            for i in range(pos[2][1]*2):
                stdscr.addch(pos[0], i, curses.ACS_HLINE)
            pos[0] += 1
    stdscr.getch()

if __name__=='__main__':
    curses.wrapper(main)
