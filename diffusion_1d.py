import numpy as np
import matplotlib.pyplot as plt
nx=100
nt=3200
dx=2/(nx-1)
nu=.3
sigma=.5
dt=(sigma*dx**2)/nu
u=np.ones(nx)
u[int(.5/dx):int(1/dx+1)]=2
print(u)
spi=100
un=np.ones(nx)
line,= plt.plot(np.linspace(0,2,nx),u)
for n in range(nt):
      un=u.copy()
      u[1:-1]=un[1:-1]+((nu*dt)/(dx**2))*(un[2:]-2*un[1:-1]+un[:-2])
      if n%spi==0:   
            line.set_ydata(u)
            plt.pause(.0001)
plt.show()