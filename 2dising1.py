import random as rnd
import math
import matplotlib.pyplot as plt
from matplotlib import animation

def setplot(sx1,sx2,sy1,sy2):
	ax=plt.gca()
	ax.set_aspect(1)
	plt.xlim([sx1,sx2])
	plt.ylim([sy1,sy2])
	ax.set_facecolor('xkcd:black')

def initspins(n):
	sp=[]
	for i in range(n):
		if rnd.random()>=0.5:
			sp.append(1)
		else:
			sp.append(-1)
	return sp

def nn(x,y):
	nnl=[]
	for i in range(x*y):
		tmp=[]
		for j in range(4):
			tmp.append(0)
		nnl.append(tmp)
	a=0
	b=x-1
	c=x*(y-1)
	d=x*y-1
	#corner a
	nnl[a][0]=c
	nnl[a][1]=b
	nnl[a][2]=1
	nnl[a][3]=x
	#corner b
	nnl[b][0]=d
	nnl[b][1]=b-1
	nnl[b][2]=a
	nnl[b][3]=b+x
	#corner c
	nnl[c][0]=c-x
	nnl[c][1]=d
	nnl[c][2]=c+1
	nnl[c][3]=a
	#corner d
	nnl[d][0]=d-x
	nnl[d][1]=d-1
	nnl[d][2]=c
	nnl[d][3]=b
	for i in range(1,x-1):
		ii=c+i
		#edge ab
		nnl[i][0]=ii
		nnl[i][1]=i-1
		nnl[i][2]=i+1
		nnl[i][3]=i+x
		#edge cd
		nnl[ii][0]=ii-x
		nnl[ii][1]=ii-1
		nnl[ii][2]=ii+1
		nnl[ii][3]=a+i
	for i in range(1,y-1):
		i1=a+i*x
		i2=b+i*x
		#edge ac
		nnl[i1][0]=i1-x
		nnl[i1][1]=i2
		nnl[i1][2]=i1+1
		nnl[i1][3]=i1+x
		#edge bd
		nnl[i2][0]=i2-x
		nnl[i2][1]=i2-1
		nnl[i2][2]=i1
		nnl[i2][3]=i2+x
	#bulk
	for i in range(1,y-1):
		for j in range(1,x-1):
			ii=i*x+j
			nnl[ii][0]=ii-x
			nnl[ii][1]=ii-1
			nnl[ii][2]=ii+1
			nnl[ii][3]=ii+x
	return nnl

def sumNN(i,sp,nl):
	sum=0
	for j in range(4):
		sum+=sp[nl[i][j]]
	return sum

#-----------------------------------------
nx=10
ny=10
J=1
kb=1
mo=1
T=5
B=0
N=nx*ny
nf=N
s=initspins(N)
nbrs=nn(nx,ny)

#ns=math.pow(2,N)
ns=1000*N
rkbt=1/(kb*T)
for j in range(int(ns)):
	i=int((N-1)*rnd.random())
	dE=2*s[i]*((J*sumNN(i,s,nbrs))+(B*mo))
	if dE<=0:
		s[i]=-s[i]
	else:
		if math.exp(-dE*rkbt)>=rnd.random():
			s[i]=-s[i]

fig, ax = plt.subplots()
dx=1/nx
dy=1/ny
if dx<=dy:
	r=dx/2
else:
	r=dy/2

def run(frame):
	i=int((N-1)*rnd.random())
	dE=2*s[i]*((J*sumNN(i,s,nbrs))+(B*mo))
	if dE<=0:
		s[i]=-s[i]
	else:
		if math.exp(-dE*rkbt)>=rnd.random():
			s[i]=-s[i]
	plt.clf()
	k=0
	for i in range(ny):
		y=(i+0.5)*dy
		for j in range(nx):
			x=(j+0.5)*dx
			if s[k]==1:		
				circle=plt.Circle((x,y),radius=r,fc='r')
			else:
				circle=plt.Circle((x,y),radius=r,fc='w')
			plt.gca().add_patch(circle)
			k+=1
	setplot(0,1,0,1)

ani=animation.FuncAnimation(fig,run,interval=nf)
plt.show()
