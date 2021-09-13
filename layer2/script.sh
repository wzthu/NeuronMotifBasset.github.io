allppmfile=allppm.h5
decouple=3
resultdir=../../bk/Basset/layer2/result/
python chen2html.py $allppmfile $decouple 
python link.py $resultdir
