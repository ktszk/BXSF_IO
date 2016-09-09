#!/usr/bin/env python
# -*- coding:utf-8 -*-
class Flag(object):
    def __init__(self,flag_char):
        self.flag=False
        self.flag_char=flag_char
    def flag_switch(self,fline):
        if fline.find('BEGIN_'+self.flag_char)!=-1:
            self.flag=True
        elif fline.find('END_'+self.flag_char)!=-1:
            self.flag=False
        else:
            pass

def read_bxsf(filename):
    try:
        f=open(filename,'r')
    except:
        print "Error: Cannot open file"
    else:
        f.close()
        import numpy as np
        count=0
        axis=[0.]*3
        info=Flag('INFO')
        block_bandgrid_3d=Flag('BLOCK_BANDGRID_3D')
        bandgrid_3d_fermi=Flag('BANDGRID_3D')
        for f in open(filename,'r'):
            info.flag_switch(f)
            block_bandgrid_3d.flag_switch(f)
            bandgrid_3d_fermi.flag_switch(f)
            if info.flag:
                tmp=f.split('#')[0]
                if tmp.find('Fermi Energy')!=-1:
                    EF=float(tmp.split(':')[1])
            if block_bandgrid_3d.flag:
                if (not bandgrid_3d_fermi.flag) and f.find('BANDGRID_3D')==-1:
                    index=f.strip()
            if bandgrid_3d_fermi.flag:
                if count==0:
                    pass
                elif count==1:
                    num_bands=int(f)
                    E_list=[[] for i in range(num_bands)]
                elif count==2:
                    tmp=f.split()
                    a,b,c=(int(t) for t in tmp)
                    sumk=a*b*c
                    k_list=np.array([[l%c,l%(c*b)//c ,l//(c*b)]
                                     for l in range(sumk)])
                elif count==3:
                    tmp=f.split()
                    center=[float(t) for t in tmp]
                elif 3<count<7:
                    tmp=f.split()
                    axis[count-4]=[float(t) for t in tmp]
                else:
                    if f.find('BAND:')!=-1:
                        tmp=f.split(':')
                        n_band=int(tmp[1])-1
                    else:
                        tmp=float(f)
                        E_list[n_band].append(tmp)
                count=count+1
        axis=np.array(axis)
        E_list=np.array(E_list)
        return(axis,E_list,index,EF,center,k_list)

class Bxsf_data():
    __slots__=['axis','E_list','index','EF','center','k_list']
    def __init__(self,axis=[0.]*3,elist=[],index='',ef=0.0,center=[0.,0.,0.],klist=[]):
        self.axis=axis
        self.E_list=elist
        self.index=index
        self.EF=ef
        self.center=center
        self.k_list=klist
    def read_bxsf(self,filename):
        try:
            (self.axis,self.E_list,self.index,
             self.EF,self.center,self.k_list)=read_bxsf(filename)
        except TypeError:
            pass
    def out_bxsf(self,filename):
        try:
            f=open(filename,'w')
        except:
            print 'Cannot open file'
        else:
            f.write('  BEGIN_INFO\n'
                    +'       Fermi Energy: %23.15E\n'%self.EF
                    +'  END_INFO\n\n')
            f.write('  BEGIN_BLOCK_BANDGRID_3D\n'
                    +'       %s\n'%self.index
                    +'  BEGIN_BANDGRID_3D_fermi\n'
                    +'         %d\n'%len(self.E_list)
                    +'         %d       %d       %d\n'%tuple( i+1 for i in self.k_list[-1])
                    +'    %16.14f  %16.14f  %16.14f\n'%tuple(self.center))
            for a in self.axis:
                f.write('    %16.14f  %16.14f  %16.14f\n'%tuple(a))
            for i,El in enumerate(self.E_list):
                f.write('    BAND: %9s%d\n'%('',i+1))
                for e in El:
                    f.write('      %15.8E\n'%e)
            f.write('  END_BANDGRID_3D\n'
                    +'  END_BLOCK_BANDGRID_3D\n')
            f.close()
