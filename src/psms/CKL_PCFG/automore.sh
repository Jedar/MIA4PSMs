set -x

mergetotal=("150000" "200000" "250000")
dataset=("xato")
length1=${#mergetotal[*]}
length2=${#dataset[*]}
echo length
for((i=0;i<length1;i++))
do
	for((j=0;j<length2;j++))

do	
	merge=${mergetotal[i]}
	data=${dataset[j]}
	echo $merge
	echo $data
	#python3 bpe_simulator.py -m ../model_allE$merge -t /disk/xm/data_xm/$data"_new.txt" -s /disk/xm/bpe-pcfgMonte/eng_$merge$data".txt"
	python3 bpe_simulator.py -m ../model_allE$merge -t ../../$data"_new.txt" -s ./result/eng_$merge$data".txt"
done
done
