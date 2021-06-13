import sys, os    
from random import randint, choice
from tkinter import *
from tkinter import messagebox, simpledialog
from jamdict import Jamdict
import json
jam = Jamdict()
level = 1
highest_level = 1
root = Tk()
display_chr = None
raw_hiragana = open('/home/ben/Documents/python/kanji/RAWKANJI').read()
right = 0
wrong = 0
streak = 0
longest_streak = 0
game_info = Frame(root)
memos = {}
fullStudy = False
unforgiving = False
drop = 3
folder = os.path.dirname(os.path.realpath(__file__))
restart = [[0], [0]]
remember = False
startLevel = [False]

print('Kanji Meaning Helper run kanji.py -h for help')
i = 0
for arg in sys.argv:
    if arg == '-fs':
        fullStudy = True
    elif arg == '-u':
        unforgiving = True
    elif arg == '-d':
        drop = int(sys.argv[i+1])
    elif arg == '-sl':
        startLevel = [True, int(sys.argv[i+1])]
    elif arg == '-r':
        remember = True
    elif arg == '-h':
        print('Help:\n-fs: Full Study, will show characters in order\n-u: Unforgiving will go back to level 1 if you fail unless -r is on then you will go to 75% of the average of you last 10 scores on -u -r\n-r: remember scores and load average scores from last ten games with -r\n-d: Drop amount of levels to drop on fail does nothing on -u\n-sl: Start Level the level you start on\n-h: this message')
        exit()
    i += 1  

if unforgiving:
    drop = 0

def save():
    global memos, restart
    a = open(folder + '/data1.json', 'w')
    json.dump(memos, a)
    b = open(folder + '/data2.json', 'w')
    json.dump(restart, b)
    
def load():
    global memos, restart
    a = open(folder + '/data1.json')
    memos = json.load(a)
    b = open(folder + '/data2.json')
    restart = json.load(b)

load()

if not unforgiving and remember:
    try:
        level = int(sum(restart[0][-10:])/len(restart[0][-10:]))
    except:
        level = int(sum(restart[0])/len(restart[0]))
if unforgiving and remember:
    try:
        level = int(sum(restart[1][-10:])/len(restart[1][-10:])*0.75) + 1
    except:
        level = int(sum(restart[1])/len(restart[1])*0.75) + 1

if startLevel[0]:
    level = startLevel[1]

def update():
    global display_chr, raw_hiragana, display_chr_lbl, level, right, wrong, streak, longest_streak, info, game_input, answer, highest_level, grade_label, grade
    if level < len(raw_hiragana):
        display_chr = raw_hiragana[randint(0, level - 1)]
        if fullStudy:
            display_chr = raw_hiragana[level - 1]
    else:
        display_chr = raw_hiragana[randint(0, len(raw_hiragana) - 1)]
    display_chr_lbl.configure(text = display_chr)
    answer = repr(jam.lookup(display_chr).chars[0]).split(':')[2].split(',')[0]
    try:
        info.configure(text = f'Level: {level} ({highest_level})\nRight Wrong Ratio {right}:{wrong} ({str(right/(wrong + 1))[:5]})\nStreak: {streak}\nLongest Streak: {longest_streak}')
    except:
        info.configure(text = f'Level: {level} ({highest_level})\nRight Wrong Ratio {right}:{wrong} ({right})\nStreak: {streak}\nLongest Streak: {longest_streak}')
    game_input.delete(1.0, END)
    grade = 0
    level -= 1
    if level < 80:
        grade = level/80
    elif level < 240:
        grade = 1 + (level-80)/160
    elif level < 440:
        grade = 2 + (level-240)/200
    elif level < 640:
        grade = 3 + (level-440)/200
    elif level < 825:
        grade = 4 + (level-640)/185
    elif level < 1006:
        grade = 5 + (level-825)/181
    elif level < 1945:
        grade = 6 + (level-1006)/313
    else:
        grade = '9+'
    level += 1
    grade = '~' + str(grade)
    grade_label.configure(text = f'Grade: {grade}', font = ('Ubuntu',50))
    
def check():
    global display_chr, raw_hiragana, display_chr_lbl, level, right, wrong, streak, longest_streak, info, game_input, answer, highest_level, memo
    if game_input.get(1.0, END)[:-1] == answer:
        level += 1
        right += 1
        streak += 1
        if streak > longest_streak:
            longest_streak = streak
        if level > highest_level:
            highest_level = level
        if display_chr not in memos.keys():
            memo = simpledialog.askstring(title='Set Memo', prompt = f'Set memo for {display_chr} ({answer})')
            memos[display_chr] = memo
            save()
        update()
    elif len(game_input.get(1.0, END)[:-1]) == len(answer):
        wrong += 1
        if level > drop:
            if remember and not unforgiving:
                restart[0].append(level)
            level -= drop
            if unforgiving:
                if not remember:
                    level = 1
                if remember:
                    restart[1].append(level)
                    try:
                        level = int(sum(restart[1][-10:])/len(restart[1][-10:])*0.75)
                    except:
                        level = int(sum(restart[1])/len(restart[1])*0.75)
        save()
        streak = 0
        try:
            messagebox.showerror("Wrong", f"The Correct Answer Was: {answer}\nMemo:\n{memos[display_chr]}")
        except:
            messagebox.showerror("Wrong", f"The Correct Answer Was: {answer}\nMemo:\nNone Set!")
        if display_chr not in memos.keys():
            memo = simpledialog.askstring(title='Set Memo', prompt = f'Set memo for {display_chr} ({answer})')
            memos[display_chr] = memo
            save()
        update()
    root.after(100, check)

display_chr_lbl = Label(game_info, text = display_chr, font = ('Ubuntu',100))
display_chr_lbl.grid(row = 0, column = 0)
try:
    info = Label(game_info, text = f'Level: {level}\nRight Wrong Ratio {right}:{wrong} ({str(right/wrong)[:5]})\nStreak: {streak}\nLongest Streak: {longest_streak}', font = ('Ubuntu',20))
except:
    info = Label(game_info, text = f'Level: {level}\nRight Wrong Ratio {right}:{wrong} ({right})\nStreak: {streak}\nLongest Streak: {longest_streak}', font = ('Ubuntu',20))
grade_label = Label(root, text = f'forgiving mode is ungraded pass -u for unforgiving mode', font = ('Ubuntu',10))

game_input = Text(font = ('Ubuntu mono',100), width = 10, height = 1, fg = '#000066')
    
info.grid(row = 0, column = 1)
game_info.grid(row = 0, column = 0)
grade_label.grid(column = 1, row = 0)
game_input.grid(row = 1, column = 0)

update()
check()

root.mainloop()
