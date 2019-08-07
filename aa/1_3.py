# -*- coding: utf-8 -*-
"""1_3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1y5Umybp0Z00m7eb91SxezlRrqhLuRDau
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
x = [[0],[0],[1],[1],[0]]
a =np.array(x)
y = [[0],[1],[1],[0],[0]]
b =np.array(y)
X=tf.constant(a.astype(np.float32))
Y=tf.constant(b.astype(np.float32))
sess = tf.InteractiveSession()
tf.global_variables_initializer().run()



#center_x,y are 2 list
def test(center_x,center_y,length):
  x=[]
  y=[]
  xc=[]
  yc=[]
  for i in range(len(center_x)):
    #Determine the 4 corners of the square
    #x-b,y-b
    a1=center_x[i]-length/2
    b1=center_y[i]-length/2
    #x-b,y+b
    a2=center_x[i]-length/2
    b2=center_y[i]+length/2
    #x+b,y+b
    a3=center_x[i]+length/2
    b3=center_y[i]+length/2
    #x+b,y-b
    a4=center_x[i]+length/2
    b4=center_y[i]-length/2
    #
    x.extend([a1,a2,a3,a4,a1])
    y.extend([b1,b2,b3,b4,b1])
    xc.extend([a1,a2,a3,a4])
    yc.extend([b1,b2,b3,b4])
    #update centers
  #remove old center(S)
  #update length
  length = length/2
  center_x = xc
  center_y = yc
  return x,y,length,center_x,center_y



c = test([0],[0],2)[0]
d = test([0],[0],2)[1]

n=3  #set the time of recurved 
def main(center_x,center_y,length,level=n):
  '''
  Center_x : the x point of initial center of square 
  Center_y : the y point of initial center of square 
  length (): the number of each 
  level : the time need to recurve
  '''
  if level ==0:
    a=test(center_x,center_y,length)[0]
    b=test(center_x,center_y,length)[1]
  else:
    A=test(center_x,center_y,length)
    a=test(center_x,center_y,length)[0]
    a.extend(main(A[3],A[4],A[2],level-1)[0])
    b =test(center_x,center_y,length)[1]
    b.extend(main(A[3],A[4],A[2],level-1)[1])
  return a,b

f=main([0],[0],2)[0]
l=main([0],[0],2)[1]

# Click on the points you get 5 points
step=5
n= [f[i:i+step] for i in range(0,len(f),step)]
m= [l[i:i+step] for i in range(0,len(l),step)]

#Transforme the nm in to tensor 
n1 = np.array(n)
m1=np.array(m)
X=tf.constant(n1.astype(np.float32))
Y=tf.constant(m1.astype(np.float32))

for i in range(len(n)):
   plt.title("T-square")
   plt.plot(X[i].eval(),Y[i].eval(),'b')

print(X, Y)