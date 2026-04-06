"""
ReClick | https://github.com/ree-verse/ReClick
Minimalist auto-clicker built with CustomTkinter.

Copyright © 2026 Ree-verse. All rights reserved.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""

import os
import threading
import time

import customtkinter as ctk
import keyboard
import mouse

ctk.set_appearance_mode(
    "system" if os.name == "nt" else "dark"
)  # On Linux, automatic theme detection isn't working at the moment
ctk.set_default_color_theme(
    "dark-blue"
)  # You can also choose "green" if you want a greener look


class ReClick(ctk.CTk):
    HOTKEYS = {
        "start": "F6",
        "stop": "F7",
        "toggle": "F8",
    }  # Adjust them if they don't fit

    def __init__(self):
        super().__init__()

        self.title("ReClick")
        self.geometry("350x550")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)

        self._running = False
        self._thread: threading.Thread | None = None

        self._build_ui()
        self._register_hotkeys()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # UI Construction

    def _build_ui(self):
        fw = {"padx": 16, "sticky": "ew", "pady": (2, 0)}

        # Click Interval
        self._heading("Click Interval", row=0)
        f = ctk.CTkFrame(self)
        f.grid(row=1, column=0, **fw)
        self._interval_entries = self._time_row(
            f,
            ("Hours", "Min", "Sec", "Ms"),
            (0, 0, 0, 100),
        )

        # Click Options
        self._heading("Click Options", row=2)
        f = ctk.CTkFrame(self)
        f.grid(row=3, column=0, **fw)
        f.grid_columnconfigure((0, 1), weight=1)
        self._btn_opt = self._dropdown(
            f,
            "Mouse Button",
            ["Left", "Right", "Middle"],
            col=0,
        )
        self._type_opt = self._dropdown(
            f,
            "Click Type",
            ["Single", "Double"],
            col=1,
        )

        # Click Repeat
        self._heading("Click Repeat", row=4)
        f = ctk.CTkFrame(self)
        f.grid(row=5, column=0, **fw)
        self._repeat_var = ctk.StringVar(value="infinite")

        finite_row = ctk.CTkFrame(f, fg_color="transparent")
        finite_row.pack(fill="x", padx=10, pady=(8, 2))
        ctk.CTkRadioButton(
            finite_row,
            text="Repeat",
            variable=self._repeat_var,
            value="finite",
            width=80,
        ).pack(side="left")
        self._repeat_n = ctk.CTkEntry(finite_row, width=60, justify="center")
        self._repeat_n.insert(0, "1")
        self._repeat_n.pack(side="left", padx=4)
        ctk.CTkLabel(finite_row, text="times").pack(side="left")

        ctk.CTkRadioButton(
            f,
            text="Infinite (repeat until stopped)",
            variable=self._repeat_var,
            value="infinite",
        ).pack(anchor="w", padx=10, pady=(2, 8))

        # Click Position
        self._heading("Click Position", row=6)
        f = ctk.CTkFrame(self)
        f.grid(row=7, column=0, **fw)
        self._pos_var = ctk.StringVar(value="current")

        ctk.CTkRadioButton(
            f,
            text="Current cursor position",
            variable=self._pos_var,
            value="current",
        ).pack(anchor="w", padx=10, pady=(8, 2))

        fixed_row = ctk.CTkFrame(f, fg_color="transparent")
        fixed_row.pack(fill="x", padx=10, pady=(2, 8))
        ctk.CTkRadioButton(
            fixed_row,
            text="",
            variable=self._pos_var,
            value="fixed",
            width=20,
        ).pack(side="left")
        self._pos_x = self._coord_entry(fixed_row, "X")
        self._pos_y = self._coord_entry(fixed_row, "Y")
        ctk.CTkButton(
            fixed_row,
            text="Pick",
            width=50,
            command=self._pick_location,
        ).pack(side="left", padx=(12, 0))

        # Hotkey hint
        hint = "  |  ".join(
            f"{key} {action.title()}" for action, key in self.HOTKEYS.items()
        )
        ctk.CTkLabel(
            self,
            text=hint,
            text_color="gray",
            font=ctk.CTkFont(size=11),
        ).grid(row=8, column=0, pady=(14, 0))

        # Start / Stop
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=9, column=0, pady=10)
        self._start_btn = ctk.CTkButton(
            btn_frame,
            text="▶  Start",
            width=150,
            command=self.start,
            fg_color="#2b8a3e",
            hover_color="#237032",
        )
        self._start_btn.pack(side="left", padx=6)
        self._stop_btn = ctk.CTkButton(
            btn_frame,
            text="■  Stop",
            width=150,
            command=self.stop,
            fg_color="#c92a2a",
            hover_color="#a61e1e",
            state="disabled",
        )
        self._stop_btn.pack(side="left", padx=6)

    # Reusable widget builders

    def _heading(self, text: str, row: int):
        ctk.CTkLabel(
            self,
            text=text,
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=row, column=0, padx=16, pady=(12, 0), sticky="w")

    @staticmethod
    def _time_row(parent, labels, defaults):
        entries = []
        for i, (label, default) in enumerate(zip(labels, defaults)):
            parent.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(parent, text=label).grid(row=0, column=i, pady=(6, 0))
            entry = ctk.CTkEntry(parent, width=55, justify="center")
            entry.insert(0, str(default))
            entry.grid(row=1, column=i, padx=8, pady=(2, 8))
            entries.append(entry)
        return entries

    @staticmethod
    def _dropdown(parent, label, values, col):
        ctk.CTkLabel(parent, text=label).grid(row=0, column=col, pady=(6, 0))
        menu = ctk.CTkOptionMenu(parent, values=values, width=120)
        menu.grid(row=1, column=col, padx=10, pady=(2, 8))
        return menu

    @staticmethod
    def _coord_entry(parent, label):
        ctk.CTkLabel(parent, text=f"{label}:").pack(side="left", padx=(6, 2))
        entry = ctk.CTkEntry(parent, width=55, justify="center")
        entry.insert(0, "0")
        entry.pack(side="left")
        return entry

    # Value helpers

    @staticmethod
    def _int(entry, fallback: int = 0) -> int:
        try:
            return max(0, int(entry.get()))
        except (ValueError, TypeError):
            return fallback

    def _interval_sec(self) -> float:
        h, m, s, ms = (self._int(e) for e in self._interval_entries)
        return max(h * 3600 + m * 60 + s + ms / 1000, 0.001)

    # Position picker

    def _pick_location(self):
        if self._running:
            return
        self._pos_var.set("fixed")
        self.withdraw()

        def _wait_for_click():
            time.sleep(0.4)
            mouse.wait(button="left", target_types=("down",))
            x, y = mouse.get_position()
            self.after(0, lambda: self._finish_pick(x, y))

        threading.Thread(target=_wait_for_click, daemon=True).start()

    def _finish_pick(self, x: int, y: int):
        for entry, value in ((self._pos_x, x), (self._pos_y, y)):
            entry.delete(0, "end")
            entry.insert(0, str(value))
        self.deiconify()

    # Button state

    def _set_buttons(self, active: bool):
        def _apply():
            self._start_btn.configure(
                state="disabled" if active else "normal",
            )
            self._stop_btn.configure(
                state="normal" if active else "disabled",
            )

        try:
            self.after(0, _apply)
        except RuntimeError:
            pass  # window already destroyed

    # Interruptible sleep

    def _sleep(self, seconds: float):
        """Sleep in small chunks so stop responds instantly."""
        deadline = time.perf_counter() + seconds
        while self._running and time.perf_counter() < deadline:
            remaining = deadline - time.perf_counter()
            time.sleep(min(0.05, max(0, remaining)))

    # Core logic

    def _register_hotkeys(self):
        for action, key in self.HOTKEYS.items():
            keyboard.add_hotkey(key, getattr(self, action))

    def start(self):
        if self._running:
            return
        self._running = True
        self._set_buttons(active=True)
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        self._set_buttons(active=False)

    def toggle(self):
        (self.stop if self._running else self.start)()

    def _loop(self):
        # Snapshot every setting once so mid-run edits don't cause chaos.
        interval = self._interval_sec()
        button = self._btn_opt.get().lower()
        double = self._type_opt.get() == "Double"
        infinite = self._repeat_var.get() == "infinite"
        limit = self._int(self._repeat_n, 1) if not infinite else 0
        fixed = self._pos_var.get() == "fixed"
        fx, fy = (self._int(self._pos_x), self._int(self._pos_y)) if fixed else (0, 0)

        click = mouse.double_click if double else mouse.click

        i = 0
        while self._running and (infinite or i < limit):
            if fixed:
                mouse.move(fx, fy)
            click(button)
            i += 1
            self._sleep(interval)

        self._running = False
        self._set_buttons(active=False)

    # Cleanup

    def _on_close(self):
        self._running = False
        keyboard.unhook_all()
        self.destroy()


if __name__ == "__main__":
    ReClick().mainloop()
