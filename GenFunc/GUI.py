from tkinter import *
from tkinter import font as tkFont

from numpy.core.numeric import cross
from main import *
import threading, time
import numpy as np
from function import easom, styblinski, crossInTray
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def changeFunc(type: int):
    global FUN_CHOICE, STOP_EXEC, IS_RUNNING
    if(IS_RUNNING):
        STOP_EXEC = True
    FUN_CHOICE = type
    updateUI()

def changeOpt(type: int):
    global OPT_TYPE, STOP_EXEC, IS_RUNNING
    if(IS_RUNNING):
        STOP_EXEC = True
    OPT_TYPE = type
    updateUI()

def updateUI():
    global ALL_BUTTONS, FUN_CHOICE, OPT_TYPE
    for button in ALL_BUTTONS:
        button.configure(background="#C4C4C4")
    ALL_BUTTONS[FUN_CHOICE-1].configure(background="#636e72")
    ALL_BUTTONS[OPT_TYPE+2].configure(background="#636e72")

def runGA():
    global FUN_CHOICE, OPT_TYPE, IS_RUNNING, STOP_EXEC, THREAD_OBJ, GRAPH
    updateUI()
    if(IS_RUNNING):
        STOP_EXEC = True
    POPULATION_SIZE = 100
    MAX_GENERATIONS = 100
    MUTATION_RATE = 0.05
    limits = []
    type = ""
    if(OPT_TYPE==1):
        type = "max"
    else:
        type = "min"
    if(FUN_CHOICE==1):
        limits = [-100, 100]
    elif(FUN_CHOICE==2):
        limits = [-5, 5]
    else:
        limits = [-10, 10]
    plot_X = np.linspace(limits[0], limits[1], 50)
    plot_Y = np.linspace(limits[0], limits[1], 50)
    X_mesh, Y_mesh = np.meshgrid(plot_X, plot_Y)
    Z_mesh = None
    if(FUN_CHOICE==1):
        Z_mesh = easom([X_mesh, Y_mesh])
    if(FUN_CHOICE==2):
        Z_mesh = styblinski([X_mesh, Y_mesh])
    else:
        Z_mesh = crossInTray([X_mesh, Y_mesh])
    GRAPH.cla()
    GRAPH.plot_wireframe(X_mesh, Y_mesh, Z_mesh, label="Function Graph")
    IS_RUNNING = True
    THREAD_OBJ = threading.Thread(target=runGenetic, args=(POPULATION_SIZE, MAX_GENERATIONS, MUTATION_RATE, limits, FUN_CHOICE, type,))
    THREAD_OBJ.setDaemon(True)
    THREAD_OBJ.start()
    # runGenetic(POPULATION_SIZE, MAX_GENERATIONS, MUTATION_RATE, limits, FUN_CHOICE, type)

def runGenetic(POPULATION_SIZE: int, MAX_GENERATIONS: int, MUTATION_RATE: float, limits: list, choice: int, type: str):
    global STOP_EXEC, IS_RUNNING, TEXT_AREA, THREAD_OBJ, GRAPH
    population = generateInitialPopulation(POPULATION_SIZE, limits)
    bestIndividual = population[0]
    bestPlot = [[], [], []]
    # print("INSIDE THREAD")
    for i in range(0, MAX_GENERATIONS):
        if(STOP_EXEC):
            STOP_EXEC = False
            IS_RUNNING = False
            break
        msg = ""
        # print(bestIndividual.fitness)
        for j, individual in enumerate(population):
            fitness(individual, choice)
            msg += f"Candidate {j+1}\t\t: {individual.fitness}\n"
        TEXT_AREA[0].delete(1.0, END)
        TEXT_AREA[0].insert(1.0, msg)
        for individual in population:
            if(type=="min"):
                if(individual.fitness < bestIndividual.fitness):
                    bestIndividual = deepcopy(individual)
            else:
                if(individual.fitness > bestIndividual.fitness):
                    bestIndividual = deepcopy(individual)
        population = generateNewPopulation(population, MUTATION_RATE, type)
        bestPlot[0].append(bestIndividual.chromosome[0])
        bestPlot[1].append(bestIndividual.chromosome[1])
        bestPlot[2].append(bestIndividual.fitness)
        GRAPH.plot(bestPlot[0], bestPlot[1], bestPlot[2], "ro--", markersize=2, label="Optimization Graph")
        if(i==0):
            GRAPH.legend()
        time.sleep(0.1)
    IS_RUNNING = False



