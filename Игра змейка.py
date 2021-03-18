from tkinter import Tk, Canvas
import random

# Размерность
WIDTH = 900
HEIGHT = 700
SEG_SIZE = 20 #размер змейки (толщина) и еды
GAME = True #статус игры

# Вспомогательные функции
def create_block():
    #Создание параметров для яблока
    global BLOCK
    posx = SEG_SIZE * random.randint(1, (WIDTH-SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT-SEG_SIZE) / SEG_SIZE)
    BLOCK = c.create_oval(posx, posy,
                          posx+SEG_SIZE, posy+SEG_SIZE,
                          fill="red")

def main():
    #Игровой процесс
    global GAME
    if GAME:
        s.move()
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords
        # Стоп-игра, если змейка вышла за пределы окна
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            GAME = False
        # Увеличене в размере
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            create_block()
        # Стоп-игра, если змейка ест сама себя
        else:
            for index in range(len(s.segments)-1):
                if head_coords == c.coords(s.segments[index].instance):
                    GAME = False
        root.after(100, main)
    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')

class Segment(object):
    #Сегмент змейки (квадратик)
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y,
                                           x+SEG_SIZE, y+SEG_SIZE,
                                           fill="blue")

class Snake(object):
    #Сама змейка
    def __init__(self, segments):
        self.segments = segments
        # возможные направления движения
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}
        #изначальное направление
        self.vector = self.mapping["Right"]

    def move(self):
        #функция движения
        for index in range(len(self.segments)-1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index+1].instance)
            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        c.coords(self.segments[-1].instance,
                 x1+self.vector[0]*SEG_SIZE, y1+self.vector[1]*SEG_SIZE,
                 x2+self.vector[0]*SEG_SIZE, y2+self.vector[1]*SEG_SIZE)

    def add_segment(self):
        #добавление сегмента змейке
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, Segment(x, y))

    def change_direction(self, event):
        #Создание "поворота" змейки
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def reset_snake(self):
        for segment in self.segments:
            c.delete(segment.instance)

def set_state(item, state):
    c.itemconfigure(item, state=state)

def clicked(event):
    global GAME
    s.reset_snake()
    GAME = True
    c.delete(BLOCK)
    c.itemconfigure(restart_text, state='hidden')
    c.itemconfigure(game_over_text, state='hidden')
    start_game()

def start_game():
    global s
    create_block()
    s = create_snake()
    c.bind("<KeyPress>", s.change_direction)
    main()

def create_snake():
    # создание сегментов змейки
    segments = [Segment(SEG_SIZE, SEG_SIZE),
                Segment(SEG_SIZE*2, SEG_SIZE),
                Segment(SEG_SIZE*3, SEG_SIZE)]
    return Snake(segments)

# Создание графического окна
root = Tk()
root.title("Змейка")

c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#000000")
c.grid()
c.focus_set()
game_over_text = c.create_text(WIDTH/2, HEIGHT/2, text="GAME OVER!",
                               font='Arial 20', fill='red',
                               state='hidden')
restart_text = c.create_text(WIDTH/2, HEIGHT-HEIGHT/3,
                             font='Arial 30',
                             fill='white',
                             text="Click here to restart",
                             state='hidden')
c.tag_bind(restart_text, "<Button-1>", clicked)
start_game()
root.mainloop()