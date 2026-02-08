from tkinter import*

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
        canv.create_rectangle(we + 10, 10, 20, 20)

w = Tk()
w.title('')
canv = Canvas(w, width = 1366, height = 768)
canv.pack()
canv.create_rectangle(10, 10, 20, 20)

w.bind('<KeyPress>', key_press)

w.mainloop()