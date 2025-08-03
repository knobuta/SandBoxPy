from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"

# ---------------------------- READ DATA ------------------------------- #
data = pandas.read_csv("data/french_words.csv")
to_learn = data.to_dict(orient="records")

# ---------------------------- PICK RANDOM WORD ------------------------------- #
def random_word():
    current_card = random.choice(to_learn)
    front_canvas.itemconfig(french_txt, text="French")
    front_canvas.itemconfig(french_word, text=current_card["French"])

# ---------------------------- UI SETUP ------------------------------- #
########## Window ##########
window = Tk()
window.title("flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

########## Canvas #########
# Create Front canvas for French word
front_canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR,
                      highlightthickness=0)
front_img = PhotoImage(file="images/card_front.png")
front_canvas.create_image(410, 273, image=front_img)
french_txt = front_canvas.create_text(410, 150, text="", fill="black", font=(FONT_NAME, 40, "italic"))
french_word = front_canvas.create_text(410, 263, text="", fill="black", font=(FONT_NAME, 60, "bold"))
front_canvas.grid(row=0, column=0, columnspan=2)

########## Button #########
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightbackground=BACKGROUND_COLOR,
                      command=random_word)
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image,  highlightbackground=BACKGROUND_COLOR,
                      command=random_word)
right_button.grid(row=1, column=1)

random_word()

# Keep the window open
window.mainloop()