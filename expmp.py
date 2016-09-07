#!/usr/bin/env python
import numpy as np
from math import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import Rectangle
from matplotlib.patches import PathPatch

matplotlib.rcParams.update({'font.size': 22})

plt.figure(figsize=(10,10))
ax=plt.axes()
plt.axis('off')
#axes
plt.arrow(-2, 0.0 , +4,  0.0, head_width=0.15, head_length=0.1, fc='k', ec='k')
plt.arrow(+2, 0.0 , -4,  0.0, head_width=0.1, head_length=0.1, fc='k', ec='k')
plt.arrow(0, -2 , 0, +4.0, head_width=0.1, head_length=0.1, fc='k', ec='k')
plt.arrow(0, +2 , 0, -4.0, head_width=0.1, head_length=0.1, fc='k', ec='k')
plt.text(1.75,0,"$k_\perp$",verticalalignment='bottom')
plt.text(0,1.75,"$\,k_\parallel$",horizontalalignment='left')
plt.xlim(-2.45,2.8)
plt.ylim(-2.2,2.5)

lhandles=[]
def GenWedge(ofs,rx,ry, facecolor='r',label='',alpha=0.3):
    codes,verts=[],[]
    amin=0
    ox,oy=ofs
    if ox==0 and oy==0:
        amax=np.pi*2
        ngoes=1
    elif ox==0:
        amax=np.pi
        ngoes=2
    else:
        amax=np.pi/2
        ngoes=4
        
    phi=np.linspace(amin,amax,100)
    
    for g in range(ngoes):
        if g==0:
            cofs=ofs
        elif g==1:
            if (ngoes==2):
                cofs=[0,-ofs[1]]
            else:
                cofs=[-ofs[0],ofs[1]]
        elif g==2:
                cofs=[-ofs[0],-ofs[1]]
        elif g==3:
                cofs=[ofs[0],-ofs[1]]

        codes.append(Path.MOVETO)
        if ngoes>1:
            verts.append(cofs)
        else:
            verts.append([cofs[0]+rx,cofs[1]])

        for p in phi:
            if p==0:
                codes.append(Path.LINETO)
            else:
                #print dir(Path)
                codes.append(Path.CURVE4)
            verts.append([cofs[0]+rx*cos(p+2*np.pi/ngoes*g),cofs[1]+ry*sin(p+2*np.pi/ngoes*g)])
        if (ngoes>1):
            codes.append(Path.CLOSEPOLY)
            verts.append(ofs)


        
    w=PathPatch(Path(verts,codes),label=label)
    w.set_alpha(alpha)
    w.set_facecolor(facecolor)
    w.set_linewidth(0.0)
    lhandles.append(w)
    return w


#galaxies
w=GenWedge([0,0],1.5,1.5,'y','redshift survey (optical/\nresolved 21-cm)')
ax.add_artist(w)
#21cm
ax.add_artist(GenWedge([0.1,0.1],0.9,1.9,'g','21-cm intensity \n mapping'))
for sign in [+1,-1]:
    w=Rectangle([-0.1,0.1*sign],0.2,1.9*sign,label='21-cm in single dish\n mode')
    w.set_hatch('/')
    w.set_fill(False)
    w.set_color('g')
    ax.add_artist(w)
lhandles.append(w)
h,=plt.plot([0.1,1.1],[0.1,0.5],'g:',label='21-cm wedge')
plt.plot([0.1,1.1],[-0.1,-0.5],'g:')
plt.plot([-0.1,-1.1],[-0.1,-0.5],'g:')
plt.plot([-0.1,-1.1],[0.1,0.5],'g:')
lhandles.append(h)

#Lya forest
wlya=GenWedge([0.0,0.2],1.8,1.8,'k','Lyman-$\\alpha$ forest',0.1)

ax.add_artist(wlya)


#PZ
ax.add_artist(GenWedge([0,0],1.5,0.25,'m','photo-z survey'))
w=GenWedge([0,0],1.5,0.5,'m','low-res survey')
w.set_color('m')
w.set_fill(False)
w.set_linestyle('--')
w.set_linewidth(3)
ax.add_artist(w)

#WL
ax.add_artist(GenWedge([0.0,0.0],2.5,0.03,'c','weak lensing (gals/CMB)'))

plt.legend(handles=lhandles,fontsize=12)
plt.savefig("expplot.pdf", bbox_inches='tight')
plt.savefig("expplot.png", bbox_inches='tight')
