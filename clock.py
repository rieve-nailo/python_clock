import math
import tkinter as tk
from datetime import datetime


BACKGROUND = "#101820"
FACE = "#f5f0e6"
INK = "#243447"
ACCENT = "#d85c41"


def hand_endpoint(
    center_x: float,
    center_y: float,
    length: float,
    angle: float,
) -> tuple[float, float]:
    return (
        center_x + length * math.sin(angle),
        center_y - length * math.cos(angle),
    )


def draw_clock(canvas: tk.Canvas, now: datetime) -> None:
    canvas.delete("all")

    width = canvas.winfo_width()
    height = canvas.winfo_height()
    center_x = width / 2
    center_y = height / 2
    radius = max(0, min(width, height) / 2 - 18)
    if radius < 20:
        return

    canvas.create_oval(
        center_x - radius,
        center_y - radius,
        center_x + radius,
        center_y + radius,
        fill=FACE,
        outline="#c9c0b2",
        width=max(2, int(radius * 0.025)),
    )

    for tick in range(60):
        angle = tick * math.tau / 60
        is_hour = tick % 5 == 0
        outer_x, outer_y = hand_endpoint(center_x, center_y, radius * 0.91, angle)
        inner_x, inner_y = hand_endpoint(
            center_x,
            center_y,
            radius * (0.79 if is_hour else 0.86),
            angle,
        )
        canvas.create_line(
            outer_x,
            outer_y,
            inner_x,
            inner_y,
            fill=INK if is_hour else "#a69d90",
            width=max(1, int(radius * (0.025 if is_hour else 0.009))),
            capstyle=tk.ROUND,
        )

    for hour in range(1, 13):
        angle = hour * math.tau / 12
        number_x, number_y = hand_endpoint(center_x, center_y, radius * 0.68, angle)
        canvas.create_text(
            number_x,
            number_y,
            text=str(hour),
            fill=INK,
            font=("Segoe UI", max(10, int(radius * 0.13)), "bold"),
        )

    second = now.second + now.microsecond / 1_000_000
    minute = now.minute + second / 60
    hour = now.hour % 12 + minute / 60
    hands = (
        (hour * math.tau / 12, radius * 0.48, max(3, int(radius * 0.055)), INK),
        (minute * math.tau / 60, radius * 0.70, max(2, int(radius * 0.035)), INK),
        (second * math.tau / 60, radius * 0.78, max(1, int(radius * 0.012)), ACCENT),
    )

    for angle, length, line_width, color in hands:
        end_x, end_y = hand_endpoint(center_x, center_y, length, angle)
        canvas.create_line(
            center_x,
            center_y,
            end_x,
            end_y,
            fill=color,
            width=line_width,
            capstyle=tk.ROUND,
        )

    cap_radius = max(4, int(radius * 0.045))
    canvas.create_oval(
        center_x - cap_radius,
        center_y - cap_radius,
        center_x + cap_radius,
        center_y + cap_radius,
        fill=ACCENT,
        outline=FACE,
        width=2,
    )


def main() -> None:
    window = tk.Tk()
    window.title("Analog Clock")
    window.configure(background=BACKGROUND)
    window.minsize(280, 280)
    window.geometry("420x420")

    canvas = tk.Canvas(
        window,
        background=BACKGROUND,
        highlightthickness=0,
    )
    canvas.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

    def update_clock() -> None:
        draw_clock(canvas, datetime.now())
        window.after(100, update_clock)

    update_clock()
    window.mainloop()


if __name__ == "__main__":
    main()
