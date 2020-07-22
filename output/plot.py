## Copyright 2020 Martin J. Steil
##
## Permission is hereby granted, free of charge, to any person obtaining
## a copy of this software and associated documentation files (the "Software"),
## to deal in the Software without restriction, including without limitation
## the rights to use, copy, modify, merge, publish, distribute, sublicense,
## and/or sell copies of the Software, and to permit persons to whom the
## Software is furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included
## in all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
## OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.

import glob
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import gridspec
from pylab import rcParams

plt.style.use('classic')     
rcParams['figure.figsize'] = 12, 6.5
rcParams['legend.fontsize'] = 14
rcParams['font.family'] = 'sans-serif'
rcParams['mathtext.fontset'] = 'dejavusans'


#plt.style.use('classic')
colors = ['r','g','b']

# Load data from CSV
for file_name in glob.glob('*.csv'):
	
	fig = plt.figure(figsize=(8, 10)) 
	gs = gridspec.GridSpec(3, 1) #, width_ratios=[1, 1.25]

	name=np.genfromtxt(file_name,delimiter='\t',skip_header=0,max_rows=1,comments=[],dtype="|U")[1]
	print('Plotting {:s} ...'.format(name))
	discretization=np.genfromtxt(file_name,delimiter='\t',skip_header=1,max_rows=1,comments=[])[1]
	
	x0x1=np.genfromtxt(file_name,delimiter='\t',skip_header=2,max_rows=1,comments=[])[1:]
	xi=np.genfromtxt(file_name,delimiter='\t',skip_header=3,max_rows=1,comments=[])[1]
	xRef=[x0x1[0],xi,xi,x0x1[1]]
	
	gamma=np.genfromtxt(file_name,delimiter='\t',skip_header=4,max_rows=1,comments=[])[1]
	uL=np.genfromtxt(file_name,delimiter='\t',skip_header=5,max_rows=1,comments=[])[1:]
	uR=np.genfromtxt(file_name,delimiter='\t',skip_header=6,max_rows=1,comments=[])[1:]
	t1=np.genfromtxt(file_name,delimiter='\t',skip_header=7,max_rows=1,comments=[])[1]
	
	# Convert inital condition [\rho,v,p] to [\rho,\mu,\epsilon]
	uL[1]=uL[0]*uL[1]
	uL[2]=uL[2]/(gamma-1.0)+0.5*uL[1]*uL[1]/uL[0]
	
	uR[1]=uR[0]*uR[1]
	uR[2]=uR[2]/(gamma-1.0)+0.5*uR[1]*uR[1]/uR[0]
	
	rhoRef=[uL[0],uL[0],uR[0],uR[0]]
	muRef=[uL[1],uL[1],uR[1],uR[1]]
	epsilonRef=[uL[2],uL[2],uR[2],uR[2]]
	
	data = np.genfromtxt(file_name,delimiter='\t',skip_header=9)
	
	ax0 = plt.subplot(gs[0])
	
	plt.title(('{:s} shock tube problem, $\gamma='.format(name))+'{:<.1f}'.format(gamma)+'$')
	
	ax0.margins(0.01,0.05)
	plt.grid(True)
	plt.ylabel("$\\rho\,[(\mathrm{kg})/\mathrm{m}^{3}]$")
	ax0.plot(xRef,rhoRef,color=colors[0],linewidth=1.5,linestyle='--')
	ax0.plot(data[:,0],data[:,1],color=colors[0],linewidth=1.5,linestyle='-')
	
	ax0.plot([],[],color='0',linewidth=1.5,linestyle='--',label='$t='+'{:<.3f}'.format(0)+'\mathrm{s}$')
	ax0.plot([],[],color='0',linewidth=1.5,linestyle='-',label='$t='+'{:<.3f}'.format(t1)+'\mathrm{s}$')
	plt.legend(numpoints=3,loc=1)
	
	ax1 = plt.subplot(gs[1])
	ax1.margins(0.01,0.05)
	plt.grid(True)
	plt.ylabel("$\mu\,[(\mathrm{kg}\mathrm{m}\mathrm{s}^{-1})/\mathrm{m}^{3}]$")
	ax1.plot(data[:,0],data[:,2],color=colors[1],linewidth=1.5,linestyle='-')
	ax1.plot(xRef,muRef,color=colors[1],linewidth=1.5,linestyle='--')
	
	ax2 = plt.subplot(gs[2])
	ax2.margins(0.01,0.05)
	plt.grid(True)
	plt.xlabel("$x\,[\mathrm{m}]$")
	plt.ylabel("$\epsilon\,[(\mathrm{kg}\mathrm{m}^2\mathrm{s}^{-2})/\mathrm{m}^{3}]$")
	ax2.plot(data[:,0],data[:,3],color=colors[2],linewidth=1.5,linestyle='-')
	ax2.plot(xRef,epsilonRef,color=colors[2],linewidth=1.5,linestyle='--')
	
	plt.tight_layout()
	plt.subplots_adjust(wspace=0.2)
	plt.savefig('{:s}_t{:.5e}_exact.pdf'.format(name,t1), bbox_inches='tight', pad_inches=0.1, dpi=600,facecolor='w', edgecolor='w')
	plt.savefig('{:s}_t{:.5e}_exact.png'.format(name,t1), bbox_inches='tight', pad_inches=0.1, dpi=75,facecolor='w', edgecolor='w')


