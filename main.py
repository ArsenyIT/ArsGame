from tkinter import*

w = Tk()
w.title('')
canv = Canvas(w, width = 1366, height = 768)
canv.pack()
Widht = 10Height = 10
    player_size = 10
SPEED = 20
player1_id = nv.create_rectangle(Widht, Height, Widht + player_size, Height + player_size)
    KEY_W = 87
KEY_S = 83
KEY_A = 65
KEY_D = 68

we = 10

def key_press(event, we):
#    if event.keycode == KEY_W:
#        player.forvard()
#    elif event.keycode == KEY_S:
#        player.backward()
#    elif event.keycode == KEY_A:
#        player.left()
    if event.keycode == KEY_D:
        canvas.move(player1_id, SPEED, 0)

w.bind('<KeyPress>', key_press)

w.mainloop()