import tkinter as tk
from PIL import Image

root = tk.Tk()
# root.geometry("+{}+{}".format(positionRight, positionDown))
root.geometry("400x450")
root.configure(bg="black")
# file = '../assets/sound.gif'
file = "sound 1.gif"
count = 0
info = Image.open(file)
frame = info.n_frames
print(frame)
img = [tk.PhotoImage(file=file, format=f'gif -index {i}') for i in range(frame)]
# tk.PhotoImage(file=file, format=f'gif -index{0}')
anim = None

count = 0
def animation(count):
    global anim
    img2 = img[count]
    gif_label.configure(image=img2)
    count += 1
    if count == frame:
        count = 0

    anim = root.after(50, lambda: animation(count))


def stop_animation():
    global anim
    root.after_cancel(anim)


gif_label = tk.Label(image="")
gif_label.pack()

start = tk.Button(text='Start', command=lambda: animation(count), height=3, width=10)
start.place(x=90, y=280)
stop = tk.Button(text='Stop', command=stop_animation, height=3, width=10)
stop.place(x=210, y=280)
root.mainloop()
