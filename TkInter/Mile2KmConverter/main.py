from tkinter import *

def miles_to_km():
    miles = float(input.get()) # to float
    km = miles * 1.60934
    km_output.config(text=f"{km}") # to string

########## Create a window ##########
window = Tk()
window.title("Mile to Km Converter")
window.minsize(width=500, height=300)
window.config(padx=100, pady=100)

########## Lables ##########
# Label: is equal to
equal_label = Label(text="is equal to", font=("Arial", 12))
equal_label.grid(column=0, row=1)

# Label: Miles
miles_label = Label(text="Miles", font=("Arial", 12))
miles_label.grid(column=2, row=0)

# Label: Km
km_label = Label(text="Km", font=("Arial", 12))
km_label.grid(column=2, row=1)

# Label: Output for Km
km_output = Label(text="0", font=("Arial", 12))
km_output.grid(column=1, row=1)

########## Button ##########
button = Button(text="Calculate", command=miles_to_km)
button.grid(column=1, row=2)

########## Entry ##########
input = Entry(width=7)
input.config(justify=CENTER, font=("Arial", 12))
input.insert(END, string="0")  # Optional: Set a default value at the center
input.grid(column=1, row=0)


# Keep the window open
window.mainloop()