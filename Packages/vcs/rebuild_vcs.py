import platform
prefix_path = "/lgm/cdat/Qt"
if "omar" in platform.uname():
    xpth=""
    arch="i386"
    OSX=5
    compile_line="""gcc -DNDEBUG -DGENCAIRO -L/lgm/cdat/uvcdat/Externals/lib"""

    opt="""-DDarwin -DCDCOMPAT -DPYTHON -Dincxws -Dinctty -Dincps -Dinccgm -IInclude -I/lgm/cdat/uvcdat/Externals/include -I/lgm/cdat/uvcdat/Externals/include/cairo -I/lgm/cdat/uvcdat/Externals/include/pixman-1 -I/lgm/cdat/uvcdat/Externals/include -I/lgm/cdat/uvcdat/Externals/include/freetype2 -I/lgm/cdat/uvcdat/Externals/include/libpng15 -I/lgm/cdat/uvcdat/Externals/include/freetype2 -I/lgm/cdat/uvcdat/Externals/include -I/git/cdat/Packages/vcs/Src/gctpc -I/lgm/cdat/uvcdat/Python.framework/Versions/2.7/include -I/lgm/cdat/uvcdat/Python.framework/Versions/2.7/include/cdms -I/lgm/cdat/uvcdat/Externals/include -I/lgm/cdat/uvcdat/Python.framework/Versions/2.7/include -I/usr/include -I/usr/local/include -I/git/cdat/Packages/vcs/Include/Qt -I/lgm/cdat/uvcdat/Python.framework/Versions/2.7/lib/python2.7/site-packages/numpy/core/include -I/lgm/cdat/uvcdat/Python.framework/Versions/2.7/include/python2.7 -c"""

    xopt="""-c -pipe -g -gdwarf-2 -Wall -W -DQT_GUI_LIB -DQT_CORE_LIB -DQT_SHARED -I. -pipe -g -gdwarf-2 -Wall -W -DQT_GUI_LIB -DQT_CORE_LIB -DQT_SHARED -I/Library/Frameworks -DQTEM -DUSEQT -DQTWM -DUSEQT -DCAIRODRAW
    """.strip()
else:
    xpth="/Library/Frameworks"
    arch="x86_64"
    OSX=6

    compile_line="""
    gcc -DGENCAIRO -fno-strict-aliasing -fno-common -dynamic -I/lgm/cdat/uvcdat/Externals/include -L/lgm/cdat/uvcdat/Externals/lib -arch %s -Xarch_%s -mmacosx-version-min=10.%i -isysroot /Developer/SDKs/MacOSX10.%i.sdk -pipe -I/Library/Frameworks/QtCore.framework -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -I/Developer/SDKs/MacOSX10.%i.sdk/usr/include
    """.strip() % (arch,arch,OSX,OSX,OSX)

    opt="""
    -DDarwin -DCDCOMPAT -DPYTHON -Dincxws -Dinctty -Dincps -Dinccgm -IInclude -I/lgm/cdat/uvcdat/Externals/include -I/lgm/cdat/uvcdat/Externals/include/cairo -I/lgm/cdat/uvcdat/Externals/include/pixman-1 -I/lgm/cdat/uvcdat/Externals/include/freetype2 -I/lgm/cdat/uvcdat/Externals/include -I/lgm/cdat/uvcdat/Externals/include/libpng15 -I/lgm/cdat/uvcdat/Externals/include/freetype2 -I/lgm/cdat/uvcdat/Externals/include -I/git/cdat/Packages/vcs/Src/gctpc -I/lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/include -I/lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/include/cdms -I/lgm/cdat/uvcdat/Externals/include -I/lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/include -I/usr/include -I/usr/local/include -I/git/cdat/Packages/vcs/Include/Qt -I/lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/lib/python2.7/site-packages/numpy/core/include -I/lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/include/python2.7 -c
    """.strip() % (xpth,xpth,xpth,xpth,xpth)

    xopt="""
    -c -pipe -g -gdwarf-2 -Wall -W -DQT_GUI_LIB -DQT_CORE_LIB -DQT_SHARED -I. -pipe -g -gdwarf-2 -Wall -W -DQT_GUI_LIB -DQT_CORE_LIB -DQT_SHARED -I/usr/include -DQTEM -DUSEQT -DQTWM -DUSEQT -DCAIRODRAW
    """.strip()
