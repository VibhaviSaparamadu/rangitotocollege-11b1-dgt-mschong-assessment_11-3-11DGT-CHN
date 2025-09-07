

import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()

popup = tk.Toplevel()
popup.geometry("400x250")
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
    if n == "" or not n.isalpha():
        messagebox.showwarning("Error", "Please enter a valid name!")
    else:
        name = n
        popup.destroy()

btn = tk.Button(popup, text="Let's Go!", font=("Lucida Console", 12, "bold"), bg="#4CAF50", fg="white", command=get_name)
btn.pack(pady=20)

popup.wait_window()

if name == "":
    root.destroy()
else:
    root.deiconify()
    root.title("The Great Games Compendium")
    root.geometry("1000x800")
    root.configure(bg="#add8e6")

    t1 = tk.Label(root, text="The Great Games Compendium", font=("Courier New", 36, "bold"), bg="#add8e6")
    t1.pack(pady=(30, 10))

    t2 = tk.Label(root, text="Welcome " + name + "!", font=("Lucida Console", 18), bg="#add8e6")
    t2.pack(pady=(0, 40))

    top = tk.Frame(root, bg="#add8e6")
    top.pack(fill="x")

    def show_stats():
        messagebox.showinfo("Stats", name + "'s stats will be shown here.")

    stats = tk.Button(top, text=name + "'s Stats", font=("Lucida Console", 10), command=show_stats)
    stats.pack(side="right", padx=20, pady=10)

    games = tk.Frame(root, bg="#add8e6")
    games.pack(pady=20)

    g1 = tk.Button(games, text="Game 1", width=20, height=4, font=("Courier New", 14))
    g2 = tk.Button(games, text="Game 2", width=20, height=4, font=("Courier New", 14))
    g3 = tk.Button(games, text="Game 3", width=20, height=4, font=("Courier New", 14))

    g1.grid(row=0, column=0, padx=20)
    g2.grid(row=0, column=1, padx=20)
    g3.grid(row=0, column=2, padx=20)

    g4 = tk.Button(root, text="Game 4", width=25, height=4, font=("Courier New", 14))
    g4.pack(pady=(30, 50))

    exit_btn = tk.Button(root, text="EXIT", bg="red", fg="white", width=15, height=2, font=("Courier New", 12, "bold"), command=root.quit)
    exit_btn.pack(side="bottom", pady=20)

    root.mainloop()


