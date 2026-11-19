"""Interactive Matplotlib animation for the recursive solver."""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button, TextBox

from . import solve


def board_states(disks):
    """Return successive board snapshots, including the starting board."""
    moves = solve(disks)
    towers = [list(range(disks, 0, -1)), [], []]
    states = [[tuple(tower) for tower in towers]]
    for source, target in moves:
        towers[target].append(towers[source].pop())
        states.append([tuple(tower) for tower in towers])
    return states


class HanoiAnimation:
    def __init__(self, disks):
        self.fig, self.ax = plt.subplots(figsize=(9, 5))
        self.fig.subplots_adjust(bottom=.24)
        self.fig.canvas.manager.set_window_title("Tower of Hanoi")
        self.disks = TextBox(self.fig.add_axes([.16, .10, .12, .06]), "Disks ", initial=str(disks))
        self.speed = TextBox(self.fig.add_axes([.48, .10, .13, .06]), "Delay (ms) ", initial="500")
        self.start = Button(self.fig.add_axes([.73, .10, .16, .06]), "Start")
        self.start.on_clicked(self.run)
        self.status = self.fig.text(.5, .04, "", ha="center")
        self.animation = None
        self.states = board_states(disks)
        self.draw(0)

    def draw(self, frame):
        self.ax.clear()
        disks = len(self.states[0][0])
        self.ax.set_xlim(-.6, 2.6)
        self.ax.set_ylim(0, disks + 1)
        self.ax.set_xticks([0, 1, 2], ["A", "B", "C"])
        self.ax.set_yticks([])
        self.ax.set_title(f"Tower of Hanoi · Move {frame} of {len(self.states) - 1}")
        colors = plt.get_cmap("tab10")
        for peg, tower in enumerate(self.states[frame]):
            self.ax.add_patch(Rectangle((peg - .02, .16), .04, disks + .4, color="#645a54"))
            self.ax.add_patch(Rectangle((peg - .48, .08), .96, .08, color="#645a54"))
            for level, disk in enumerate(tower):
                width = .22 + .65 * disk / disks
                self.ax.add_patch(Rectangle(
                    (peg - width / 2, .2 + level), width, .78, color=colors(disk - 1)
                ))

    def run(self, _event):
        try:
            disks = int(self.disks.text)
            delay = int(self.speed.text)
            if not 1 <= disks <= 10 or not 50 <= delay <= 2000:
                raise ValueError
        except ValueError:
            self.status.set_text("Use 1–10 disks and a delay of 50–2,000 ms.")
            self.fig.canvas.draw_idle()
            return

        if self.animation is not None and self.animation.event_source is not None:
            self.animation.event_source.stop()
        self.status.set_text("")
        self.states = board_states(disks)
        self.draw(0)
        self.animation = FuncAnimation(
            self.fig, self.draw, init_func=lambda: self.draw(0),
            frames=range(1, len(self.states)), interval=delay,
            repeat=False, cache_frame_data=False,
        )
        self.fig.canvas.draw_idle()


def show(disks):
    window = HanoiAnimation(disks)
    plt.show(block=True)
    plt.close(window.fig)
