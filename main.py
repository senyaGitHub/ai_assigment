from simulation.simulation_engine import Simulator
import tkinter as tk
from gui.gui import Gui

if __name__ == "__main__":
    simulator = Simulator()
    simulator.run()

root = tk.Tk()
app = gui(root)
root.mainloop()
