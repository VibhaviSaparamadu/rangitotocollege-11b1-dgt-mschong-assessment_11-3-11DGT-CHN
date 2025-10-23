import tkinter as tk
from tkinter import messagebox
import subprocess
from utils import stats


wins = 0
lose = 0
h_score = 0
r_item = "None"

def launch_turkey_clicker():
    subprocess.Popen(["python", "turkey_clicker.py"])

def launch_lucky_spinner():
    subprocess.Popen(["python", "lucky_spinner.py"])

root = tk.Tk()
root.withdraw()
popup = tk.Toplevel()
popup.geometry("400x250")
popup.resizable(False, False)
popup.title("Welcome Player!")
popup.configure(bg="#add8e6")
popup.grab_set()

label = tk.Label(popup, text="Enter your name to begin!", bg="#add8e6", font=("Lucida Console", 16, "bold"))
label.pack(pady=(30, 10))
entry = tk.Entry(popup, font=("Courier New", 14), width=25, justify="center")
entry.pack(pady=10)
entry.focus()

name = ""
def get_name():
    global name
    n = entry.get().strip()
    if n == "" or not n.isalpha() or len(n) > 12:
        messagebox.showwarning("Error", "Your name must be alphabetic and under 12 characters.")
    else:
        name = n
        popup.destroy()

start_btn = tk.Button(popup, text="Let's Go!", font=("Lucida Console", 12, "bold"), bg="#4CAF50", fg="#FFFFFF", command=get_name)
start_btn.pack(pady=20)
popup.wait_window()

if name == "":
    root.destroy()
else:
    root.deiconify()
    root.title("The Great Games Compendium")
    root.geometry("1000x800")
    root.resizable(False, False)
    root.configure(bg="#add8e6")

    title1 = tk.Label(root, text="The Great Games Compendium", font=("Courier New", 36, "bold"), bg="#add8e6", fg="#004299")
    title1.pack(pady=(30, 10))
    title2 = tk.Label(root, text="Welcome " + name + "!", font=("Lucida Console", 18), bg="#add8e6", fg="#004299")
    title2.pack(pady=(0, 40))

    def show_stats():
        s = stats.player_stats
        messagebox.showinfo("Stats", f"{name}'s stats:\n\nWins = {s['wins']}\nLosses = {s['losses']}\nHighest Score = {s['high_score']}\nRarest Item = {s['rarest_item']}")


    top = tk.Frame(root, bg="#add8e6")
    top.pack(fill="x")
    stats_btn  = tk.Button(top, text=name + "'s Stats", font=("Lucida Console", 10), command=show_stats)
    stats_btn.pack(side="right", padx=20, pady=10)

    games = tk.Frame(root, bg="#add8e6")
    games.pack(pady=20)
    tk.Button(games, text="Turkey Clicker", width=20, height=5, font=("Courier New", 14), command=launch_turkey_clicker).grid(row=0, column=0, padx=20)
    tk.Button(games, text="Lucky Spinner", width=20, height=5, font=("Courier New", 14), command=launch_lucky_spinner).grid(row=0, column=1, padx=20)
    tk.Button(games, text="Falling Apples", width=20, height=5, font=("Courier New", 14)).grid(row=0, column=2, padx=20)

    tk.Button(root, text="Tic-Tac-Toe", width=25, height=5, font=("Courier New", 14)).pack(pady=(30, 50))
    tk.Button(root, text="EXIT", bg="#DF0000", fg="#FFFFFF", width=15, height=2, font=("Courier New", 12, "bold"), command=root.quit).pack(side="bottom", pady=90)

    root.mainloop()
