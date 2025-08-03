from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
    check_label.config(text="")
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 2 == 1:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
    else:
        if reps != 8:
            count_down(short_break_sec)
            timer_label.config(text="Break", fg=PINK, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
        else:
            count_down(long_break_sec)
            timer_label.config(text="Break", fg=RED, bg=YELLOW, font=(FONT_NAME, 35, "bold"))

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer

    # cosmetic
    count_min = math.floor(count / 60)
    count_sec =count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✓"
        check_label.config(text=marks)
# ---------------------------- UI SETUP ------------------------------- #
########## Create a window ##########
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

########## Canvas ##########
canvas = Canvas(bg=YELLOW, width=200, height=224,highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00.00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

########## Labels ##########
# Timer
timer_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
timer_label.grid(row=0, column=1)

# Check mark
check_label = Label(fg=GREEN, bg=YELLOW)
check_label.grid(row=3, column=1)

########## Button ##########
start_button = Button(text="Start", highlightbackground=YELLOW, command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", highlightbackground=YELLOW, command=reset_timer)
reset_button.grid(row=2, column=2)



# Keep the window open
window.mainloop()