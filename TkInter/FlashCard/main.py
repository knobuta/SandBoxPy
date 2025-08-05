from tkinter import *
import pandas
import random

from numpy.ma.core import filled

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"
current_card = {}
to_learn = {}

# ---------------------------- READ DATA ------------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# ---------------------------- PICK RANDOM WORD ------------------------------- #
def random_word(button_id):
    global current_card, flip_timer, to_learn
    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_txt, text="French", fill="black")
    canvas.itemconfig(canvas_word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_img, image=front_img)
    flip_timer = window.after(3000, func=flip_card)

    if button_id == 2:
        to_learn.remove(current_card)
        new_data = pandas.DataFrame(to_learn)
        new_data.to_csv("data/words_to_learn.csv", index=False)

def flip_card():
    canvas.itemconfig(canvas_txt, text="English", fill="white")
    canvas.itemconfig(canvas_word, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_img, image=back_img)

# ---------------------------- UI SETUP ------------------------------- #
########## Window ##########
window = Tk()
window.title("flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

########## Canvas #########
# Create Front canvas for French word
# front_canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR,
#                       highlightthickness=0)
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
canvas_img = canvas.create_image(410, 273)

# To change the image
canvas.itemconfig(canvas_img, image=front_img)
canvas_txt = canvas.create_text(410, 150, text="", fill="black", font=(FONT_NAME, 40, "italic"))
canvas_word = canvas.create_text(410, 263, text="", fill="black", font=(FONT_NAME, 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

########## Button #########
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightbackground=BACKGROUND_COLOR,
                      command=lambda: random_word(1))
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image,  highlightbackground=BACKGROUND_COLOR,
                      command=lambda: random_word(2))
right_button.grid(row=1, column=1)

random_word(0)


# Keep the window open
window.mainloop()