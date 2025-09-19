import tkinter as tk
import random

def click(event):
    global score, rect, rect_coords, running
    if not running:
        return
    clicked_items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    if any(item in turkey_parts for item in clicked_items):
        for part in turkey_parts:
            try:
                canvas.itemconfig(part, fill="red")
            except tk.TclError:
                pass
        canvas.update()
        score += 1
        canvas.itemconfig(score_text, text="Score: " + str(score))
        root.after(50, spawn)
    else:
        end("Game Lost!")

def spawn():
    global rect, rect_coords, turkey_parts
    if rect:
        canvas.delete(rect)
    for part in turkey_parts:
        canvas.delete(part)
    turkey_parts.clear()
    x = random.randint(0, 320)
    y = random.randint(60, 320)
    body = canvas.create_oval(x, y, x + 40, y + 40, fill="#8B4513", outline="")
    head = canvas.create_oval(x + 25, y - 15, x + 40, y + 10, fill="#DEB887", outline="")
    beak = canvas.create_polygon(x + 37, y - 5, x + 45, y, x + 37, y + 5, fill="orange", outline="")
    eye = canvas.create_oval(x + 33, y - 10, x + 36, y - 7, fill="black", outline="")
    wattle = canvas.create_oval(x + 38, y, x + 42, y + 8, fill="red", outline="")
    tail1 = canvas.create_oval(x - 10, y + 10, x + 10, y + 30, fill="#FFD700", outline="")
    tail2 = canvas.create_oval(x - 5, y - 5, x + 15, y + 15, fill="#FF8C00", outline="")
    tail3 = canvas.create_oval(x, y - 15, x + 20, y + 5, fill="#A0522D", outline="")
    leg1 = canvas.create_line(x + 12, y + 40, x + 12, y + 52, fill="#DEB887", width=3)
    leg2 = canvas.create_line(x + 28, y + 40, x + 28, y + 52, fill="#DEB887", width=3)
    turkey_parts.extend([body, head, beak, eye, wattle, tail1, tail2, tail3, leg1, leg2])
    rect = canvas.create_rectangle(x, y, x + 40, y + 40, outline="")
    rect_coords = (x, y, x + 40, y + 40)

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
        font=("Arial Rounded MT Bold", 22, "bold"),
        fill="#2E8B57"
    )
    root.after(2000, reset)

def reset():
    global score, time_left, running, score_text, timer_text, high_score_text
    canvas.delete("all")
    canvas.config(bg=random_light_color())
    score = 0
    time_left = 30
    running = False
    timer_text = canvas.create_text(200, 20, text="Time: 30", font=("Arial Rounded MT Bold", 16), fill="#333")
    score_text = canvas.create_text(200, 50, text="Score: 0", font=("Arial Rounded MT Bold", 16), fill="#333")
    high_score_text = canvas.create_text(200, 80, text=f"High Score: {high_score}", font=("Arial Rounded MT Bold", 16), fill="#EA00FF")
    start_btn.place(relx=0.5, rely=0.5, anchor="center")

def start_game():
    global running, score, time_left, timer_text, score_text, high_score_text
    running = True
    score = 0
    time_left = 30
    start_btn.place_forget()
    canvas.delete("all")
    canvas.config(bg=random_light_color())
    timer_text = canvas.create_text(200, 20, text="Time: 30", font=("Arial Rounded MT Bold", 16), fill="#333")
    score_text = canvas.create_text(200, 50, text="Score: 0", font=("Arial Rounded MT Bold", 16), fill="#333")
    high_score_text = canvas.create_text(200, 80, text=f"High Score: {high_score}", font=("Arial Rounded MT Bold", 16), fill="#7E0097")
    spawn()
    timer()

def random_light_color():
    r = random.randint(200, 255)
    g = random.randint(200, 255)
    b = random.randint(200, 255)
    return f'#{r:02x}{g:02x}{b:02x}'

root = tk.Tk()
root.geometry("400x400")
root.title("Turkey Clicker Game")
root.resizable(False, False)
canvas = tk.Canvas(root, width=400, height=400, bg="#ff8585")
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
turkey_parts = []
root.mainloop()
