from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Students")
root.geometry('840x512')
root.resizable(False, False)

canv = Canvas(root, width=400, height=400, bg="white", cursor="pencil", )
canv.create_line(0, 200, 400, 200, width=1)
canv.create_line(200, 0, 200, 400, width=1)

figures = []

class figure:
    x = []
    y = []

    sides = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sides = len(self.x)


def Load():
    lineList = []
    filename = entryf.get()

    with open(filename, 'r', encoding='utf-8') as f:
        ind = 1
        for i in f.readlines():
            a = i.split(';')
            x = []
            y = []
            for j in a:
                x.append(int(j.split(',')[0]))
                y.append(int(j.split(',')[1]))

            f = figure(x, y)
            figures.append(f)
            lineList.append(str(ind) + ' многоугольник : ' + str(f.sides) + ' сторон' + '\n')
            ind += 1

    PrintFig(lineList)
    DrawFig(figures, 'black', True)


def PrintFig(list):
    studListd = StringVar(value=list)
    listboxd = Listbox(listvariable=studListd)
    listboxd.place(anchor=NW, x=15, y=65, width=385, height=360)

    scrollbar = ttk.Scrollbar(orient="vertical", command=listboxd.yview)
    scrollbar.place(anchor=NW, y=65, x=385, width=20, height=360)
    listboxd["yscrollcommand"] = scrollbar.set


def DrawFig(ls, color, clear):
    if clear: canv.delete('all')
    canv.create_line(0, 200, 400, 200, width=1)
    canv.create_line(200, 0, 200, 400, width=1)
    for i in ls:
        for j in range(i.sides):
            canv.create_line(i.x[j] * 10 + 200, -i.y[j] * 10 + 200, i.x[j-1] * 10 + 200, -i.y[j-1] * 10 + 200, width=2, fill=color)


def Color():
    color = entryax.get()
    inp = []
    f = figures[int(entryv.get())-1]
    for j in range(f.sides):
        inp.append(tuple([f.x[j] * 10 + 200, -f.y[j] * 10 + 200]))

    for j in range(f.sides):
        canv.create_polygon(inp, width=2, fill=color)

    DrawFig(figures, 'black', False)


def check_intersection(l1, l2):
    dx1 = l1[2] - l1[0]
    dx2 = l2[2] - l2[0]
    dy1 = l1[3] - l1[1]
    dy2 = l2[3] - l2[1]

    k1 = dy1 / dx1
    k2 = dy2 / dx2

    b1 = l1[1] - k1 * l1[0]
    b2 = l2[1] - k2 * l2[0]

    if k1 == k2: return [False, 0, 0]

    x = (b2 - b1) / (k1 - k2)
    y = k1 * x + b1

    if (min(l1[0], l1[2]) <= x <= max(l1[0], l1[2])) and (min(l2[0], l2[2]) <= x <= max(l2[0], l2[2])): return [True, x, y]

    return [False, 0, 0]


def find_intersections():
    for i in range(len(figures)-1):
        for j in range(i+1, len(figures)):
            if(min(figures[i].x) > max(figures[j].x)): break
            if(max(figures[i].x) < min(figures[j].x)): break
            if(min(figures[i].y) > max(figures[j].y)): break
            if(max(figures[i].y) < min(figures[j].y)): break

            for a in range(figures[i].sides):
                for b in range(figures[j].sides):
                    res = check_intersection([figures[i].x[a-1], figures[i].y[a-1], figures[i].x[a], figures[i].y[a]],
                                             [figures[j].x[b-1], figures[j].y[b-1], figures[j].x[b], figures[j].y[b]])
                    if res[0]:
                        x = res[1]
                        y = res[2]
                        canv.create_line(x*10+199, -y*10+199, x*10+201, -y*10+201, width=10, fill='red')


def Move():
    n = int(entryn.get())
    a = entrym.get()
    x = int(a.split(',')[0])
    y = int(a.split(',')[1])

    for i in range(figures[n-1].sides):
        figures[n-1].x[i] += x
        figures[n-1].y[i] += y

    DrawFig(figures, 'black', True)


# tkinter
btn = ttk.Button(text="Загрузить из файла", command=Load)
btn.place(anchor=NW, x=250, y=20, height=25, width=150)

btn1 = ttk.Button(text="Раскраска", command=Color)
btn1.place(anchor=NW, x=15, y=432, height=25, width=100)

labelax = ttk.Label(text="Цвет:")
labelax.place(anchor=NW, x=15, y=470, height=25)
entryax = ttk.Entry()
entryax.place(anchor=NW, x=165, y=470, height=25, width=40)

labelv = ttk.Label(text="Номер многоугольника:")
labelv.place(anchor=NW, x=220, y=470, height=25)
entryv = ttk.Entry()
entryv.place(anchor=NW, x=370, y=470, height=25, width=40)

btn2 = ttk.Button(text="Пересечения", command=find_intersections)
btn2.place(anchor=NW, x=300, y=432, height=25, width=100)

btn3 = ttk.Button(text="Перемещение", command=Move)
btn3.place(anchor=NW, x=720, y=432, height=25, width=100)

labelFile = ttk.Label(text="Имя файла:")
labelFile.place(anchor=NW, x=15, y=20, height=25)
entryf = ttk.Entry()
entryf.place(anchor=NW, x=90, y=20, height=25, width=150)

labelax = ttk.Label(text="Смещение (вектор 0,0):")
labelax.place(anchor=NW, x=429, y=470, height=25)
entrym = ttk.Entry()
entrym.place(anchor=NW, x=559, y=470, height=25, width=40)

labelv = ttk.Label(text="Номер многоугольника:")
labelv.place(anchor=NW, x=624, y=470, height=25)
entryn = ttk.Entry()
entryn.place(anchor=NW, x=779, y=470, height=25, width=40)

studListd = StringVar(value=[])
listboxd = Listbox(listvariable=studListd)
listboxd.place(anchor=NW, x=15, y=65, width=385, height=360)

scrollbar = ttk.Scrollbar(orient="vertical", command=listboxd.yview)
scrollbar.place(anchor=NW, y=65, x=385, width=20, height=360)
listboxd["yscrollcommand"] = scrollbar.set

canv.place(x=420, y=15)
root.mainloop()