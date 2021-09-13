import h5py
import numpy as np
import os
import sys
os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"
f = h5py.File(sys.argv[1],'r')
#f = h5py.File('allppm.h5','r')
allppm = f['allppm'][:]
act = f['act'][:]
conact = f['conact'][:]
spnumb = f['spnumb'][:]
ppm = allppm[0,:,:]

#decouple = int(3)
decouple = int(sys.argv[2])
html_txt0 = '''
<html lang="en">
    <body>
        <h2>Nucleotides</h2>
        <canvas id="logo_nt"></canvas>

        <h2>Amino acids</h2>
        <canvas id="logo_aa"></canvas>

        <script src="js/jseqlogo.js"></script>
        <script>
            var options = {
                "colors": jseqlogo.colors.nucleotides
            };

            var data = {
                "A": [0.5, 1.0, 0.0, 0.1, 0.0, 0.0, 0.0],
                "C": [0.8, 0.05, 0.2, 0.0, 0.5, 0.05, 0.0],
                "G": [0.01, 0.0, 0.0, 0.7, 0.0, 0.3, 0.84],
                "T": [0.2, 0.0, 0.45, 0.0, 0.3, 0.0, 0.2]
            };

            sequence_logo(document.getElementById("logo_nt"), 600, 200, data, options);


        </script>
    </body>
</html>
'''

html_txt = '''
<html lang="en">
<style>

tr td,th{

border:1px solid black;

}

.mt{

 border-collapse:collapse;

}

</style>
    %s
    <br/>
    Visit NeuronMotif website for full results: 
    <a href="https://wzthu.github.io/NeuronMotif/">https://wzthu.github.io/NeuronMotif/</a>
    <br/>
    Please wait patiently for all motif logos or patterns in the column of CN motifs to load ...
    <body>
        %s
        <script src="js/jseqlogo.js"></script>
        <script>
            var options = {
                "colors": jseqlogo.colors.nucleotides
            };

            %s
        </script>
    </body>
</html>
'''


def ppm2js(ppm, ppm_id, width, height):
    ppm += 0.0001
    v = ppm.sum(axis=1)
    v = v.repeat(4).reshape(ppm.shape)
    ppm /= v
    ppm0 = ppm.copy()
    vlg = -ppm *np.log2(ppm)
    ppm = ppm *(2 -vlg.sum(axis=1)).repeat(4).reshape(ppm.shape)
    A ='"A": [' + ','.join(['%1.2f' % (p)  for p in ppm[:,0]]) + '],'
    C ='"C": [' + ','.join(['%1.2f' % (p)  for p in ppm[:,1]]) + '],'
    G ='"G": [' + ','.join(['%1.2f' % (p)  for p in ppm[:,2]]) + '],'
    T ='"T": [' + ','.join(['%1.2f' % (p)  for p in ppm[:,3]]) + ']'
    html = 'var data = {%s};' % (A+C+G+T)
    html += 'sequence_logo(document.getElementById("%s"), %d,%d, data, options);' % (ppm_id,width,height)
    return html


filelist = []

countpre = 0
count = 0
for i in range(allppm.shape[0]):
    count += 1
    if (count > 1000 and (count % decouple)==0) or i == allppm.shape[0]-1:
        filelist.append(sys.argv[1] + '_' + str(countpre) + '_' + str(i) + '.html'  )
        countpre = i+1
        count = 0
        print(filelist[-1])

ppm_ids = []
ppm_jss = []
width=ppm.shape[0]*8
height = 50

countpre = 0
count = 0

for i in range(allppm.shape[0]):
    if True:
        ppm_id = '%04d_%04d_%.4f_%.4f_%d' % (i/decouple,i%decouple,act[i], conact[i],spnumb[i])
        ppm_js = ppm2js(allppm[i,:,:], ppm_id, width, height)
        ppm_jss.append(ppm_js)
        ppm_ids.append('<tr><td>%04d</td><td>%04d</td><td>%.4f</td><td>%.4f</td><td>%d</td><td><a href="motif_%d/tomtom.html">TomtomLink</a></td><td><canvas id="%s"></canvas></td></tr>' % (i/decouple,i%decouple,act[i], conact[i],spnumb[i], i, ppm_id))
        count += 1
    if (count > 1000 and (count % decouple)==0) or i == allppm.shape[0]-1:
        html_txt1 = html_txt % ('Page '+ ' '.join(['<a href="'+filelist[i]+'">'+str(i)+'</a>' for i in range(len(filelist))]),
'<table class="mt"><tr><td>Neuron</td><td>Decouple</td><td>MaxAct(I2)</td><td>ConsensusAct(I1)</td><td>SampleSize</td><td align=center>TomtomResult</td><td align=center>CN motifs ('+str(ppm.shape[0])+' bp)</td></tr>'+'\n'.join(ppm_ids)+'</table>', '\n'.join(ppm_jss))
        print('+++++++++')
        with open(sys.argv[1] + '_' + str(countpre) + '_' + str(i) + '.html'  ,'w') as ftest:
            ftest.write(html_txt1)
        if countpre == 0:
            with open('index.html'  ,'w') as ftest:
                ftest.write(html_txt1)
        countpre = i+1
        count = 0
        ppm_ids = []
        ppm_jss = []
        print('===========')
    
    

