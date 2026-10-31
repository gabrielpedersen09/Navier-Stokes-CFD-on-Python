import numpy as np
import matplotlib.pyplot as plt
nx=1000
nt=7200
dx=(2*np.pi)/(nx-1)
sigma=.2
nu=.05
dt=(dx**2*sigma)/(2*nu)
spi=5000
x=np.linspace(0,2*np.pi,nx)
u=np.cos(x)
line,=plt.plot(x,u)
for n in range (nt):
      un=u.copy()
      u[1:-1]=un[1:-1]-un[1:-1]*(dt/dx)*(un[1:-1]-un[0:-2])+((nu*dt)/(dx**2))*(un[2:]-2*un[1:-1]+un[0:-2])
      u[0]=u[1]
      u[-1]=u[-2]
      if n%spi==0:
            line.set_ydata(u)
            plt.pause(.00001)
plt.show()