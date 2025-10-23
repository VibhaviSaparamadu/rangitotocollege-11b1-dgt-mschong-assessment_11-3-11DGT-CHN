import tkinter as tk
from tkinter import ttk, messagebox
import random
from utils import stats

items = [
    ("Wood", "#a8e6cf", 30),
    ("Rubber", "#dcedc1", 28),
    ("Bone", "#ffd3b6", 15),
    ("Fossil", "#ffaaa5", 12),
    ("Iron", "#ff8b94", 6),
    ("Copper", "#fcb0b3", 5),
    ("Silver", "#c8a2c8", 3),
    ("Gold", "#fdd835", 2),
    ("Titanium", "#b39ddb", 2),
    ("Neodynium", "#ff80ab", 2),
    ("Oblivion", "#80cbc4", 2),
    ("Platanodynium", "#ffcc80", 2),
    ("Kyrpton", "#c5e1a5", 2),
    ("Vibranium", "#9fa8da", 2),
    ("Burger", "#fff59d", 2),
    ("Cheese Burger", "#ffe082", 2),
    ("Pineapple Burger", "#ffb74d", 1)
]

class SpinnerGame:
    def get_luck_boost(self):
        # Luck boost starts at 20 spins and will increase after that every 10 spins
        if self.spin_count < 20:
            return 0
        #will increase luck by 5% every 10 spins
        boost = 0.05 * ((self.spin_count - 20) // 10 + 1)
        return boost
    def __init__(self, root):
        self.win = root
        self.win.title("Lucky Spinner")
        self.win.geometry("420x470")
        self.win.config(bg="#f2f2ff")

        # simple font style setup
        self.bigfont = ("Verdana", 16, "bold")
        self.midfont = ("Calibri", 12, "bold")
        self.smallfont = ("Arial", 10)

        self.inv = {n: 0 for n, c, w in items}
        self.names = [n for n, c, w in items]
        self.colors = {n: c for n, c, w in items}
        self.weights = [w for n, c, w in items]

        # Track number of spins
        self.spin_count = 0
        title = tk.Label(self.win, text="Lucky Spinner", font=self.bigfont, bg="#d1c4e9", fg="#2e004f", pady=10)
        title.pack(fill="x")
        self.bar = ttk.Progressbar(self.win, orient="horizontal", length=300, mode="determinate")
        self.bar.pack(pady=15)
        self.txt = tk.Label(self.win, text="Click SPIN to try your luck!", bg="#ffffff", width=40, height=3,
                            wraplength=250, font=self.midfont, relief="solid", bd=1)
        self.txt.pack(pady=10)


        self.result = tk.Label(self.win, text="", bg="#f2f2ff", font=self.midfont)
        self.result.pack()

        # Luck boost label
        self.luck_label = tk.Label(self.win, text="Luck Boost: 0%", bg="#e1bee7", fg="#6a1b9a", font=("Verdana", 13, "bold"), relief="groove", bd=2, padx=8, pady=4)
        self.luck_label.pack(pady=4)

        # Total spins label
        self.spins_label = tk.Label(self.win, text="Total Spins: 0", bg="#ffe0b2", fg="#ef6c00", font=("Verdana", 13, "bold"), relief="groove", bd=2, padx=8, pady=4)
        self.spins_label.pack(pady=4)

        self.btn = tk.Button(self.win, text="SPIN!", font=self.bigfont, bg="#b2fab4", fg="#004d40",
                             activebackground="#81c784", command=self.spin)
        self.btn.pack(pady=20)

        self.storebtn = tk.Button(self.win, text="Storage", bg="#bbdefb", fg="#0d47a1", font=self.midfont,
                                  activebackground="#64b5f6", command=self.show_storage)
        self.storebtn.pack(pady=5)

    def spin(self):
        self.btn.config(state="disabled")
        self.bar["value"] = 0
        self.txt.config(text="Spinning...", bg="#fff3e0")
        self.spin_count += 1
        boost = self.get_luck_boost()
        self.luck_label.config(text=f"Luck Boost: {int(boost*100)}%")
        # Update total spins label
        self.spins_label.config(text=f"Total Spins: {self.spin_count}")
        for i in range(40):
            self.win.after(i * 50, self.update_bar)
        for i in range(20):
            self.win.after(i * 100, self.show_rand)
        self.win.after(2100, self.final_spin)

    def update_bar(self):
        self.bar.step(2.5)

    def show_rand(self):
        n = random.choice(self.names)
        c = self.colors[n]
        self.txt.config(text=n, bg=c)

    def final_spin(self):
        luck_boost = self.get_luck_boost()
        boosted_weights = []
        for n, c, w in items:
            if w <= 2 and luck_boost > 0:
                # Boost rare item chance
                boosted = w * (1 + luck_boost)
            else:
                boosted = w
            boosted_weights.append(boosted)
        pick = random.choices(self.names, weights=boosted_weights, k=1)[0]
        self.inv[pick] += 1
        self.txt.config(text=f"{pick}", bg=self.colors[pick])
        self.result.config(text="You got: " + pick)
        for n, c, w in items:
            if n == pick and w <= 2:
                stats.update_stats(rarest_item=pick)
                messagebox.showinfo("WOW!", "You got a super rare item: " + pick)
                #if user gets rare item with chance less than 2%, show message
        self.btn.config(state="normal")

    #storage window
    def show_storage(self):
        s = tk.Toplevel(self.win)
        s.title("Your Storage")
        s.geometry("320x545")
        s.config(bg="#f8f9fa")

        tk.Label(s, text="Your Items", bg="#f8f9fa", font=self.bigfont, fg="#1a237e").pack(pady=10)
        canvas = tk.Canvas(s, bg="#f8f9fa", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        y = 10
        for n in self.names:
            c = self.colors[n]
            canvas.create_rectangle(10, y, 30, y+20, fill=c, outline="")
            canvas.create_text(60, y+10, text=n, anchor="w", font=self.smallfont)
            canvas.create_text(260, y+10, text=str(self.inv[n]), anchor="e", font=self.smallfont)
            y += 25

        tk.Button(s, text="Close", bg="#f48fb1", fg="white", command=s.destroy).pack(pady=10)


root = tk.Tk()
app = SpinnerGame(root)
root.mainloop()