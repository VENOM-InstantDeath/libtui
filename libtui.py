import curses
import re
from curses.textpad import rectangle

def listoint(l,sym):
    if not isinstance(l,list): raise ValueError
    if len(l) == 2:
        s = l[0]+sym+l[1]
        return eval(s)

def label(id, center, fill, color, content):
    return {"id": id,
            "type": "label",
            "content": content,
            "center": center,
            "fill": fill,
            "color": color}

def vlayout(id, border, scrollok, size, elements):
    return {"id": id,
            "type": "vlayout",
            "border": border,
            "scroll": scrollok,
            "size": (size[0], size[1]),
            "elements": elements}

def modpos(y, x):
    return {"type": "modpos",
            "y": y,
            "x": x}

def br():
    return {"type": "br"}

def sep():
    return {"type": "sep"}


def fill(stdscr, y, max_x, color):
    for i in range(max_x):
        stdscr.addch(y, i, " ", curses.color_pair(color))

def wstr(stdscr, mpos, st, obj):
    """{"id": "x1",
        "type": "label",
        "content": "Main",
        "center": True}"""
    x = mpos[2][1]*2
    mx = x-5
    cx = mpos[2][1]
    color = 0
    if obj["color"]: color = obj["color"]
    if obj["fill"]: fill(stdscr, mpos[0], x, color)
    if obj["center"]:
        lines = (len(obj["content"])//mx)+1
        if lines+mpos[0] > (mpos[2][0]*2)-1: raise RuntimeError(f"El objeto '{obj['id']}' es más grande que el resto de la pantalla")
        for i in range(lines):
            stdscr.addstr(mpos[0], cx-(len(obj["content"][mx*i:mx*(i+1)])//2), obj["content"][mx*i:mx*(i+1)], curses.color_pair(color))
            mpos[0] += 1
    else:
        lines = (len(obj["content"])//x)+1
        if lines+mpos[0] > (mpos[2][0]*2)-1: raise RuntimeError(f"El objeto '{obj['id']}' es más grande que el resto de la pantalla.")
        for i in range(lines):
            stdscr.addstr(mpos[0], mpos[1], obj["content"][x*i:x*(i+1)], curses.color_pair(color))
            mpos[0] += 1

def vlay(stdscr, pos, der, obj):
    y, x = obj["size"]
    a = [0,0]
    if not re.match('^(max|[0-9]+)([+-](max|[0-9]+))?$', y): raise ValueError
    if not re.match('^(max|[0-9]+)([+-](max|[0-9]+))?$', x): raise ValueError
    a[0], a[1] = (re.findall('[+-]', y), re.findall('[+-]', x))
    ry, rx = (re.split('[+-]', y), re.split('[+-]', x))
    for i in range(len(ry)):
        if ry[i] == "max":
            ry[i] = str((pos[2][0]*2)-pos[0])
    for i in range(len(rx)):
        if rx[i] == "max":
            rx[i] = str((pos[2][1]*2)-pos[1])
    #curses.endwin();print(ry[0]);print(a[0][0]);print(ry[1]);exit()
    y, x = (listoint(ry, a[0][0]), listoint(rx, a[1][0]))
    if obj["border"]:
        rectangle(stdscr, pos[0], pos[1], pos[0]+y+1, pos[1]+x+1)
        pos[0]+=1
        pos[1]+=1
    if der:
        win = stdscr.derwin(y, x, pos[0], pos[1])
    else:
        win = curses.newwin(y, x, pos[0], pos[1])
    wpos = [0,0,[0,0]]
    wpos[2][0], wpos[2][1] = win.getmaxyx()
    wpos[2][0] //= 2
    wpos[2][1] //= 2
    pos[0] += y+1
    pos[1] = 0
    for i in obj["elements"]:
        if i["type"] == "label":
            wstr(win, wpos, "v", i)
        if i["type"] == "vlayout":
            vlay(win, wpos, 1, i)
        if i["type"] == "modpos":
            wpos[0] += i["y"]
            wpos[1] += i["x"]
        if i["type"] == "br":
            wpos[0] += 1
        if i["type"] == "sep":
            for i in range(wpos[2][1]*2):
                win.addch(wpos[0], i, curses.ACS_HLINE)
            wpos[0] += 1
    stdscr.refresh()
    win.refresh()

def hlay(stdscr, pos, obj):
    pass

def tui(stdscr, pos, std):
    st_layout = "v"
    for i in std:
        if i["type"] == "label":
            wstr(stdscr, pos, st_layout, i)
        if i["type"] == "vlayout":
            vlay(stdscr, pos, 0, i)
        if i["type"] == "modpos":
            pos[0] += i["y"]
            pos[1] += i["x"]
        if i["type"] == "br":
            pos[0] += 1
        if i["type"] == "sep":
            for i in range(pos[2][1]*2):
                stdscr.addch(pos[0], i, curses.ACS_HLINE)
            pos[0] += 1

def main(stdscr):
    curses.use_default_colors()
    curses.curs_set(0)
    curses.init_pair(9, 231, 9) # rojo
    curses.init_pair(20, 231, 20) # azul
    y, x = stdscr.getmaxyx()
    stdpos = [0,0,(y//2,x//2)]
    std = []
    std.append(label('x1', True, True, 20, "Fandom de Backyardigans"))
    std.append(br())
    std.append(label('x2', True, False, 0, "Intro de Backyardigans"))
    std.append(br())
    std.append(label('x3', False, False, 0, "Hola soy Pablo, soy Tayrone, soy Uniqua, soy Tasha, y yo Austin y somos aaaaaamigos tuyos backyardigans."))
    std.append(br())
    std.append(sep())
    std.append(br())
    std.append(label('x4', False, False, 0, "Dónenme en PayPal, muchachos."))
    std.append(br())
    std.append(sep())
    std.append(label('x5', True, False, 0, "Nuevos elementos: layouts"))
    std.append(br())
    n = ("11-0","50-0")
    std.append(vlayout('v1', False, 1, (n[0], n[1]), [label('title', True, True, 9, "Lipsum"), label('debug', False, False, 0, "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")]))
    std.append(label('e', False, False, 0, ".-."))
    tui(stdscr, stdpos, std)
    stdscr.getch()

if __name__=='__main__':
    curses.wrapper(main)
