""""""

import colorgram
import turtle as turtle_module
import random

# rgb_colors = []
# colors = colorgram.extract('hirst.jpg', 30)
# for color in colors:
#     r = color.rgb.r
#     g = color.rgb.g
#     b = color.rgb.b
#     new_color = (r, g, b)
#     rgb_colors.append(new_color)

# Extracted colors from an image using colorgram
color_list = [(251, 249, 245), (209, 165, 124), (249, 234, 236), (140, 49, 106), (164, 169, 38), (244, 80, 56),
              (228, 115, 163), (3, 143, 56), (215, 234, 231), (241, 65, 140), (1, 143, 184), (162, 55, 51),
              (50, 203, 226), (254, 230, 0), (20, 166, 126), (244, 223, 49), (210, 231, 234), (171, 186, 177),
              (27, 197, 220), (232, 165, 190), (233, 174, 161), (141, 213, 224), (191, 191, 193), (160, 211, 182),
              (105, 46, 100), (8, 117, 39)]

# Set up the dimensions of the drawing area
height = 10
width = 10

# Start point for the turtle
start_x = -200
start_y = -200

steps = 50  # Distance between each row of dots

def move_forward(times):
    """Moves the turtle forward a specified number of times with random color."""
    for _ in range(times):
        tim.forward(steps)
        tim.dot(20, random.choice(color_list))

# Initialize the turtle object
turtle_module.colormode(255) # Set the color mode to RGB
tim = turtle_module.Turtle() # Create a turtle object
tim.speed("fastest") # Set the speed of the turtle
tim.penup() # Lift the pen to avoid drawing lines
tim.hideturtle() # Hide the turtle cursor
tim.goto(-200, -200) # Move the turtle to the starting position

screen = turtle_module.Screen() # Create a screen object

# Draw the grid of dots
for i in range(height):
    tim.dot(20, random.choice(color_list))
    move_forward(width - 1)

    if i < height - 1:  # Avoid moving up after the last row
        tim.goto(start_x, start_y + steps * (i + 1))  # Move to the next row

screen = turtle_module.Screen()
screen.exitonclick()