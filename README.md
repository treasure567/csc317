# Line-by-Line Explanation of `main.py`

This document explains every line of the automata simulator in `main.py`.

---

## Lines 1–2: Imports

```python
import tkinter as tk
from tkinter import messagebox
```

- **Line 1** — Imports the `tkinter` library (Python's built-in GUI toolkit) and aliases it as `tk` for shorter references throughout the code.
- **Line 2** — Imports the `messagebox` submodule separately, which provides pop-up dialog boxes (info, error, warning) used later to show accept/reject results.

---

## Lines 5–7: Constants

```python
TAPE_INPUT = "1010"
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400
```

- **Line 5** — Defines the binary string `"1010"` that the automaton will scan. Each character (`1` or `0`) represents a symbol on the tape.
- **Line 6** — Sets the window width to 500 pixels.
- **Line 7** — Sets the window height to 400 pixels.

---

## Lines 10–21: `build_tape_display()` function

```python
def build_tape_display(parent, symbols):
```

- **Line 10** — Defines a function that creates the visual tape (a row of boxes) inside a given parent widget. `symbols` is the input string (e.g., `"1010"`).

```python
    frame = tk.Frame(parent)
    frame.pack(pady=10)
```

- **Line 11** — Creates a `Frame` widget (an invisible container) to hold the tape cells.
- **Line 12** — Packs the frame into the parent with 10 pixels of vertical padding.

```python
    labels = []
    for col, sym in enumerate(symbols):
```

- **Line 13** — Initialises an empty list to collect references to each tape cell label.
- **Line 14** — Loops over each character in `symbols`, with `col` as the index (used for grid positioning) and `sym` as the character itself.

```python
        lbl = tk.Label(
            frame, text=sym, font=("Courier", 18, "bold"),
            width=3, relief=tk.SOLID, bd=2, bg="white"
        )
```

- **Lines 15–18** — Creates a `Label` widget for one tape cell:
  - `text=sym` — displays the symbol (`"1"` or `"0"`).
  - `font=("Courier", 18, "bold")` — monospace bold font at size 18.
  - `width=3` — cell width in text units.
  - `relief=tk.SOLID, bd=2` — solid border with 2-pixel thickness.
  - `bg="white"` — white background (will change color during scanning).

```python
        lbl.grid(row=0, column=col, padx=2)
        labels.append(lbl)
    return labels
```

- **Line 19** — Places the label in the grid at row 0, column = its index, with 2px horizontal padding.
- **Line 20** — Appends the label reference to the list.
- **Line 21** — Returns the list of all tape cell labels so they can be updated later.

---

## Lines 24–30: `build_info_row()` function

```python
def build_info_row(parent, title, initial, color="black"):
```

- **Line 24** — Defines a helper that creates a title label and a value label stacked vertically. Used for the iteration counter and state display.

```python
    tk.Label(parent, text=title).pack()
```

- **Line 25** — Creates and packs a simple text label showing the title (e.g., `"Iteration (i):"`).

```python
    value_lbl = tk.Label(
        parent, text=initial, font=("Arial", 14, "bold"), fg=color
    )
    value_lbl.pack()
    return value_lbl
```

- **Lines 26–30** — Creates a bold label showing the initial value (e.g., `"0"` or `"None"`), with a configurable text color. Packs it and returns it so the caller can update the text later.

---

## Lines 33–46: `build_outcome_panel()` function

```python
def build_outcome_panel(parent):
```

- **Line 33** — Defines a function that creates the Reject/Accept indicator labels.

```python
    wrapper = tk.Frame(parent)
    wrapper.pack(pady=20)
```

- **Lines 34–35** — Creates a frame container with vertical padding.

```python
    denied = tk.Label(
        wrapper, text="Reject", font=("Arial", 14, "bold"),
        bg="red", fg="white", width=10, height=2
    )
    denied.grid(row=0, column=0, padx=10)
```

- **Lines 36–40** — Creates a red label that says "Reject" and places it in the left column. It acts as a visual indicator (its relief changes when the tape is rejected).

```python
    approved = tk.Label(
        wrapper, text="Accept", font=("Arial", 14, "bold"),
        bg="green", fg="white", width=10, height=2
    )
    approved.grid(row=0, column=1, padx=10)
    return denied, approved
```

- **Lines 41–46** — Same idea but for "Accept" in green, placed in the right column. Returns both labels as a tuple.

---

## Lines 49–78: `TapeRunner` class — `__init__`

```python
class TapeRunner:
    def __init__(self, window, symbols):
```

- **Lines 49–50** — Defines the main class that controls the entire simulation. It takes the root `window` and the `symbols` string.

```python
        self._win = window
        self._symbols = symbols
        self._cursor = 0
        self._iterations = 0
        self._current_state = None
```

- **Lines 51–55** — Stores instance variables:
  - `_win` — reference to the tkinter root window.
  - `_symbols` — the tape input string.
  - `_cursor` — current position of the read head on the tape (starts at 0).
  - `_iterations` — counts how many steps have been taken.
  - `_current_state` — tracks the automaton's current state (`"A"`, `"B"`, or `None`).

```python
        tk.Label(
            window, text="Automata Scanner", font=("Arial", 16, "bold")
        ).pack(pady=10)
```

- **Lines 57–59** — Creates and packs a title label at the top of the window.

```python
        self._tape_labels = build_tape_display(window, symbols)
        self._iter_display = build_info_row(window, "Iteration (i):", "0", "blue")
        self._state_display = build_info_row(window, "State:", "None")
        self._rej_indicator, self._acc_indicator = build_outcome_panel(window)
```

- **Lines 61–64** — Builds all the UI sections by calling the helper functions, and stores references to the widgets that need to be updated during the simulation.

```python
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
```

- **Lines 66–78** — Creates the three control buttons (Start, Step, Stop) in a loop:
  - Each button gets colored text (`fg=colour`) and a bold font.
  - `command=handler` binds the button click to the appropriate method.
  - They are laid out horizontally using `grid`.

---

## Lines 80–83: `_read_head()` method

```python
    def _read_head(self):
        if self._cursor < len(self._symbols):
            return int(self._symbols[self._cursor])
        return "#"
```

- **Line 80** — Reads the symbol at the current cursor position.
- **Lines 81–82** — If the cursor is still within the tape, returns the symbol as an integer (`0` or `1`).
- **Line 83** — If the cursor has moved past the end of the tape, returns `"#"` to signal there is nothing left to read.

---

## Lines 85–87: `_reset_tape_colors()` method

```python
    def _reset_tape_colors(self):
        for lbl in self._tape_labels:
            lbl.config(bg="white")
```

- Loops through every tape cell label and resets its background to white. Used when restarting the simulation.

---

## Lines 89–96: `_on_start()` method

```python
    def _on_start(self):
        self._cursor = 0
        self._iterations = 0
        self._current_state = None
        self._iter_display.config(text="0")
        self._state_display.config(text="None")
        self._reset_tape_colors()
        print("Started: i = 0")
```

- **Lines 90–91** — Resets the cursor to the beginning and the step counter to zero.
- **Line 92** — Clears the automaton state.
- **Lines 93–94** — Updates the on-screen iteration and state displays to their initial values.
- **Line 95** — Resets all tape cell colors to white.
- **Line 96** — Prints a console message for debugging.

---

## Lines 98–122: `_on_step()` method

```python
    def _on_step(self):
        reading = self._read_head()
```

- **Lines 98–99** — Reads the current tape symbol.

```python
        if reading == "#":
            self._evaluate_result()
            return
```

- **Lines 101–103** — If the tape is exhausted (`"#"`), evaluate the final state and stop stepping.

```python
        active_label = self._tape_labels[self._cursor]
        active_label.config(bg="yellow")
        self._win.update()
        self._win.after(200)
```

- **Lines 105–108** — Highlights the current tape cell in yellow, forces the window to redraw (`update()`), then pauses for 200 milliseconds to create a brief visual flash before the final color is applied.

```python
        if reading == 1:
            self._current_state = "A"
            self._state_display.config(text="A", fg="red")
            active_label.config(bg="#ffcccc")
        else:
            self._current_state = "B"
            self._state_display.config(text="B", fg="blue")
            active_label.config(bg="#ccccff")
```

- **Lines 110–117** — The automaton's transition logic:
  - If the symbol is `1`: go to state **A**, display "A" in red, color the cell light red.
  - If the symbol is `0`: go to state **B**, display "B" in blue, color the cell light blue.

```python
        self._cursor += 1
        self._iterations += 1
        self._iter_display.config(text=str(self._iterations))
        print(f"Step {self._iterations}: y={reading}, State={self._current_state}")
```

- **Lines 119–122** — Advances the cursor to the next cell, increments the step counter, updates the iteration display, and prints the step info to the console.

---

## Lines 124–132: `_evaluate_result()` method

```python
    def _evaluate_result(self):
        if self._current_state == "B":
            messagebox.showinfo("Result", "ACCEPTED\nFinal State: B")
            self._acc_indicator.config(relief=tk.SUNKEN)
            self._rej_indicator.config(relief=tk.RAISED)
        else:
            messagebox.showerror("Result", "REJECTED\nFinal State: A")
            self._rej_indicator.config(relief=tk.SUNKEN)
            self._acc_indicator.config(relief=tk.RAISED)
```

- **Lines 125–128** — If the final state is **B** (accepting state): show an info dialog saying "ACCEPTED" and visually press the Accept indicator (sunken relief) while raising the Reject indicator.
- **Lines 129–132** — Otherwise (state is **A** or `None`): show an error dialog saying "REJECTED" and press the Reject indicator.

---

## Lines 134–136: `_on_stop()` method

```python
    def _on_stop(self):
        print("Stopped")
        self._win.quit()
```

- Prints "Stopped" to the console and closes the tkinter event loop, terminating the application.

---

## Lines 139–148: `main()` and entry point

```python
def main():
    root = tk.Tk()
    root.title("Automata Simulator")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    TapeRunner(root, TAPE_INPUT)
    root.mainloop()
```

- **Line 140** — Creates the root tkinter window.
- **Line 141** — Sets the window title to "Automata Simulator".
- **Line 142** — Sets the window size to 500x400 using the constants.
- **Line 143** — Instantiates `TapeRunner`, which builds the entire UI inside the root window.
- **Line 144** — Starts the tkinter event loop, which keeps the window open and responsive until `quit()` is called.

```python
if __name__ == "__main__":
    main()
```

- **Lines 147–148** — Standard Python entry-point guard. If this file is run directly (not imported as a module), it calls `main()` to launch the app.
