from tkinter import*
import math

root=Tk()
root.geometry('600x600')
w=Canvas(root,height=600,width=600)
w.pack()
w0=300
h0=300
w.create_line(0,300,600,300,fill="red",arrow=LAST)
w.create_line(300,600,300,0,fill="red",arrow=LAST)

for i in range(-5,5):
    j=i*40
    w.create_line(j+w0,h0,j+w0,h0-5,fill="red")
    w.create_text(j+w0,h0+5,text=str(i))
    
for i in range(-5,5):
    j=i*40
    w.create_line(w0,j+h0,w0+5,j+h0,fill="red")
    w.create_text(w0-10,j+h0,text=str(-i))

def x(t):
    
    x = math.cos(t)*160-math.cos(2*t)*80
    x = t*40
    x+=w0
    return x

def y(t):
    
    y = math.sin(t)*160-math.sin(2*t)*80
    y-=h0
    y=-y
    return y    


t = -math.pi

while(t<math.pi):
    w.create_line(x(t),y(t),x(t+0.01),y(t+0.01),fill="blue")
    t+=0.01
    
root.mainloop()







