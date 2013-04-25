import sys
import cdms2
import numpy

#Create test datasets
a=numpy.arange(10,100)
b=numpy.arange(50,150)

d1=cdms2.MV2.array(2.*a)
d2=cdms2.MV2.array(3.*b)

t1=cdms2.createAxis(a)
t1.designateTime()
t1.id='time'
t1.units='days since 2013'

t2=cdms2.createAxis(b)
t2.designateTime()
t2.id='time'
t2.units='days since 2013'


d1.setAxis(0,t1)
d2.setAxis(0,t2)
f=cdms2.open('2x.nc','w')
f.write(d1,id='y')
f.close()

f=cdms2.open('3x.nc','w')
f.write(d2,id='y')
f.branch_time=60
f.close()

#Now run a few test
import os
f1 = os.popen("%s Script/cdsplice.py -s 3x.nc -o 2x.nc -x test1.xml"%sys.executable).readlines()
f1 = os.popen("%s Script/cdsplice.py -t index -b 23 -s 3x.nc -o 2x.nc -x test2.xml"%sys.executable).readlines()
f1 = os.popen("%s Script/cdsplice.py -b 2013-1-12 -s 3x.nc -o 2x.nc -x test3.xml"%sys.executable).readlines()
f1 = os.popen("%s Script/cdsplice.py -b 23 -t value -s 3x.nc -o 2x.nc -x test4.xml").readlines()
