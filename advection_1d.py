import numpy as np
import matplotlib.pyplot as plt
nx=1000
dx=2/(nx-1)
sigma=.5
dt=sigma*dx
c=1
nt=800
u=np.ones(nx)
u[int(.5/dx):int(1/dx+1)]=2
print(u)
un=np.ones(nx)
spi=20
line,=plt.plot(np.linspace(0,2,nx),u);
for n in range(nt):
      un=u.copy()
      u[1:]=un[1:]-(dt/(2*dx))*(un[1:]**2-un[:-1]**2)
      if n%spi==0:
            line.set_ydata(u)
            plt.pause(0.01)
plt.show()