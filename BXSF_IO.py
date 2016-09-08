#!/usr/bin/env python
# -*- coding:utf-8
class BXSF_IO(object):
    def __init__(self):
        self.axis=[[]]*3
        self.E_list=[]
        self.EF=0
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
    def read_bxsf(self,filename):
        import numpy as np
        count=0
        info=self.Flag('INFO')
        block_bandgrid_3d=self.Flag('BLOCK_BANDGRID_3D')
        bandgrid_3d_fermi=self.Flag('BANDGRID_3D')
        for f in open(filename,'r'):
            info.flag_switch(f)
            block_bandgrid_3d.flag_switch(f)
            bandgrid_3d_fermi.flag_switch(f)
            if info.flag:
                tmp=f.split('#')[0]
                if tmp.find('Fermi Energy')!=-1:
                    self.EF=float(tmp.split(':')[1])
            if block_bandgrid_3d.flag:
                pass
            if bandgrid_3d_fermi.flag:
                if count==0:
                    pass
                elif count==1:
                    num_bands=int(f)
                    self.E_list=[[]]*num_bands
                elif count==2:
                    tmp=f.split()
                    num_k=[int(t) for t in tmp]
                elif count==3:
                    tmp=f.split()
                    center=[float(t) for t in tmp]
                elif 3<count<7:
                    tmp=f.split()
                    self.axis[count-4]=[float(t) for t in tmp]
                else:
                    if f.find('BAND:')!=-1:
                        tmp=f.split(':')
                        n_band=int(tmp[1])-1
                    else:
                        tmp=float(f)
                        self.E_list[n_band].append(tmp)
                count=count+1
        self.axis=np.array(self.axis)
        self.Elist=np.array(self.Elist)
