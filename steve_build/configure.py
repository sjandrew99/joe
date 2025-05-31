#!/usr/bin/env python3
import os
import subprocess
import shutil

CC = 'g++'
MYPATH=os.path.abspath(__file__)
JOE_ROOT=os.path.normpath(os.path.dirname(MYPATH) + '/..') # the root of the repository
SRCDIR = JOE_ROOT+'/joe'
OBJDIR=os.path.dirname(MYPATH)+'/obj'
os.makedirs(OBJDIR,exist_ok=True)

# run configure in a subdirectory, because some stuff needs at least autoconf.h:
CONFIGURE_DIR='cfg_out'
shutil.rmtree(CONFIGURE_DIR)
os.makedirs(CONFIGURE_DIR,exist_ok=True)
os.chdir(CONFIGURE_DIR)
subprocess.run(['../../configure'])
os.chdir('..')

SRCFILES = [i for i in os.listdir(SRCDIR) if i.endswith('.c') or i.endswith('.cpp')]
OBJFILES = [OBJDIR + '/' + i + '.o' for i in SRCFILES]
SRCFILES = [SRCDIR + '/' + i for i in SRCFILES]  

makefile_lines = []

# write the recipe for the executable, joe:
line = 'joe : ' + ' '.join(OBJFILES)
makefile_lines.append(line)
line = '\t' + CC + ' ' + ' '.join(OBJFILES) + ' -o joe'
makefile_lines.append(line)
makefile_lines.append('')

for i, src in enumerate(SRCFILES):
    makefile_lines.append(OBJFILES[i] + ' : ' + src)
    makefile_lines.append('\t' + CC + ' -c ' + src + ' -o ' + OBJFILES[i] +' -I'+CONFIGURE_DIR+'/joe ' + '-DJOEDATA="\\\"/usr/local/share/joe\\\""') # idk about JOEDATA
    makefile_lines.append('')

with open('Makefile','w') as fp:
    for i in makefile_lines:
        fp.write(i); fp.write('\n')

