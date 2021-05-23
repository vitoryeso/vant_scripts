import os
import pandas as pd
import sys
import sys

if len(sys.argv) != 3:
    print("invalid arguments")
    exit()

CFG_PATH = sys.argv[1]


WEIGHTS_PATH = sys.argv[2]

mAP = []
carmAP = []
busmAP = []
motmAP = []
iou = []

#pegando os nomes dos arquivos da pasta
for i in os.walk(WEIGHTS_PATH):
	f = i
	break

f = f[2]
#filtrando os nomes para pegar so os pesos
prov = []
for arq in f:
	if arq.split('.')[-1] != 'weights' or 'final' in arq or 'last' in arq or '100.' in arq:
		prov.append(arq)
for a in prov:
	f.remove(a)

for i in range(len(f)):
	cmd = '/content/darknet/darknet detector map /content/vant_scripts/vant_dataset.data /content/vant_scripts/custom_configs/' + CFG_PATH + ' ' + WEIGHTS_PATH + f[i] + ' -iou_thresh 0.50 > map.txt'
	os.system(cmd)
	arq = open('map.txt', 'r')

	while(1):
		line = arq.readline()
		if 'mAP@' in line:
			mAP.append(float(line.split(' ')[-3]))
		if 'car' in line:
			carmAP.append(float(line.split(' ')[8].split('%')[0]))
		if 'bus' in line:
			busmAP.append(float(line.split(' ')[8].split('%')[0]))
		if 'motorcycle' in line:
			motmAP.append(float(line.split(' ')[8].split('%')[0]))
		if 'average IoU' in line:
			iou.append(float(line.split(' ')[-3]))
		if line == '':
			break
	arq.close()
	os.system('rm map.txt')
for i in range(len(f)):
	f[i] = int(f[i].split('_')[-1].split('.')[0])

data = {'Iterations': f,
			'Avg_mAP': mAP,
				'car': carmAP,
					'bus': busmAP,
						'motorcycle': motmAP,
							'Avg_IOU': iou}

df = pd.DataFrame(data)
df = df.sort_values('Iterations')
df.to_csv('map.csv')
