allppmfile=allppm.h5
decouple=1
resultdir=../../../../vis/Basset/origin/layer1/jsp/result/
python chen2html.py $allppmfile $decouple 
python link.py $resultdir
