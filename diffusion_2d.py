import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import cm
nx=100
ny=100
nt=8000
dx=(2)/(nx-1)
dy=(2)/(ny-1)
nu=.05
sigma=.15
spi=30
dt=sigma*dx**2/nu
x=np.linspace(0,2,nx)
y=np.linspace(0,2,ny)
x,y=np.meshgrid(x,y,indexing='ij')
fig,ax=plt.subplots(figsize=(7,6))
sm=cm.ScalarMappable(norm=Normalize(vmin=1,vmax=2),cmap='viridis')
cbar=fig.colorbar(sm,ax=ax,shrink=.3,pad=.1)
ux=np.ones((nx,ny))
ux[int(.5/dx):int(1/dx+1),int(.5/dy):int(1/dy+1)]=2
line=plt.imshow(ux,cmap='viridis',origin='lower',vmin=1,vmax=2)
for n in range (nt):
      un=ux.copy()
      ux[1:-1,1:-1]=un[1:-1,1:-1]+(nu*dt/dx**2)*(un[2:,1:-1]-2*un[1:-1,1:-1]+un[:-2,1:-1])+(nu*dt/dy**2)*(un[1:-1,2:]-2*un[1:-1,1:-1]+un[1:-1,:-2])
      ux[0,:]=1
      ux[-1,:]=1
      ux[:,-1]=1
      ux[:,0]=1
      if n%spi==0:
            line.set_data(ux)
            ax.set_title(f'N:{n}')
            plt.pause(.01)
plt.show()