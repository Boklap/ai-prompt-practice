#!/usr/bin/env python3
"""
terminal_snake_minimal.py
Minimalist Terminal Snake Game
"""

import curses, random, time, os, json

WIDTH, HEIGHT, FPS, SPEED_BOOST, MAX_FOOD = 64, 18, 12, 1.2, 3
SCORE_FILE = os.path.expanduser("~/score/score.json")

# Symbols
WALL_TL, WALL_TR, WALL_BL, WALL_BR = "╭","╮","╰","╯"
WALL_V, WALL_H = "│","─"
SNAKE_HEAD, SNAKE_BODY, APPLE = "█","▓","Ó"

# Colors
COLOR_HEAD, COLOR_BODY, COLOR_APPLE = 2,3,1
COLOR_MENU_SELECTED, COLOR_MENU_NORMAL = 4,7

def load_highscore():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE,"r") as f:
            return json.load(f).get("highscore",0)
    return 0

def save_highscore(score):
    os.makedirs(os.path.dirname(SCORE_FILE),exist_ok=True)
    with open(SCORE_FILE,"w") as f:
        json.dump({"highscore":score},f)

def draw_centered(stdscr, lines):
    h,w = stdscr.getmaxyx()
    for i,line in enumerate(lines):
        x = w//2 - len(line)//2
        y = h//2 - len(lines)//2 + i
        stdscr.addstr(y,x,line)

def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(0)
    stdscr.timeout(-1)
    current_selection = 0
    menu = ["Play","Exit"]
    menu_art = ["   █████   Ó  ","  █     █    ","   █   █     ","    █ █      ","     █       "]
    while True:
        stdscr.clear()
        draw_centered(stdscr, ["Terminal Snake"]+[""]+menu_art+[""])
        h,w = stdscr.getmaxyx()
        for idx,item in enumerate(menu):
            x = w//2 - len(item)//2
            y = h//2 + 5 + idx
            if idx==current_selection:
                stdscr.attron(curses.color_pair(COLOR_MENU_SELECTED))
                stdscr.addstr(y,x,item)
                stdscr.attroff(curses.color_pair(COLOR_MENU_SELECTED))
            else:
                stdscr.attron(curses.color_pair(COLOR_MENU_NORMAL))
                stdscr.addstr(y,x,item)
                stdscr.attroff(curses.color_pair(COLOR_MENU_NORMAL))
        key = stdscr.getch()
        if key in [curses.KEY_UP, ord('w')]: current_selection=(current_selection-1)%len(menu)
        elif key in [curses.KEY_DOWN, ord('s')]: current_selection=(current_selection+1)%len(menu)
        elif key in [curses.KEY_ENTER, ord('\n')]: return menu[current_selection]
        stdscr.refresh()

def draw_game(stdscr,snake,apples,score,highscore):
    stdscr.clear()
    stdscr.addstr(0,0,f"Score: {score}  Highscore: {highscore}")
    for y in range(HEIGHT+2):
        for x in range(WIDTH+2):
            char=""
            if y==0 and x==0: char=WALL_TL
            elif y==0 and x==WIDTH+1: char=WALL_TR
            elif y==HEIGHT+1 and x==0: char=WALL_BL
            elif y==HEIGHT+1 and x==WIDTH+1: char=WALL_BR
            elif y==0 or y==HEIGHT+1: char=WALL_H
            elif x==0 or x==WIDTH+1: char=WALL_V
            if char: stdscr.addstr(y,x,char)
    stdscr.attron(curses.color_pair(COLOR_APPLE))
    for ax,ay in apples: stdscr.addstr(ay+1,ax+1,APPLE)
    stdscr.attroff(curses.color_pair(COLOR_APPLE))
    for i,(sx,sy) in enumerate(snake):
        if i==0: stdscr.attron(curses.color_pair(COLOR_HEAD)); stdscr.addstr(sy+1,sx+1,SNAKE_HEAD); stdscr.attroff(curses.color_pair(COLOR_HEAD))
        else: stdscr.attron(curses.color_pair(COLOR_BODY)); stdscr.addstr(sy+1,sx+1,SNAKE_BODY); stdscr.attroff(curses.color_pair(COLOR_BODY))
    stdscr.refresh()

def spawn_apple(snake,apples):
    empty=[(x,y) for x in range(WIDTH) for y in range(HEIGHT) if (x,y) not in snake and (x,y) not in apples]
    if empty and len(apples)<MAX_FOOD: apples.append(random.choice(empty))

def message_center(stdscr,message,score,highscore):
    stdscr.nodelay(0)
    h,w = stdscr.getmaxyx()
    for i in range(len(message)+1):
        draw_centered(stdscr,[message[:i]])
        stdscr.refresh()
        time.sleep(0.1)
    draw_centered(stdscr,[message,f"Score: {score} Highscore: {highscore}","Press Enter to return"])
    save_highscore(highscore)
    while True:
        key=stdscr.getch()
        if key in [ord('\n'), curses.KEY_ENTER]: return

def game_loop(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(1000//FPS)
    highscore = load_highscore()
    snake=[(WIDTH//2,HEIGHT//2)]
    direction=(0,-1)
    apples=[]
    score=0
    spawn_apple(snake,apples)
    last_time=time.time()
    while True:
        key=stdscr.getch()
        if key in [ord('w')] and direction!=(0,1): direction=(0,-1)
        elif key in [ord('s')] and direction!=(0,-1): direction=(0,1)
        elif key in [ord('a')] and direction!=(1,0): direction=(-1,0)
        elif key in [ord('d')] and direction!=(-1,0): direction=(1,0)
        speed=SPEED_BOOST if key==ord(' ') else 1.0
        now=time.time()
        if now-last_time<1/FPS/speed: continue
        last_time=now
        hx,hy=snake[0]
        new_head=(hx+direction[0],hy+direction[1])
        if new_head in snake or new_head[0]<0 or new_head[0]>=WIDTH or new_head[1]<0 or new_head[1]>=HEIGHT:
            message_center(stdscr,"You Lose",score,highscore); return
        snake.insert(0,new_head)
        if new_head in apples:
            apples.remove(new_head); score+=10; spawn_apple(snake,apples); highscore=max(highscore,score)
        else: snake.pop()
        if len(snake)==WIDTH*HEIGHT: message_center(stdscr,"You Win",score,highscore); return
        draw_game(stdscr,snake,apples,score,highscore)

def init_colors():
    curses.start_color()
    curses.init_pair(COLOR_APPLE,curses.COLOR_RED,0)
    curses.init_pair(COLOR_HEAD,curses.COLOR_GREEN,0)
    curses.init_pair(COLOR_BODY,curses.COLOR_CYAN,0)
    curses.init_pair(COLOR_MENU_SELECTED,curses.COLOR_YELLOW,0)
    curses.init_pair(COLOR_MENU_NORMAL,curses.COLOR_WHITE,0)

def main(stdscr):
    init_colors()
    while True:
        choice = main_menu(stdscr)
        if choice=="Play": game_loop(stdscr)
        else: break

if __name__=="__main__":
    curses.wrapper(main)
