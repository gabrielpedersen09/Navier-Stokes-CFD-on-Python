import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
nx=150
ny=75
lx,ly=3,1
nt=1500
nit=300
spi=200
rho=1.225
nu=.005
dx=lx/(nx-1)
dy=ly/(ny-1)
dt=.0002
U=1.0
u=np.full((nx,ny),U)
v=np.zeros((nx,ny))
b=np.zeros((nx,ny))
p=np.zeros((nx,ny))
imagen=Image.open("/storage/emulated/0/Movies/naca.png").convert("L")
imagen=imagen.resize((nx,ny))
tunnel=np.array(imagen).T[:,::-1]<126
u[tunnel]=0
v[tunnel]=0
north=tunnel[1:-1,2:]
south=tunnel[1:-1,:-2]
east=tunnel[2:,1:-1]
west=tunnel[:-2,1:-1]
def b_source(tdudx,tdudy,tdvdx,tdvdy,rho,dt,b):
      b[1:-1,1:-1]=rho*(1/dt*(tdudx+tdvdy)-(tdudx**2)-2*(tdudy*tdvdx)-(tdvdy**2))
      return b
def pressure(p,dx,dy,b,nit):
      pn=np.ones((nx,ny))
      pn=p.copy()
      for n in range (nit):
            pn=p.copy()
            c=p[1:-1,1:-1]
            p_south=np.where(south,c,pn[1:-1,:-2])
            p_north=np.where(north,c,pn[1:-1,2:])
            p_west=np.where(west,c,pn[:-2,1:-1])
            p_east=np.where(east,c,pn[2:,1:-1])
            p[1:-1,1:-1]=(dy**2*(p_east+p_west)+dx**2*(p_south+p_north))/(2*(dx**2+dy**2))-(dx**2*dy**2)/(2*(dx**2+dy**2))*b[1:-1,1:-1]
            p[:,-1]=p[:,-2]
            p[:,0] = p[:,1]
            p[0,:]=p[1,:]
            p[-1,:]=0
      return p
def navier(u,v,rho,dt,dx,dy,nu,p,nt,U):
      un=np.empty_like(u)
      vn=np.empty_like(v)
      b=np.zeros((nx,ny))
      for n in range(nt):
            #first order
            tdudx=(u[2:,1:-1]-u[:-2,1:-1])/(2*dx)
            tdudy=(u[1:-1,2:]-u[1:-1,:-2])/(2*dy)
            tdvdx=(v[2:,1:-1]-v[:-2,1:-1])/(2*dx)
            tdvdy=(v[1:-1,2:]-v[1:-1,:-2])/(2*dy)
            dudx=(u[1:-1,1:-1]-u[:-2,1:-1])/(dx)
            dudy=(u[1:-1,1:-1]-u[1:-1,:-2])/(dy)
            dvdx=(v[1:-1,1:-1]-v[:-2,1:-1])/(dx)
            dvdy=(v[1:-1,1:-1]-v[1:-1,:-2])/(dy)
            #second order
            dududx=(u[2:,1:-1]-2*u[1:-1,1:-1]+u[:-2,1:-1])/(dx**2)
            dududy=(u[1:-1,2:]-2*u[1:-1,1:-1]+u[1:-1,:-2])/(dy**2)
            dvdvdx=(v[2:,1:-1]-2*v[1:-1,1:-1]+v[:-2,1:-1])/(dx**2)
            dvdvdy=(v[1:-1,2:]-2*v[1:-1,1:-1]+v[1:-1,:-2])/(dy**2)
            b=b_source(tdudx,tdudy,tdvdx,tdvdy,rho,dt,b)
            p=pressure(p,dx,dy,b,nit)
            un=u.copy()
            vn=v.copy()
            #x axis
            u[1:-1,1:-1]=un[1:-1,1:-1]-un[1:-1,1:-1]*dt*dudx-vn[1:-1,1:-1]*dt*dudy-(dt/(2*rho*dx))*(p[2:,1:-1]-p[:-2,1:-1])+nu*dt*(dududx+dududy)
            v[1:-1,1:-1]=vn[1:-1,1:-1]-un[1:-1,1:-1]*dt*dvdx-vn[1:-1,1:-1]*dt*dvdy-(dt/(2*rho*dy))*(p[1:-1,2:]-p[1:-1,:-2])+nu*dt*(dvdvdx+dvdvdy)
            u[0,:]=U
            v[0,:]=0
            v[:,0]=0
            v[:,-1]=0
            u[-1,:]=u[-2,:]
            v[-1,:]=v[-2,:]
            u[:,0]=u[:,1]
            u[:,-1]=u[:,-2]
            u[tunnel]=0
            v[tunnel]=0
            if n%spi==0:
                  step=4
                  av=min(2+step*n,nx)
                  ax.clear()
                  ax.set_aspect('equal')
                  ax.contourf(x,y,p,cmap='viridis')
                  ax.contourf(x,y,tunnel.astype(float),levels=[.5,1.5],colors='k')
                  #ax.quiver(x[:av:4,::4],y[:av:4,::4],u[:av:4,::4],v[:av:4,::4],np.sqrt(u**2+v**2)[:av:4,::4],scale_units='xy',scale=25,width=.003)
                  ax.set_title(f'N:{n}')
                  plt.pause(.05)
        
      return u,v,p
x=np.linspace(0,lx,nx)
y=np.linspace(0,ly,ny)
x,y=np.meshgrid(x,y,indexing='ij')
plt.ion()
fig,ax=plt.subplots(figsize=(11,7),dpi=100)
u,v,p=navier(u,v,rho,dt,dx,dy,nu,p,nt,U)
plt.ioff()
plt.show()