if __name__ == '__main__':
    window = Tk()
    helv12 = tkFont.Font(family='Helvetica', size=12, weight='bold')
    # helv1 = tkFont.Font(family='Helvetica', size=8, weight='bold')
    window.geometry("1000x600")
    window.configure(bg = "#ffffff")
    canvas = Canvas(
        window,
        bg = "#ffffff",
        height = 600,
        width = 1000,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    background = canvas.create_image(
        500.0, 394.0)

    b0 = Button(
        text = "EASOM FUNCTION",
        font=helv12,
        bg="#C4C4C4",
        borderwidth = 0,
        highlightthickness = 0,
        command = lambda: changeFunc(1),
        relief = "flat")

    b0.place(
        x = 51, y = 10,
        width = 284,
        height = 45)

    b1 = Button(
        text = "MAXIMIZE FUNCTION",
        font=helv12,
        bg="#C4C4C4",
        borderwidth = 0,
        highlightthickness = 0,
        command = lambda: changeOpt(1),
        relief = "flat")

    b1.place(
        x = 193, y = 75,
        width = 285,
        height = 45)

    b2 = Button(
        text = "MINIMIZE FUNCTION",
        font=helv12,
        bg="#C4C4C4",
        borderwidth = 0,
        highlightthickness = 0,
        command = lambda: changeOpt(2),
        relief = "flat")

    b2.place(
        x = 522, y = 75,
        width = 284,
        height = 45)

    b3 = Button(
        text = "STYBLINSKI-TANG FUNCTION",
        font=helv12,
        bg="#C4C4C4",
        borderwidth = 0,
        highlightthickness = 0,
        command = lambda: changeFunc(2),
        relief = "flat")

    b3.place(
        x = 357, y = 10,
        width = 284,
        height = 45)

    b4 = Button(
        text = "CROSS-IN-TRAY FUNCTION",
        font=helv12,
        bg="#C4C4C4",
        borderwidth = 0,
        highlightthickness = 0,
        command = lambda: changeFunc(3),
        relief = "flat")

    b4.place(
        x = 664, y = 10,
        width = 284,
        height = 45)

    b5 = Button(
        text="RUN GA",
        font=helv12,
        bg="#C4C4C4",
        borderwidth = 0,
        highlightthickness = 0,
        command = runGA,
        relief = "flat")

    b5.place(
        x = 450, y = 135,
        width = 100,
        height = 40)
    
    entry0 = Text(
    bd = 0,
    font=helv12,
    bg = "#eeeeee",
    # state="disabled",
    highlightthickness = 0)

    entry0.place(
        x = 0, y = 188,
        width = 500,
        height = 410)

    graph_fig = Figure(figsize=(5, 5), dpi=100)
    GRAPH = graph_fig.add_subplot(111, projection="3d")
    
    graph_area = FigureCanvasTkAgg(graph_fig)
    graph_area.get_tk_widget().place(x=500, y=188,
    width=500,
    height=410)

    ALL_BUTTONS = [b0, b3, b4, b1, b2, b5]
    TEXT_AREA = [entry0]
    FUN_CHOICE = 1
    OPT_TYPE = 1
    STOP_EXEC = False
    IS_RUNNING = False
    THREAD_OBJ = None
    window.resizable(False, False)
    window.mainloop()
