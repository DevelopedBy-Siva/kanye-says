import tkinter as tk
from tkinter import messagebox
import requests
from PIL import ImageTk


_WIDTH = 420
_HEIGHT = 420
_APP_NAME = "Kanye Says..."
_BACKGROUND_COLOR = "#FFF"

_QUOTE_BG_IMG = "./static/quote.png"

_BTN_HEIGHT = 140
_BTN_BG_IMG = "./static/character.png"

_API = "https://api.kanye.rest"


def _run() -> None:

    root = tk.Tk()
    root.minsize(width=_WIDTH, height=_HEIGHT)
    root.config(background=_BACKGROUND_COLOR, padx=10, pady=10)
    root.title(_APP_NAME)
    root.resizable(False, False)

    # Quotes container
    quotes_canvas = _canvas()
    quotes_img = ImageTk.PhotoImage(file=_QUOTE_BG_IMG)
    _ = _image(quotes_canvas, quotes_img)
    # Display quotes
    quote_text_id = quotes_canvas.create_text(
        _WIDTH / 2,
        _HEIGHT / 2 - 20,
        text="",
        font=("Ubuntu 24 bold"),
        width=quotes_img.width() - 30,
    )
    quotes_canvas.pack(expand=tk.YES, fill=tk.BOTH)

    # Button container
    btn_canvas = _canvas(height=_BTN_HEIGHT)
    btn_img = ImageTk.PhotoImage(file=_BTN_BG_IMG)
    btn = _image(btn_canvas, btn_img, height=_BTN_HEIGHT)

    # Bind the image to a button
    btn_canvas.tag_bind(
        btn,
        "<Button-1>",
        lambda _: _quotes(canvas=quotes_canvas, text_id=quote_text_id),
    )
    btn_canvas.pack(expand=tk.YES, fill=tk.BOTH)

    # Initial quote
    _quotes(canvas=quotes_canvas, text_id=quote_text_id)

    root.mainloop()


def _canvas(width: int = _WIDTH, height: int = _HEIGHT) -> tk.Canvas:
    """
    Helper method to create a Canvas
    """
    canvas = tk.Canvas(
        width=width,
        height=height,
        background=_BACKGROUND_COLOR,
        highlightthickness=0,
    )
    return canvas


def _image(
    parent: tk.Canvas,
    pi: ImageTk.PhotoImage,
    width: int = _WIDTH,
    height: int = _HEIGHT,
) -> int:
    """
    Helper method to create a Canvas Image
    """
    return parent.create_image(width / 2, height / 2, image=pi, anchor=tk.CENTER)


def _quotes(canvas: tk.Canvas, text_id: int):
    """
    Generate new quote and render on the screen
    """
    try:
        response = requests.get(_API)
        if response.status_code != 200:
            raise ValueError("No quotes retrieved.")
        json = response.json()
        canvas.itemconfig(text_id, text=json["quote"])
    except Exception as e:
        print(f"Unexpected Error: {e}")
        messagebox.showerror("Error", "Unable to retrieve quotes. Try again.")


if __name__ == "__main__":
    _run()
