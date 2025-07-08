import tkinter as tk
import random
from tkinter import messagebox
from playsound import playsound
import threading

root = tk.Tk()
root.title("Memory Card Matching Game")
root.resizable(False, False)

buttons = []
first_card = None
second_card = None
flipped_indices = []

symbols = list('AABBCCDDEEFFGGHH')

moves = 0
moves_label = tk.Label(root, text="Moves: 0", font=("Arial", 12))
moves_label.grid(row=5, column=0, columnspan=4, pady=10)

# Function to play sound async (to avoid freezing UI)
def play_sound(path):
    threading.Thread(target=playsound, args=(path,), daemon=True).start()

def start_game():
    global symbols, moves, flipped_indices, first_card, second_card

    symbols = list('AABBCCDDEEFFGGHH')
    random.shuffle(symbols)
    moves = 0
    moves_label.config(text="Moves: 0")
    flipped_indices.clear()
    first_card = None
    second_card = None

    for btn in buttons:
        btn.config(text="", state="normal", bg="SystemButtonFace")

def on_card_click(i):
    global first_card, second_card, moves

    btn = buttons[i]
    if i in flipped_indices or btn['text'] != "":
        return

    # Play flip sound
    play_sound('flip.wav')

    # Animate flip (fake flip by quickly changing text)
    def animate_flip():
        btn.config(text="...", bg="lightyellow")
        root.after(150, lambda: btn.config(text=symbols[i]))

    animate_flip()
    btn.config(state="disabled")

    if first_card is None:
        first_card = i
    elif second_card is None:
        second_card = i
        moves += 1
        moves_label.config(text=f"Moves: {moves}")
        root.after(1000, check_match)

def check_match():
    global first_card, second_card
    if symbols[first_card] == symbols[second_card]:
        flipped_indices.extend([first_card, second_card])
        buttons[first_card].config(bg="lightgreen")
        buttons[second_card].config(bg="lightgreen")

        # Play match sound
        play_sound('match.wav')

        if len(flipped_indices) == len(symbols):
            messagebox.showinfo("You Win!", f"Congratulations! You won in {moves} moves.")
    else:
        buttons[first_card].config(text="", state="normal", bg="SystemButtonFace")
        buttons[second_card].config(text="", state="normal", bg="SystemButtonFace")

    first_card = None
    second_card = None

# Hover effect functions
def on_enter(e):
    btn = e.widget
    if btn['state'] == 'normal' and btn['text'] == "":
        btn.config(bg="lightblue")

def on_leave(e):
    btn = e.widget
    if btn['state'] == 'normal' and btn['text'] == "":
        btn.config(bg="SystemButtonFace")

for i in range(16):
    btn = tk.Button(root, text="", width=8, height=4,
                    font=("Arial", 14, "bold"),
                    command=lambda i=i: on_card_click(i))
    btn.grid(row=i//4, column=i%4, padx=5, pady=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    buttons.append(btn)

reset_btn = tk.Button(root, text="Reset Game", command=start_game, font=("Arial", 12))
reset_btn.grid(row=6, column=0, columnspan=4, pady=10)

start_game()
root.mainloop()
