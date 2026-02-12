import tkinter as tk
from tkinter import messagebox


TAPE_INPUT = "1010"
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400


def build_tape_display(parent, symbols):
    frame = tk.Frame(parent)
    frame.pack(pady=10)
    labels = []
    for col, sym in enumerate(symbols):
        lbl = tk.Label(
            frame, text=sym, font=("Courier", 18, "bold"),
            width=3, relief=tk.SOLID, bd=2, bg="white"
        )
        lbl.grid(row=0, column=col, padx=2)
        labels.append(lbl)
    return labels


def build_info_row(parent, title, initial, color="black"):
    tk.Label(parent, text=title).pack()
    value_lbl = tk.Label(
        parent, text=initial, font=("Arial", 14, "bold"), fg=color
    )
    value_lbl.pack()
    return value_lbl


def build_outcome_panel(parent):
    wrapper = tk.Frame(parent)
    wrapper.pack(pady=20)
    denied = tk.Label(
        wrapper, text="Reject", font=("Arial", 14, "bold"),
        bg="red", fg="white", width=10, height=2
    )
    denied.grid(row=0, column=0, padx=10)
    approved = tk.Label(
        wrapper, text="Accept", font=("Arial", 14, "bold"),
        bg="green", fg="white", width=10, height=2
    )
    approved.grid(row=0, column=1, padx=10)
    return denied, approved


class TapeRunner:
    def __init__(self, window, symbols):
        self._win = window
        self._symbols = symbols
        self._cursor = 0
        self._iterations = 0
        self._current_state = None

        tk.Label(
            window, text="Automata Scanner", font=("Arial", 16, "bold")
        ).pack(pady=10)

        self._tape_labels = build_tape_display(window, symbols)
        self._iter_display = build_info_row(window, "Iteration (i):", "0", "blue")
        self._state_display = build_info_row(window, "State:", "None")
        self._rej_indicator, self._acc_indicator = build_outcome_panel(window)

        controls = tk.Frame(window)
        controls.pack(pady=20)
        for idx, (label, colour, handler) in enumerate([
            ("Start()", "green", self._on_start),
            ("Step()", "blue", self._on_step),
            ("Stop()", "red", self._on_stop),
        ]):
            btn = tk.Button(
                controls, text=label, fg=colour,
                font=("Arial", 11, "bold"),
                width=10, command=handler
            )
            btn.grid(row=0, column=idx, padx=5)

    def _read_head(self):
        if self._cursor < len(self._symbols):
            return int(self._symbols[self._cursor])
        return "#"

    def _reset_tape_colors(self):
        for lbl in self._tape_labels:
            lbl.config(bg="white")

    def _on_start(self):
        self._cursor = 0
        self._iterations = 0
        self._current_state = None
        self._iter_display.config(text="0")
        self._state_display.config(text="None")
        self._reset_tape_colors()
        print("Started: i = 0")

    def _on_step(self):
        reading = self._read_head()

        if reading == "#":
            self._evaluate_result()
            return

        active_label = self._tape_labels[self._cursor]
        active_label.config(bg="yellow")
        self._win.update()
        self._win.after(200)

        if reading == 1:
            self._current_state = "A"
            self._state_display.config(text="A", fg="red")
            active_label.config(bg="#ffcccc")
        else:
            self._current_state = "B"
            self._state_display.config(text="B", fg="blue")
            active_label.config(bg="#ccccff")

        self._cursor += 1
        self._iterations += 1
        self._iter_display.config(text=str(self._iterations))
        print(f"Step {self._iterations}: y={reading}, State={self._current_state}")

    def _evaluate_result(self):
        if self._current_state == "B":
            messagebox.showinfo("Result", "ACCEPTED\nFinal State: B")
            self._acc_indicator.config(relief=tk.SUNKEN)
            self._rej_indicator.config(relief=tk.RAISED)
        else:
            messagebox.showerror("Result", "REJECTED\nFinal State: A")
            self._rej_indicator.config(relief=tk.SUNKEN)
            self._acc_indicator.config(relief=tk.RAISED)

    def _on_stop(self):
        print("Stopped")
        self._win.quit()


def main():
    root = tk.Tk()
    root.title("Automata Simulator")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    TapeRunner(root, TAPE_INPUT)
    root.mainloop()


if __name__ == "__main__":
    main()
