from tkinter import*

w = Tk()
w.title('')
canv = Canvas(w, width= 1370, height = 770)
canv.pack()

x = 50
y = 50
player_size = 100
SPEED = 20

player1_id = canv.create_rectangle(x, y, x + player_size, y + player_size)

KEY_W = 87
KEY_S = 83
KEY_A = 65
KEY_D = 68

def key_press(event):
    if event.keycode == KEY_W:
        canv.move(player1_id, 0, -SPEED)
    elif event.keycode == KEY_S:
        canv.move(player1_id, 0, SPEED)
    elif event.keycode == KEY_A:
        canv.move(player1_id, -SPEED, 0)
    if event.keycode == KEY_D:
        canv.move(player1_id, SPEED, 0)

w.bind('<KeyPress>', key_press)

w.mainloop()