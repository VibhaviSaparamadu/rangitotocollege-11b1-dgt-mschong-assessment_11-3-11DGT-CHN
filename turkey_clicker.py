import tkinter as tk
import random
from utils import stats

root = tk.Tk()
root.title("Turkey Clicker") #game title
root.geometry("400x400")
root.resizable(False, False)

canvas = tk.Canvas(root, width=400, height=400, bg="#ff8585")
canvas.pack()

# level configurations
levels = {
    1: {"time": 40, "size": 50},
    2: {"time": 30, "size": 40},
    3: {"time": 20, "size": 30},
}

#variables
score = 0
time_left = 30
running = False
turkey_parts = []
rect = None
level = 2

high_scores = {1: None, 2: None, 3: None}

#random color generator
def random_color():
    r = random.randint(200, 255)
    g = random.randint(200, 255)
    b = random.randint(200, 255)
    return f'#{r:02x}{g:02x}{b:02x}'

def draw_turkey():
    global turkey_parts, rect
    for p in turkey_parts:
        canvas.delete(p)
    if rect:
        canvas.delete(rect)
    turkey_parts = []

    s = turkey_size
    base = 40
    scale = s / base
    max_x = max(0, 400 - int(base * scale + 50 * scale))
    max_y = max(60, 400 - int(base * scale + 60 * scale))
    x = random.randint(0, max_x)
    y = random.randint(60, max_y)
    def sx(a): return int(x + a * scale)
    def sy(a): return int(y + a * scale)

    #turkey parts
    body = canvas.create_oval(sx(0), sy(0), sx(40), sy(40), fill="#8B4513", outline="")
    head = canvas.create_oval(sx(25), sy(-15), sx(40), sy(10), fill="#DEB887", outline="")
    beak = canvas.create_polygon(sx(37), sy(-5), sx(45), sy(0), sx(37), sy(5), fill="orange", outline="")
    eye = canvas.create_oval(sx(33), sy(-10), sx(36), sy(-7), fill="black", outline="")
    wattle = canvas.create_oval(sx(38), sy(0), sx(42), sy(8), fill="red", outline="")
    tail1 = canvas.create_oval(sx(-10), sy(10), sx(10), sy(30), fill="#FFD700", outline="")
    tail2 = canvas.create_oval(sx(-5), sy(-5), sx(15), sy(15), fill="#FF8C00", outline="")
    tail3 = canvas.create_oval(sx(0), sy(-15), sx(20), sy(5), fill="#A0522D", outline="")
    leg1 = canvas.create_line(sx(12), sy(40), sx(12), sy(52), fill="#DEB887", width=int(3 * scale))
    leg2 = canvas.create_line(sx(28), sy(40), sx(28), sy(52), fill="#DEB887", width=int(3 * scale))
    turkey_parts = [body, head, beak, eye, wattle, tail1, tail2, tail3, leg1, leg2]
    rect = canvas.create_rectangle(sx(0), sy(0), sx(40), sy(40), outline="")

def click(event):
    global score
    if not running:
        return
    items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    hit = any(i in turkey_parts for i in items)
    if hit:
        for p in turkey_parts:
            canvas.itemconfig(p, fill="red")
        canvas.update()
        score += 1 #upon user click, score increases by 1
        canvas.itemconfig(score_text, text="Score: " + str(score))
        root.after(50, draw_turkey)
    else:
        end_game("Game Lost!") #if user click on background, game ends

def timer():
    global time_left
    if not running:
        return
    if time_left > 0:
        time_left -= 1
        canvas.itemconfig(timer_text, text="Time: " + str(time_left))
        root.after(1000, timer)
    else:
        end_game("Time's Up!") #when time reaches 0, game ends

def end_game(text):
    global running
    running = False
    if stats.player_stats["high_score"] is None or score > stats.player_stats["high_score"]:
        stats.update_stats(high_score=score)
    if "Lost" in text or "Time" in text:
        stats.update_stats(losses=stats.player_stats["losses"] + 1)
    else:
        stats.update_stats(wins=stats.player_stats["wins"] + 1)
        
    canvas.create_text(200, 200, text=text, font=("Arial", 20), fill="red")
    canvas.create_text(200, 240, text=f"Score: {score}", font=("Arial Rounded MT Bold", 22, "bold"), fill="#2E8B57")
    root.after(2000, reset)

def reset():
    global score, time_left, running
    canvas.delete("all")
    canvas.config(bg=random_color())
    score = 0
    running = False
    time_left = levels[level]["time"]
    draw_hud()
    start_frame.place(relx=0.5, rely=0.5, anchor="center")

def start_game():
    global running, score, time_left, turkey_size, level
    running = True
    score = 0
    level = level_var.get()
    turkey_size = levels[level]["size"]
    time_left = levels[level]["time"]
    start_frame.place_forget()
    canvas.delete("all")
    canvas.config(bg=random_color())
    draw_hud()
    if high_scores[level] is not None: 
        canvas.create_text(200, 80, text=f"High Score: {high_scores[level]}", font=("Arial Rounded MT Bold", 16), fill="#5a3d9a")
    draw_turkey()
    timer()

def draw_hud():
    global timer_text, score_text 
    timer_text = canvas.create_text(200, 20, text="Time: " + str(time_left), font=("Arial Rounded MT Bold", 16), fill="#333")
    score_text = canvas.create_text(200, 50, text="Score: " + str(score), font=("Arial Rounded MT Bold", 16), fill="#333")
    #timer and score display
canvas.bind("<Button-1>", click)

start_frame = tk.Frame(root, bg="#e6f0ff", width=320, height=140, bd=2, relief="ridge")
level_var = tk.IntVar(value=2)

tk.Label( #game level selection menu
    start_frame,
    text="Choose Level:",
    font=("Arial Rounded MT Bold", 14, "bold"),
    bg=start_frame["bg"],
    fg="#3a4d63"
).pack(pady=(15, 5))

row = tk.Frame(start_frame, bg=start_frame["bg"])
row.pack(pady=5)
for i in [1, 2, 3]:
    tk.Radiobutton( #game level radio buttons
        row,
        text=f"Level {i}",
        variable=level_var,
        value=i,
        bg=start_frame["bg"],
        fg="#4a6480",
        font=("Arial Rounded MT Bold", 12),
        activebackground="#c7d9f3",
        activeforeground="#2a3b55",
        selectcolor="#a5b8d8",
        pady=2
    ).pack(side="left", padx=15)

tk.Button( #start game button
    start_frame,
    text="Start",
    command=start_game,
    font=("Arial Rounded MT Bold", 16, "bold"),
    bg="#74e478",
    fg="#ffffff",
    relief="flat",
    padx=15,
    pady=8,
    activebackground="#63a66d",
    activeforeground="#FFFFFF",
    cursor="hand2"
).pack(pady=(10, 12))

start_frame.place(relx=0.5, rely=0.5, anchor="center")
draw_hud()
root.mainloop()