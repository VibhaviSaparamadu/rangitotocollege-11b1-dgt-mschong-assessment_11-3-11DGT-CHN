import tkinter as tk
import random

def click(event):
    global score, rect, rect_coords, running
    if not running:
        return
    x1, y1, x2, y2 = rect_coords
    if x1 <= event.x <= x2 and y1 <= event.y <= y2:
        score += 1
        canvas.itemconfig(score_text, text="Score: " + str(score))
        spawn()
    else:
        end("Game Lost!")

def spawn():
    global rect, rect_coords
    if rect:
        canvas.delete(rect)
    x = random.randint(0, 360)
    y = random.randint(60, 360)
    rect = canvas.create_rectangle(x, y, x+40, y+40, fill="green")
    rect_coords = (x, y, x+40, y+40)

def timer():
    global time_left, running
    if not running:
        return
    if time_left > 0:
        time_left -= 1
        canvas.itemconfig(timer_text, text="Time: " + str(time_left))
        root.after(1000, timer)
    else:
        end("Time's Up!")

def end(msg):
    global running, rect, score, high_score
    running = False
    if rect:
        canvas.delete(rect)
    if score > high_score:
        high_score = score
    canvas.create_text(200, 200, text=msg, font=("Arial", 20), fill="red")
    canvas.create_text(
        200, 240,
        text=f"Score: {score}",
        font=("Arial Rounded MT Bold", 22, "bold"),  # Nice bold font for score
        fill="#2E8B57"
    )
    root.after(2000, reset)

def reset():
    global score, time_left, running, score_text, timer_text, high_score_text
    canvas.delete("all")
    score = 0
    time_left = 30
    running = False
    timer_text = canvas.create_text(200, 20, text="Time: 30", font=("Arial Rounded MT Bold", 16), fill="#333")
    score_text = canvas.create_text(200, 50, text="Score: 0", font=("Arial Rounded MT Bold", 16), fill="#333")
    high_score_text = canvas.create_text(200, 80, text=f"High Score: {high_score}", font=("Arial Rounded MT Bold", 16), fill="#FF8C00")
    start_btn.place(relx=0.5, rely=0.5, anchor="center")

def start_game():
    global running, score, time_left, timer_text, score_text, high_score_text
    running = True
    score = 0
    time_left = 30
    start_btn.place_forget()
    canvas.delete("all")
    timer_text = canvas.create_text(200, 20, text="Time: 30", font=("Arial Rounded MT Bold", 16), fill="#333")
    score_text = canvas.create_text(200, 50, text="Score: 0", font=("Arial Rounded MT Bold", 16), fill="#333")
    high_score_text = canvas.create_text(200, 80, text=f"High Score: {high_score}", font=("Arial Rounded MT Bold", 16), fill="#FF8C00")
    spawn()
    timer()

root = tk.Tk()
root.geometry("400x400")
canvas = tk.Canvas(root, width=400, height=400, bg="lightblue")
canvas.pack()
score = 0
time_left = 30
running = False
rect = None
rect_coords = (0,0,0,0)
timer_text = canvas.create_text(200, 20, text="Time: 30", font=("Arial Rounded MT Bold", 16), fill="#333")
score_text = canvas.create_text(200, 50, text="Score: 0", font=("Arial Rounded MT Bold", 16), fill="#333")
canvas.bind("<Button-1>", click)
start_btn = tk.Button(
    root,
    text="Start",
    command=start_game,
    font=("Arial Rounded MT Bold", 20, "bold"),
    bg="#4CAF50",
    fg="white",
    relief="flat",
    padx=20,
    pady=10
)
start_btn.place(relx=0.5, rely=0.5, anchor="center")
high_score = 0
high_score_text = None
root.mainloop()

