import tkinter as tk
from tkinter import Frame, Label, Button
from number_entry import IntEntry
import random

def main():
    root = tk.Tk()
    root.option_add('Font', 'Helvetica 16')
    frm_main = Frame(root)
    frm_main.master.title('Dice')
    frm_main.pack(padx=3, pady=3, fill=tk.BOTH, expand=True)
    setup_main(frm_main)

    frm_main.mainloop()

def setup_main(frm):
    lbl_sides = Label(frm, text= 'Enter the number of sides of the dices (2-20)')
    lbl_sides.grid(row=0,column=0, padx=3, pady=3)
    ent_sides = IntEntry(frm, width=2, lower_bound=2, upper_bound=20)
    ent_sides.grid(row=0, column=1, padx=3, pady=3)

    lbl_count = Label(frm, text= 'Enter the number of dice to roll (1-10)')
    lbl_count.grid(row=1,column=0, padx=3, pady=3)
    ent_count = IntEntry(frm, width=2, lower_bound=1, upper_bound=10)
    ent_count.grid(row=1, column=1, padx=3, pady=3)

    btn_roll = Button(frm, text='Roll')
    btn_roll.grid(row=2, column=0, padx=3, pady=3)

    lbl_roll = Label(frm, text='')
    lbl_roll.grid(row=3, column=0, padx=3, pady=3)

    def roll_dice(sides, count):
        sum=0
        roll_text =''
        for row in range(count):
            die_roll=random.randint(1,sides)
            sum+=die_roll
            roll_text += f'{die_roll} '
        roll_text += f'Total: {sum}'
        return roll_text

    def roll_action():
        try:
            sides=ent_sides.get()
        except ValueError:
            lbl_roll.config(text='You must enter a valid number of sides')
            return
        try:
            count=ent_count.get()
        except ValueError:
            lbl_roll.config(text='You must enter a valid number of dice')
            return

        lbltext = roll_dice(sides, count)
        lbl_roll.config(text=lbltext)
        
    btn_roll.config(command=roll_action)


if __name__ == '__main__':
    main()