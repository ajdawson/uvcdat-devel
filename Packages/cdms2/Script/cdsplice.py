#!/usr/bin/env python

import cdms2
import os
import sys
import argparse
import genutil
import cdtime
import warnings
import subprocess
import tempfile

parser = argparse.ArgumentParser(description= 'Splices two files together')

parser.add_argument("-o", "--origin",
                    help="Origin (first) file from which spawn was started\nIf not passed, then we will try to figure out the file you're looking for")
parser.add_argument("-s", "--spawn",
                    help="Spawn (second) file will be spliced after the origin file",
                    required=True)
parser.add_argument("-p", "--project",
                    default="CMIP5",
                    help="Project class to be used to try to figure origin file and branch times automagically")
parser.add_argument("-b",
                    "--branch",
                    help="time we want to branch spawn from in source file, i.e LAST valid time in origin")
parser.add_argument("-t", "--type",
                    default='component',
                    choices=['component','index','value'],
                    help="format the branch time was passed as")
parser.add_argument("-x", "--output",
                    help="Output file full path and name\nIf left out then output goes to stdout (screen)")
parser.add_argument("-c", "--cdscan",
                    help="Options you would like to send to cdscan while scanning origin and spawn",default="")

args = parser.parse_args(sys.argv[1:])

print args
#print args.spawn

class CMIP5(object):
    def __init__(self,spawn,origin=None,branch=None,type=None):
        """Initialize the class with spwan file"""
        if spawn[0]!='/': # Sets it to full path
            pwd = os.getcwd()
            print pwd
            spawn = os.path.join(pwd,spawn)
        try:
            self.spawn=cdms2.open(spawn)
        except Exception,err:
            raise RuntimeError,"Could not load spawn file (%s) into cdms2: %s" % (spawn,err)
        self.origin = self.findOrigin(origin)

        self.branch = self.findBranchTime(branch,type)


    def findOrigin(self,origin):
        """Automatically finds the origin from which spawn comes from"""
        if origin is not None:
            try:
                self.origin=cdms2.open(origin)
                return self.origin
            except:
                raise RuntimeError,"Could not load origin file (%s) into cdms2" % origin

        pnm = getattr(self.spawn,"uri",self.spawn.id).replace(self.spawn.experiment_id,self.spawn.parent_experiment_id)
        pnm = pnm.replace("r%ii%ip%i" % (self.spawn.realization,self.spawn.initialization_method,self.spawn.physics_version),self.spawn.parent_experiment_rip)
        self.origin = cdms2.open(pnm)
        return self.origin

    def findBranchTime(self,branch,type):
        """Automatically figures the branch time if not sent"""
        for v in self.origin.variables:
            try:
                t=self.origin[v].getTime()
                break
            except:
                pass
        bout= None
        if branch is None:
            b = float(self.spawn.branch_time)
            print b
        elif type == 'component':
            b = cdtime.s2c(branch)
        elif type=='index':
            bout = int(branch)
            if bout!=float(branch):
                raise RuntimeError,"Index must be int, you passed %s\nDid you mean to pass the type as 'value'" % branch
            if len(t)<=bout:
                raise RuntimeError,"Your start index (%i) is greater than the length of the origin (%i)" % (bout,len(t))
        if bout is None: # need to convert value to index
            try:
                bout,e = t.mapInterval((b,b,'ccb'))
                tc=t.asComponentTime()
                if e-1 != bout:
                    warnings.warn( "Hum something is odd I'm getting more than one index, please report this, command was: %s" % " ".join(sys.argv))
            except Exception,err:
                raise Exception,"Could not retrieve %s in %s, reason: %s" % (branch,self.origin.uri,err)
        return bout



def loadProject(project,*pargs,**kargs):
    if args.project == "CMIP5":
        project = CMIP5(*pargs,**kargs)
    else:
        raise RuntimeError,"Only CMIP5 implemented at this point for automation"
    return project

project = None
# figures out the source
if args.origin is None or args.branch is None:
    project = loadProject(args.project,args.spawn,origin=args.origin,branch=args.branch,type=args.type)
    spawn = getattr(project.spawn,"uri",project.spawn.id)
    origin = getattr(project.origin,"uri",project.origin.id)
    branch = project.branch
else:
    spawn = args.spawn
    origin = args.origin
    branch = args.branch

print origin,branch
tmpnm='tmp.xml'


# print "done?",

def span(file,var='ts'):
    tc = file[var].getTime().asComponentTime()
    print tc[0],tc[-1]
    return tc

print "project origin:",project.origin
print "project spawn:",project.spawn
span(project.origin)
span(project.spawn)

#tmp = tempfile.mkstemp()#dir='.')
tmp = tempfile.NamedTemporaryFile()
#Ok we now know what to do let's create the temporary xml file
cmd = "%s/bin/cdscan -x %s %s %s %s" % (sys.prefix, tmpnm, args.cdscan, origin, spawn)

print cmd
p = subprocess.Popen(cmd,shell=True,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
#                     stdout=tmp,
                     stderr=subprocess.PIPE)
#                     stderr=tmp)


print p.stdout.readlines()
print p.stderr.readlines()

print tmp.name


