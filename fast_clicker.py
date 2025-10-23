import tkinter as tk
from tkinter import messagebox

class FastClickerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Fast Clicker Game")
        self.root.geometry("600x500")
        
        # Set color scheme
        self.bg_color = "#E8F5E9"  # Light mint green
        self.button_color = "#81C784"  # Soft green
        self.click_button_color = "#FF80AB"  # Soft pink
        self.text_color = "#2E7D32"  # Dark green
        self.highlight_color = "#4CAF50"  # Vibrant green
        
        self.root.configure(bg=self.bg_color)

        # Game variables
        self.click_count = 0
        self.high_scores = {5: 0, 10: 0, 20: 0}  # Separate high scores for each time limit
        self.time_left = 0
        self.game_running = False
        self.timer_id = None
        self.current_time_limit = None

        # Create welcome label with shadow effect
        self.welcome_frame = tk.Frame(root, bg=self.bg_color)
        self.welcome_frame.pack(pady=20)

        self.welcome_shadow = tk.Label(
            self.welcome_frame,
            text="Welcome to Fast Clicker!",
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg="#CCCCCC"
        )
        self.welcome_shadow.pack()

        self.welcome_label = tk.Label(
            self.welcome_frame,
            text="Welcome to Fast Clicker!",
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.welcome_label.place(in_=self.welcome_shadow, x=-2, y=-2)

        # Create time selection buttons
        self.time_frame = tk.Frame(root, bg=self.bg_color)
        self.time_frame.pack(pady=10)

        tk.Label(
            self.time_frame,
            text="Select Time Limit:",
            font=("Helvetica", 14),
            bg=self.bg_color,
            fg=self.text_color
        ).pack()

        times = [5, 10, 20]
        for t in times:
            btn = tk.Button(
                self.time_frame,
                text=f"{t} seconds",
                command=lambda time=t: self.start_game(time),
                font=("Helvetica", 12),
                bg=self.button_color,
                fg="white",
                width=10,
                relief="flat",
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=10)
            # Add hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.highlight_color))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.button_color))

        # Create score display frame
        self.score_frame = tk.Frame(root, bg=self.bg_color)
        self.score_frame.pack(pady=15)

        # Current score
        self.score_label = tk.Label(
            self.score_frame,
            text="Score: 0",
            font=("Helvetica", 14, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.score_label.pack(pady=5)

        # High scores frame
        self.high_scores_frame = tk.Frame(root, bg=self.bg_color)
        self.high_scores_frame.pack(pady=5)

        # Create labels for each time limit's high score
        self.high_score_labels = {}
        for time in times:
            self.high_score_labels[time] = tk.Label(
                self.high_scores_frame,
                text=f"{time}s Best: 0",
                font=("Helvetica", 12),
                bg=self.bg_color,
                fg=self.text_color
            )
            self.high_score_labels[time].pack()

        # Timer display
        self.timer_label = tk.Label(
            root,
            text="Time: 0",
            font=("Helvetica", 16, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.timer_label.pack(pady=10)

        # Create clickable sprite button with modern styling
        self.click_button = tk.Button(
            root,
            text="Click Me!",
            command=self.increment_score,
            font=("Helvetica", 18, "bold"),
            bg=self.click_button_color,
            fg="white",
            width=15,
            height=2,
            relief="flat",
            cursor="hand2",
            state="disabled"
        )
        self.click_button.pack(pady=20)
        
        # Add hover effect to click button
        self.click_button.bind("<Enter>", lambda e: self.click_button.configure(bg="#FF4081") if self.game_running else None)
        self.click_button.bind("<Leave>", lambda e: self.click_button.configure(bg=self.click_button_color) if self.game_running else None)

    def start_game(self, seconds):
        # Reset game state
        self.click_count = 0
        self.time_left = seconds
        self.current_time_limit = seconds
        self.game_running = True
        self.score_label.config(text="Score: 0")
        self.timer_label.config(text=f"Time: {self.time_left}")
        self.click_button.config(state="normal")
        
        # Start the timer
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time: {self.time_left}")
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.end_game()

    def increment_score(self):
        if self.game_running:
            self.click_count += 1
            self.score_label.config(text=f"Score: {self.click_count}")

    def end_game(self):
        self.game_running = False
        self.click_button.config(state="disabled")
        
        # Update high score if needed
        if self.click_count > self.high_scores[self.current_time_limit]:
            self.high_scores[self.current_time_limit] = self.click_count
            self.high_score_labels[self.current_time_limit].config(
                text=f"{self.current_time_limit}s Best: {self.click_count}"
            )
            message = f"New High Score for {self.current_time_limit}s! 🎉\nYou clicked {self.click_count} times!"
        else:
            message = f"Game Over!\nYou clicked {self.click_count} times!"
        
        messagebox.showinfo("Game Over", message)

# Create and run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = FastClickerGame(root)
    root.mainloop()
