allppmfile=allppm.h5
decouple=12
resultdir=../../bk/Basset/layer3/result/
python chen2html.py $allppmfile $decouple 
python link.py $resultdir
