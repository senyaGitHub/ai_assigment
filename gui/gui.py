import tkinter as tk
from tkinter import messagebox, scrolledtext
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

        # Main container
        main_container = tk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel - Grid
        left_panel = tk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, padx=(0, 10))

        # Legend at top
        self.legend_panel = tk.Frame(left_panel, bg="white", pady=5)
        self.legend_panel.pack(fill=tk.X)

        # Grid
        self.grid_frame = tk.Frame(left_panel, bg="gray", relief=tk.SUNKEN, bd=2)
        self.grid_frame.pack()

        # Right panel - Status and Log
        right_panel = tk.Frame(main_container, width=350)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_panel.pack_propagate(False)

        # Status panel
        status_label = tk.Label(right_panel, text="Agent Status", font=("Arial", 12, "bold"))
        status_label.pack(pady=(0, 5))

        self.status_text = tk.Text(right_panel, height=12, width=45, font=("Courier", 9))
        self.status_text.pack(fill=tk.X, pady=(0, 10))

        # Action log
        log_label = tk.Label(right_panel, text="Action Log", font=("Arial", 12, "bold"))
        log_label.pack(pady=(0, 5))

        self.log_text = scrolledtext.ScrolledText(right_panel, height=15, width=45,
                                                    font=("Courier", 8), state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Create grid cells
        self._create_grid()

        # Initial render
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
        self.update_status()

        # Update grid colors based on agent health
        for y in range(self.__environment.get_height()):
            for x in range(self.__environment.get_width()):
                agent = self.__environment.get_agent(Location(x, y))

                if agent and agent.is_alive():
                    base_colour = self.__agent_colours.get(agent.__class__, "white")
                    # Darken color based on health
                    health_pct = agent.get_health_percentage()
                    colour = self._adjust_color_brightness(base_colour, health_pct)
                else:
                    colour = "white"

                cell = self.__cells[(x, y)]
                cell.configure(bg=colour)

        self.update_idletasks()

    def _adjust_color_brightness(self, color_name, health_percentage):
        """Adjust color brightness based on health"""
        # Map color names to RGB
        color_map = {
            "green": (0, 255, 0),
            "blue": (100, 150, 255),
            "red": (255, 50, 50),
            "orange": (255, 165, 0),
            "purple": (200, 100, 255)
        }

        if color_name not in color_map:
            return color_name

        r, g, b = color_map[color_name]
        factor = health_percentage / 100.0

        # Darken based on health
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)

        return f'#{r:02x}{g:02x}{b:02x}'

    def update_legend(self):
        """Update the legend with agent counts"""
        for widget in self.legend_panel.winfo_children():
            widget.destroy()

        counts = {}
        for y in range(self.__environment.get_height()):
            for x in range(self.__environment.get_width()):
                agent = self.__environment.get_agent(Location(x, y))
                if agent and agent.is_alive():
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
                    font=("Arial", 9)
                )
                label.pack(side=tk.LEFT, padx=(0, 15))

    def update_status(self):
        """Update agent status display"""
        self.status_text.delete(1.0, tk.END)

        from agents.dek import Dek
        from agents.thia import Thia
        from agents.monster import Monster

        # Find key agents
        for y in range(self.__environment.get_height()):
            for x in range(self.__environment.get_width()):
                agent = self.__environment.get_agent(Location(x, y))

                if agent and isinstance(agent, Dek):
                    status = f"=== DEK ===\n"
                    status += f"Health: {agent.health}/{agent.max_health}\n"
                    status += f"Stamina: {agent.stamina}/{agent.max_stamina}\n"
                    status += f"Honour: {agent.honour}\n"
                    status += f"Trophies: {agent.trophies}\n"
                    status += f"Position: ({agent.x}, {agent.y})\n\n"
                    self.status_text.insert(tk.END, status)

                elif agent and isinstance(agent, Thia):
                    status = f"=== THIA ===\n"
                    status += f"Health: {agent.health}/{agent.max_health}\n"
                    status += f"Status: Damaged\n"
                    status += f"Position: ({agent.x}, {agent.y})\n\n"
                    self.status_text.insert(tk.END, status)

        # Count monsters
        monster_count = sum(1 for y in range(self.__environment.get_height())
                           for x in range(self.__environment.get_width())
                           if (agent := self.__environment.get_agent(Location(x, y)))
                           and isinstance(agent, Monster) and agent.is_alive())

        self.status_text.insert(tk.END, f"=== THREATS ===\n")
        self.status_text.insert(tk.END, f"Monsters alive: {monster_count}\n")

    def log_action(self, agent_name, action, details):
        """Add action to log"""
        self.log_text.config(state=tk.NORMAL)
        log_entry = f"[{agent_name}] {action}: {details}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def on_closing(self):
        """Handle window close event"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.__closed = True
            self.destroy()

    def is_closed(self):
        """Check if window is closed"""
        return self.__closed