import os,sys
#print os.popen(cmd).readlines()
files = os.popen('find . -name "*.c*" -print').readlines()
do = []
for f in files:
    fnm=f.strip()
    if fnm.find("cdatwrap")>-1:
        continue
    if fnm.find("qpython")>-1:
        continue
    if fnm.find("xgks/cgm/cl")>-1:
        continue
    if fnm.find("/X11/")>-1:
        continue
    if fnm.find("Src/xgks/gif/gif.c")>-1:
        continue
    p,s = os.path.split(fnm)
    so=".".join(s.split(".")[:1])+".o"
    if s in """slabapimodule.c slabapi.c vcsmodule.c slabapi.c f2c_lite.c main_event_loop.cpp vcs_editor.cpp""".split():
        pb="./build/temp.macosx-10.4-%s-2.7/" % arch
    else:
        pb="./build/temp.macosx-10.4-%s-2.7/git/cdat/Packages/vcs/" % arch
    fo=pb+p+"/"+so
    if not os.path.exists(fo):
        do.append([fnm,fo])
        print "Adding missing:",do[-1][0]
        try:
            os.makedirs(os.path.split(fo)[0])
        except Exception,err:
            print err
            pass
        continue
    t1=os.stat(fnm)
    t2=os.stat(fo)
    if t1.st_mtime>t2.st_mtime:
        do.append([fnm,fo])
        print "Adding newer:",do[-1][0],t1.st_mtime,t2.st_mtime
        continue
#sys.exit()
for file,out in do:
    cmd="%s %s %s -o %s %s" % (compile_line,opt,xopt,out,file)
    cmd = cmd.replace("/lgm/cdat/uvcdat",prefix_path)
    print "Recompiling file:",file,"cmd:",cmd
    print os.popen(cmd).readlines()
    #print fnm,fo,os.path.exists(fo)
if len(do)==0:
    print "Nothing to do yeah!"
