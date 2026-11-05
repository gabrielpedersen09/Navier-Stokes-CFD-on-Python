import numpy as np
import matplotlib.pyplot as plt
nx=200
ny=200
nt=3000
c=1
spi=15
dx=(2*np.pi)/(nx-1)
dy=(2*np.pi)/(ny-1)
sigma=.09
dt=sigma*dx
x=np.linspace(0,2*np.pi,nx,endpoint=False)
y=np.linspace(0,2*np.pi,ny,endpoint=False)
x,y=np.meshgrid(x,y,indexing='ij')
u=np.cos(x)*np.cos(y)
fig,ax=plt.subplots(figsize=(7,6))
line =plt.imshow(u,cmap='viridis',vmin=-1,vmax=1)
cbar=fig.colorbar(line,ax=ax,shrink=.4,pad=.1)
for n in range(nt):
      un=u.copy()
      u[1:,1:]=un[1:,1:]-(c*dt/dx)*(un[1:,1:]-un[:-1,1:])-(c*dt/dy)*(un[1:,1:]-un[1:,:-1])
      u=(un-(c*dt/dx)*(un-np.roll(un,1,axis=0))-(c*dt/dy)*(un-np.roll(un,1,axis=1)))
      if n%spi==0:
            line.set_data(u)
            ax.set_title(f'N:{n}',fontfamily='serif',fontstyle='italic')
            plt.pause(.001)
plt.show()