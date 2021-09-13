import sys
import os
dirpath = sys.argv[1]

dirs = os.listdir(dirpath)

for d in dirs:
    if not os.path.exists(os.path.join(dirpath,d,d+'.meme')):
        continue
    with open(os.path.join(dirpath,d,d+'.meme'),'r') as f: 
        line = f.readlines()[9]
    motifid = line.split(' ')[1].split('_')[0]
    motifdir = 'motif_%d' % int(motifid)
    os.system('cp -r ' + os.path.join(dirpath,d,d+'.out') +' '+ motifdir)
    os.system('cp -r ' + os.path.join(dirpath,d,d+'.meme') +' '+ motifdir)
        
     