if len(sys.argv)>1: raw_input("Recompiled")
socmd = """g++ -L/lgm/cdat/uvcdat/Externals/lib -R/lgm/cdat/uvcdat/lib -R/lgm/cdat/uvcdat/Externals/lib -bind_at_load -mmacosx-version-min=10.6 -dynamiclib -install_name /lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/lib/python2.7/site-packages/vcs/_vcs.so -undefined dynamic_lookup -L/lgm/cdat/uvcdat/Externals/lib -R/lgm/cdat/uvcdat/lib -R/lgm/cdat/uvcdat/Externals/lib -bind_at_load -mmacosx-version-min=10.6 build/temp.macosx-10.4-x86_64-2.7/Src/vcsmodule.o build/temp.macosx-10.4-x86_64-2.7/Src/slabapi.o build/temp.macosx-10.4-x86_64-2.7/Src/f2c_lite.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/main.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/rscript.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/misc.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getp.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procA.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procL.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procC.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procTt.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procTo.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procTl.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procTf.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procTm.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procP.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procGi.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procCOMM.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procDisp.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/acquire.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/fintwt.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/isolines.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/pict_elem.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/format.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procTh.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procCGM.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procPage.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procCanvas.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procClear.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procGfi.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procGfo.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/err_warn.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/check_canvas_defer.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procInd.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procDump.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/outlines.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procGo.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procGcon.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/select_A.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeA.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/vcs_update.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/isofills.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/fillup.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/filldown.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/proj_gks.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procColor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeC.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeP.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/reset_A.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procRem.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procCop.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procRen.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procSleep.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeGi.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeGo.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeGfi.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeGfo.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeGcon.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeL.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeTt.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeTo.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeTl.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeTf.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeTm.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeTh.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getGi.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getGfi.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getGo.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getGfo.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getGcon.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getList.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getTt.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getTo.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getTl.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getTf.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getTm.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getTh.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getp_.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getA.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/continents.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/outfills.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/compile_vcs.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/save_image.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/save_image_vcs.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/save_gif_image_vcs.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/write_ras.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/computer.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procRun.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procPat.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procRas.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procGif.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procJpeg.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procPng.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procDRS.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procnetCDF.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procHDF.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/chkis.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/set_text_attr.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/boxfills.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procGfb.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procOvly.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/logicomp.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeGfb.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getGfb.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/compu_log.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/vectors.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getGv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeGv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procGv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procGXyvy.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procGYxvx.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procGXY.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeGXy.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeGYx.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removegxy_.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getGXyvy.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getGYxvx.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getGXY.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/Xyvy.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/Yxvx.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/XvY.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procHints.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procControl.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procGSp.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getGSp.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeGSp.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/scatter_plot.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/transform_axis.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/markers.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/python_misc.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/vcs_canvas.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/animation.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/image_routines.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procLoop.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procLoop_cdat.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/gd.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/latitude.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/meshfill.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procGfm.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeGfm.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getGfm.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procProj.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/removeProj.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/getProj.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/library/procMETA.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/act_ws.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/aspect_flags.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/cellarray.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/choice.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/colours.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/deferral_ws.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/escape.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/event.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/externinit.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/fillarea.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/gdp.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/ggdp.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/gks_error.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/input.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/inqWDT.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/inqfillareas.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/inqpixel.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/inqpmarker.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/inqpolylines.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/inqtext.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/inqtransform.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/inquiries.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/locator.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/message.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/metafile.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/open_gks.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/open_ws.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/pick.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/polylines.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/polymarkers.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/prmgr.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/segments.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/string.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/stroke.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/text.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/transforms.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/umalloc.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/update.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/valuator.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/cgm/cgmi.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/cgm/cgmo.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/gksm/gksm.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/ps/ps.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/svg/svg.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/pdf/pdf.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/png/png.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/x/xSet.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/x/xcellarray.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/x/xcolours.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/x/xevent.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/x/xfillarea.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/x/xinqpixel.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/x/xopws.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/x/xpline.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/x/xpmarker.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/x/xport.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/x/xtext.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/x/xupdate.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/alberfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/cproj.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/gnomfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/haminv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/lamccinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/obleqfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/polyfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/sinfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/stplnfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/vandgfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/alberinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/eqconfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/gnominv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/imolwfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/merfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/obleqinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/polyinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/sininv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/stplninv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/vandginv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/alconfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/eqconinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/goodfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/imolwinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/merinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/omerfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/psfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/somfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/tmfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/wivfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/alconinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/equifor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/goodinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/inv_init.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/millfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/omerinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/psinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/sominv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/tminv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/wivinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/azimfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/equiinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/gvnspfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/lamazfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/millinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/orthfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/report.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/sphdz.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/untfz.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/wviifor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/aziminv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/for_init.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/gvnspinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/lamazinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/molwfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/orthinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/robfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/sterfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/utmfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/wviiinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/br_gctp.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/gctp.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/hamfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/lamccfor.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/molwinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/paksz.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/robinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/sterinv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/gctpc/utminv.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/ttf/ttf2vcs.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/cairo/vcs2cairo.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/cairo/meta2cairo.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/xgks/cairo/cairoXemulator.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/Qt/main.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/Qt/mainwindow.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/Qt/moc_mainwindow.o build/temp.macosx-10.4-x86_64-2.7/git/cdat/Packages/vcs/Src/Qt/qti.o build/temp.macosx-10.4-x86_64-2.7/Src/events/main_event_loop.o build/temp.macosx-10.4-x86_64-2.7/Src/events/vcs_editor.o -L/lgm/cdat/uvcdat/Externals/lib -L/lgm/cdat/uvcdat/Externals/lib -L/lgm/cdat/uvcdat/Externals/lib -L/lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/lib -L/lgm/cdat/uvcdat/Externals/lib -L/usr/lib -L/usr/local/lib -lfreetype -lcairo -lm -lcdms -lnetcdf -lnetcdf -lhdf5_hl -lhdf5 -lz -lcurl -lssl -lcrypto -lldap -lz -lgrib2c -lpng -ljasper -o build/lib.macosx-10.4-x86_64-2.7/vcs/_vcs.so  -F/usr/lib -framework QtCore -framework QtGui -lz -lm
cp build/lib.macosx-10.4-x86_64-2.7/vcs/_vcs.so /lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/lib/python2.7/site-packages/vcs
""" % (xpth,xpth,xpth)
socmd=socmd.replace("x86_64",arch)
socmd=socmd.replace("/lgm/cdat/uvcdat",prefix_path)
print "So:",os.popen(socmd).readlines()
if len(sys.argv)>1: raw_input("soed")
sipcmd="""cd cdatwrap
g++ -c -pipe -I/lgm/cdat/uvcdat/Externals/include -I/lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/lib/python2.7/site-packages/vcs/Include -I/lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/include/python2.7/.. -fPIC -O2 -Wall -W -DNDEBUG -DQT_NO_DEBUG -DQT_CORE_LIB -DQT_GUI_LIB -I. -I/lgm/cdat/uvcdat/include -I/lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/include/python2.7 -I/usr/local/Qt4.7/mkspecs/macx-g++ -I/Library/Frameworks/QtCore.framework/Headers -I/Library/Frameworks/QtGui.framework/Headers -I/usr/include -F/Library/Frameworks -o sipcdatguiwrapcmodule.o sipcdatguiwrapcmodule.cpp
g++ -c -pipe -I/lgm/cdat/uvcdat/Externals/include -I/lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/lib/python2.7/site-packages/vcs/Include -I/lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/include/python2.7/.. -fPIC -O2 -Wall -W -DNDEBUG -DQT_NO_DEBUG -DQT_CORE_LIB -DQT_GUI_LIB -I. -I/lgm/cdat/uvcdat/include -I/lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/include/python2.7 -I/usr/local/Qt4.7/mkspecs/macx-g++ -I/Library/Frameworks/QtCore.framework/Headers -I/Library/Frameworks/QtGui.framework/Headers -I/usr/include -F/Library/Frameworks -o sipcdatguiwrapVCSQtManager.o sipcdatguiwrapVCSQtManager.cpp
g++ -c -pipe -I/lgm/cdat/uvcdat/Externals/include -I/lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/lib/python2.7/site-packages/vcs/Include -I/lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/include/python2.7/.. -fPIC -O2 -Wall -W -DNDEBUG -DQT_NO_DEBUG -DQT_CORE_LIB -DQT_GUI_LIB -I. -I/lgm/cdat/uvcdat/include -I/lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/include/python2.7 -I/usr/local/Qt4.7/mkspecs/macx-g++ -I/Library/Frameworks/QtCore.framework/Headers -I/Library/Frameworks/QtGui.framework/Headers -I/usr/include -F/Library/Frameworks -o sipcdatguiwrapMainWindow.o sipcdatguiwrapMainWindow.cpp
g++ -headerpad_max_install_names /lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/lib/python2.7/site-packages/vcs/_vcs.so -bundle -undefined dynamic_lookup -o cdatguiwrap.so sipcdatguiwrapcmodule.o sipcdatguiwrapVCSQtManager.o sipcdatguiwrapMainWindow.o -F/Library/Frameworks -L/Library/Frameworks -framework QtCore -framework QtGui -framework QtCore
cp -f cdatguiwrap.so /lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/lib/python2.7/site-packages/cdatguiwrap.so
echo 'Yep'
"""% (xpth,xpth,xpth,xpth,xpth,xpth,xpth,xpth,xpth,xpth,xpth)
sipcmd=sipcmd.replace("x86_64",arch)
sipcmd=sipcmd.replace("/lgm/cdat/uvcdat",prefix_path)
print "sip",os.popen(sipcmd).readlines()
if len(sys.argv)>1: raw_input("siped")
qpycmd="""g++ -O3 -c  -pipe -g -gdwarf-2 -Wall -W -DQT_GUI_LIB -DQT_CORE_LIB -DQT_SHARED -I. -pipe -g -gdwarf-2 -Wall -W -DQT_GUI_LIB -DQT_CORE_LIB -DQT_SHARED -I/usr/include  -IInclude/Qt -IInclude -I//lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/include -o build/qpython.o Src/Qt/qpython.cpp
g++ -o build/qpython build/qpython.o /lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/lib/python2.7/config/libpython2.7.a  -F/usr/lib -framework QtCore -framework QtGui -lz -lm  -lutil
cp build/qpython /lgm/cdat/uvcdat%s/Python.framework/Versions/2.7/bin/cdat
""" %(xpth,xpth,xpth)
qpycmd=qpycmd.replace("x86_64",arch)
qpycmd=qpycmd.replace("/lgm/cdat/uvcdat",prefix_path)
print "qpython:",os.popen(qpycmd).readlines()
if len(sys.argv)>1: raw_input("qpyed")
