import tkinter as tk
from tkinter import messagebox
from controller.config import Config
from agents.location import Location

class Gui(tk.Tk):
    def __init__(self, environment, agent_colours):
        super().__init__()
        self.__environment = environment
        self.__agent_colours = agent_colours
        self.__closed = False
        self.__cells = {}

        self.title(Config.simulation_name)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


        self.legend_panel = tk.Frame(self, bg="white", pady=5)
        self.legend_panel.grid(row=0, column=0, sticky="ew")


        self.grid_frame = tk.Frame(self, bg="gray")
        self.grid_frame.grid(row=1, column=0, padx=5, pady=5)


        self._create_grid()


        self.render()

    def _create_grid(self):
        """Create all grid cells once"""
        for y in range(self.__environment.get_height()):
            for x in range(self.__environment.get_width()):
                cell = tk.Canvas(
                    self.grid_frame,
                    width=Config.cell_size,
                    height=Config.cell_size,
                    bg="white",
                    highlightthickness=1,
                    highlightbackground="gray"
                )
                cell.grid(row=y, column=x, padx=0, pady=0)
                self.__cells[(x, y)] = cell

    def render(self):
        """Update the display"""
        if self.__closed:
            return


        self.update_legend()


        for y in range(self.__environment.get_height()):
            for x in range(self.__environment.get_width()):
                agent = self.__environment.get_agent(Location(x, y))

                if agent:
                    colour = self.__agent_colours.get(agent.__class__, "white")
                else:
                    colour = "white"

                cell = self.__cells[(x, y)]
                cell.configure(bg=colour)

        self.update_idletasks()

    def update_legend(self):
        """Update the legend with agent counts"""
        for widget in self.legend_panel.winfo_children():
            widget.destroy()


        counts = {}
        for y in range(self.__environment.get_height()):
            for x in range(self.__environment.get_width()):
                agent = self.__environment.get_agent(Location(x, y))
                if agent:
                    cls = agent.__class__
                    counts[cls] = counts.get(cls, 0) + 1


        if counts:
            for cls, count in sorted(counts.items(), key=lambda x: x[0].__name__):
                colour_box = tk.Label(
                    self.legend_panel,
                    bg=self.__agent_colours[cls],
                    width=3,
                    relief="solid",
                    borderwidth=1
                )
                colour_box.pack(side=tk.LEFT, padx=(10, 2))

                label = tk.Label(
                    self.legend_panel,
                    text=f"{cls.__name__}: {count}",
                    font=("Arial", 10)
                )
                label.pack(side=tk.LEFT, padx=(0, 15))

    def on_closing(self):
        """Handle window close event"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.__closed = True
            self.destroy()

    def is_closed(self):
        """Check if window is closed"""
        return self.__closed
