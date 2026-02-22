"""Tkinter UI for interactively exploring number base conversions."""
from __future__ import annotations

from numbases.bases import from_base, to_base


def main() -> None:
    try:
        import tkinter as tk
        from tkinter import ttk
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Tkinter is not available. Install it (for Ubuntu: `sudo apt-get install python3-tk`) "
            "to run the visual UI."
        ) from exc

    class BaseExplorerApp(tk.Tk):
        """Desktop app for converting numbers across bases."""

        def __init__(self) -> None:
            super().__init__()
            self.title("numbases explorer")
            self.geometry("760x420")
            self.minsize(680, 360)

            self.input_value = tk.StringVar(value="101")
            self.input_base = tk.StringVar(value="2")
            self.custom_base = tk.StringVar(value="3")
            self.decimal_value = tk.StringVar(value="-")
            self.custom_value = tk.StringVar(value="-")
            self.status_text = tk.StringVar(value="Enter a number and click Convert.")
            self.common_vars = {base: tk.StringVar(value="-") for base in (2, 8, 10, 16, 36)}
            self.last_decimal: int | None = None

            self._build()
            self.bind("<Return>", self._on_convert)
            self.custom_base.trace_add("write", self._on_custom_base_changed)

        def _build(self) -> None:
            pad = {"padx": 10, "pady": 8}

            root = ttk.Frame(self, padding=14)
            root.pack(fill=tk.BOTH, expand=True)

            title = ttk.Label(root, text="Explore Number Bases", font=("TkDefaultFont", 14, "bold"))
            title.grid(row=0, column=0, columnspan=3, sticky="w")

            input_box = ttk.LabelFrame(root, text="Input", padding=12)
            input_box.grid(row=1, column=0, sticky="nsew", **pad)

            ttk.Label(input_box, text="Number").grid(row=0, column=0, sticky="w")
            number_entry = ttk.Entry(input_box, textvariable=self.input_value, width=32)
            number_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(2, 10))
            number_entry.focus_set()

            ttk.Label(input_box, text="Input Base (2-36)").grid(row=2, column=0, sticky="w")
            in_base = ttk.Spinbox(
                input_box,
                from_=2,
                to=36,
                increment=1,
                textvariable=self.input_base,
                width=8,
            )
            in_base.grid(row=2, column=1, sticky="w")

            controls = ttk.Frame(input_box)
            controls.grid(row=3, column=0, columnspan=2, sticky="w", pady=(12, 0))
            ttk.Button(controls, text="Convert", command=self.convert).pack(side=tk.LEFT)
            ttk.Button(controls, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=(8, 0))

            output_box = ttk.LabelFrame(root, text="Outputs", padding=12)
            output_box.grid(row=1, column=1, sticky="nsew", **pad)

            ttk.Label(output_box, text="Decimal value").grid(row=0, column=0, sticky="w")
            ttk.Label(output_box, textvariable=self.decimal_value, font=("TkDefaultFont", 12, "bold")).grid(
                row=0, column=1, sticky="w"
            )

            row = 1
            for base in (2, 8, 10, 16, 36):
                ttk.Label(output_box, text=f"Base {base}").grid(row=row, column=0, sticky="w")
                ttk.Label(output_box, textvariable=self.common_vars[base]).grid(row=row, column=1, sticky="w")
                row += 1

            custom_box = ttk.LabelFrame(root, text="Custom Base", padding=12)
            custom_box.grid(row=1, column=2, sticky="nsew", **pad)
            ttk.Label(custom_box, text="Base (2-36)").grid(row=0, column=0, sticky="w")
            out_base = ttk.Spinbox(
                custom_box,
                from_=2,
                to=36,
                increment=1,
                textvariable=self.custom_base,
                width=8,
            )
            out_base.grid(row=1, column=0, sticky="w", pady=(2, 10))

            ttk.Label(custom_box, text="Representation").grid(row=2, column=0, sticky="w")
            ttk.Label(custom_box, textvariable=self.custom_value, font=("TkDefaultFont", 11, "bold")).grid(
                row=3, column=0, sticky="w", pady=(2, 0)
            )

            status = ttk.Label(root, textvariable=self.status_text, foreground="#334155")
            status.grid(row=2, column=0, columnspan=3, sticky="w", padx=12, pady=(2, 0))

            root.columnconfigure(0, weight=2)
            root.columnconfigure(1, weight=2)
            root.columnconfigure(2, weight=1)
            root.rowconfigure(1, weight=1)

        def _on_convert(self, _: object) -> None:
            self.convert()

        def _on_custom_base_changed(self, *_: object) -> None:
            if self.last_decimal is None:
                self.custom_value.set("-")
                return
            try:
                base = self._parse_base(self.custom_base.get(), "custom output base")
                self.custom_value.set(to_base(self.last_decimal, base))
            except Exception:
                self.custom_value.set("Invalid base")

        def _parse_base(self, raw_base: str, label: str) -> int:
            try:
                base = int(raw_base)
            except ValueError as exc:
                raise ValueError(f"{label} must be an integer in 2..36") from exc
            if base < 2 or base > 36:
                raise ValueError(f"{label} must be in range 2..36")
            return base

        def convert(self) -> None:
            try:
                value_text = self.input_value.get().strip()
                if not value_text:
                    raise ValueError("number input cannot be empty")

                input_base = self._parse_base(self.input_base.get(), "input base")
                decimal = from_base(value_text, input_base)
                self.last_decimal = decimal
                self.decimal_value.set(str(decimal))

                for base in self.common_vars:
                    self.common_vars[base].set(to_base(decimal, base))

                custom_base = self._parse_base(self.custom_base.get(), "custom output base")
                self.custom_value.set(to_base(decimal, custom_base))
                self.status_text.set("Converted successfully.")
            except Exception as exc:
                self.last_decimal = None
                self.decimal_value.set("-")
                for value in self.common_vars.values():
                    value.set("-")
                self.custom_value.set("-")
                self.status_text.set(f"Error: {exc}")

        def clear(self) -> None:
            self.input_value.set("")
            self.input_base.set("10")
            self.custom_base.set("2")
            self.last_decimal = None
            self.decimal_value.set("-")
            for value in self.common_vars.values():
                value.set("-")
            self.custom_value.set("-")
            self.status_text.set("Cleared.")

    app = BaseExplorerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
