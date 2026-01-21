import csv
import random
import tkinter as tk
from tkinter import ttk

CSV_PATH = "questions.csv"
TOTAL_QUESTIONS = 8
START_POT = 50000

# ---------------- DATA ----------------
def load_questions(path):
    qs = []
    with open(path, encoding="utf-8") as f:
        r = csv.reader(f, delimiter=";")
        for row in r:
            qs.append({
                "q": row[2],
                "answers": row[3:7],
                "correct": row[3]  # 1re réponse = bonne
            })
    random.shuffle(qs)
    return qs[:TOTAL_QUESTIONS]

questions = load_questions(CSV_PATH)
q_index = 0
pot = START_POT

# ---------------- UI ----------------
root = tk.Tk()
root.title("PYTHON DROP")
root.geometry("1280x720")
root.configure(bg="#1b1b1b")

FONT_TITLE = ("Segoe UI Black", 36)
FONT_Q = ("Segoe UI", 20, "bold")
FONT_A = ("Segoe UI", 14, "bold")

title = tk.Label(root, text="PYTHON DROP", fg="white", bg="#1b1b1b", font=FONT_TITLE)
title.pack(pady=30)

question_var = tk.StringVar()
question_lbl = tk.Label(
    root, textvariable=question_var,
    fg="white", bg="#1b1b1b",
    font=FONT_Q, wraplength=1000, justify="center"
)
question_lbl.pack(pady=20)

answers_frame = tk.Frame(root, bg="#1b1b1b")
answers_frame.pack(pady=40)

entries = []
labels = []

def make_answer(col, letter):
    f = tk.Frame(answers_frame, bg="#1b1b1b")
    f.grid(row=0, column=col, padx=25)

    lbl = tk.Label(f, text="", fg="white", bg="#1b1b1b", font=FONT_A, wraplength=220)
    lbl.pack(pady=10)

    e = tk.Entry(f, font=("Segoe UI", 14), justify="center", width=10)
    e.insert(0, "0")
    e.pack()

    labels.append(lbl)
    entries.append(e)

for i, l in enumerate(["A", "B", "C", "D"]):
    make_answer(i, l)

# ---------------- GAME LOGIC ----------------
def show_question():
    global q_index
    q = questions[q_index]
    question_var.set(q["q"])
    for i in range(4):
        labels[i].config(text=f"{chr(65+i)} - {q['answers'][i]}")
        entries[i].delete(0, tk.END)
        entries[i].insert(0, "0")

def validate():
    global pot
    q = questions[q_index]
    correct_idx = q["answers"].index(q["correct"])

    bets = []
    for e in entries:
        try:
            bets.append(int(e.get()))
        except:
            bets.append(0)

    total_bet = sum(bets)
    if total_bet > pot:
        return

    pot = bets[correct_idx]
    pot_var.set(f"CAGNOTTE : {pot} €")

def next_question():
    global q_index
    if pot <= 0:
        question_var.set("PERDU")
        return
    q_index += 1
    if q_index >= len(questions):
        question_var.set(f"FIN — GAIN : {pot} €")
        return
    show_question()

# ---------------- CONTROLS ----------------
validate_btn = tk.Button(
    root, text="VALIDER",
    font=("Segoe UI Black", 20),
    bg="#2b2b2b", fg="white",
    relief="flat", padx=40, pady=15,
    command=validate
)
validate_btn.pack(pady=20)

next_btn = tk.Button(
    root, text="QUESTION SUIVANTE",
    font=("Segoe UI", 14),
    command=next_question
)
next_btn.pack()

pot_var = tk.StringVar(value=f"CAGNOTTE : {pot} €")
pot_lbl = tk.Label(
    root, textvariable=pot_var,
    fg="white", bg="#1b1b1b",
    font=("Segoe UI", 14, "bold")
)
pot_lbl.place(x=20, y=680)

# ---------------- START ----------------
show_question()
root.mainloop()
