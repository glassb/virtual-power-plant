import configuration as config
import functions
import matplotlib.pyplot as plt
import time
from datetime import datetime
import os
import re
import numpy as np


STOP = 0;
NET_FLOW = 0
NODE_QUANTITY = 50

#create usableBatteries instance
#usableBatteries = np.ones(50)



#Simulate One day: 288 5-min increments in a day
for i in range(288):

	iterationValue = i
	print("\n\nIteration ",iterationValue,"\n")

	#get usable batteries set
	usableBatteries = functions.getUsableBatteries(iterationValue,config.BUY_PRICE)

	#validate that the usable batteries can meet power demand
	validateUsableBatteries = functions.validateUsableBatteries(usableBatteries)

	# if the Power Flow 0->1 does not match the aggregator power request, then unvalidate the usable battery set
	if NET_FLOW != 0:
		validateUsableBatteries = 0

	# if the usable battery set cannot met power demand, then raise the buy price
	while validateUsableBatteries == 0:

		config.BUY_PRICE += config.PRICE_STEP
		print("New Buy Price:",config.BUY_PRICE)

		usableBatteries = functions.getUsableBatteries(iterationValue,config.BUY_PRICE)
		validateUsableBatteries = functions.validateUsableBatteries(usableBatteries)

		#final conditional to stop the VPP
		if config.BUY_PRICE > config.MAX_SELL_PRICE and validateUsableBatteries == 0:
			STOP = 1
			print("VPP STOPPED: NOT ENOUGH STORAGE.")
			break

	if STOP:
		break

	'''
	#reset the buy_price every iteration
	config.BUY_PRICE = .001
	functions.randomizePrices()
	print(config.Battery1.sellPrice)
	'''

	#update load to next time step
	functions.getUpdatedLoad(config.loadData,i)
	TOTAL_LOAD = functions.getTotalLoad()
	optimalSolution = functions.optimizer(usableBatteries)



	print("P inj:",optimalSolution[0][0:NODE_QUANTITY])
	print("P flo:",optimalSolution[0][NODE_QUANTITY:2*NODE_QUANTITY])
	print("V:",optimalSolution[0][2*NODE_QUANTITY:])
	functions.updateBatteryChargeStates(optimalSolution[0][0:NODE_QUANTITY])

	print("Sell Price: ",config.BUY_PRICE)
	print("COST: ",optimalSolution[1])
	# if netFlow positive, then not supplying enough power to the substation, if negative oversupplying
	print("NET 01 FLOW: ",config.AGGREGATOR_POWER_REQUEST - TOTAL_LOAD + optimalSolution[0][NODE_QUANTITY])

	#reset net flow value
	NET_FLOW = config.AGGREGATOR_POWER_REQUEST - TOTAL_LOAD + optimalSolution[0][NODE_QUANTITY]


	print(config.Battery1.chargeState/config.Battery1.capacity)
	print(config.Battery2.chargeState/config.Battery2.capacity)
	print(config.Battery3.chargeState/config.Battery3.capacity)
	print(config.Battery4.chargeState/config.Battery4.capacity)
	print(config.Battery5.chargeState/config.Battery5.capacity)
	print(config.Battery6.chargeState/config.Battery6.capacity)
	print(config.Battery7.chargeState/config.Battery7.capacity)
	print(config.Battery8.chargeState/config.Battery8.capacity)
	print(config.Battery9.chargeState/config.Battery9.capacity)
	print(config.Battery10.chargeState/config.Battery10.capacity)
	print(config.Battery11.chargeState/config.Battery11.capacity)
	print(config.Battery12.chargeState/config.Battery12.capacity)
	print(config.Battery13.chargeState/config.Battery13.capacity)
	print(config.Battery14.chargeState/config.Battery14.capacity)
	print(config.Battery15.chargeState/config.Battery15.capacity)
	print(config.Battery16.chargeState/config.Battery16.capacity)
	print(config.Battery17.chargeState/config.Battery17.capacity)
	print(config.Battery18.chargeState/config.Battery18.capacity)
	print(config.Battery19.chargeState/config.Battery19.capacity)
	print(config.Battery20.chargeState/config.Battery20.capacity)
	print(config.Battery21.chargeState/config.Battery21.capacity)
	print(config.Battery22.chargeState/config.Battery22.capacity)
	print(config.Battery23.chargeState/config.Battery23.capacity)
	print(config.Battery24.chargeState/config.Battery24.capacity)
	print(config.Battery25.chargeState/config.Battery25.capacity)
	print(config.Battery26.chargeState/config.Battery26.capacity)
	print(config.Battery27.chargeState/config.Battery27.capacity)
	print(config.Battery28.chargeState/config.Battery28.capacity)
	print(config.Battery29.chargeState/config.Battery29.capacity)
	print(config.Battery30.chargeState/config.Battery30.capacity)
	print(config.Battery31.chargeState/config.Battery31.capacity)
	print(config.Battery32.chargeState/config.Battery32.capacity)
	print(config.Battery33.chargeState/config.Battery33.capacity)
	print(config.Battery34.chargeState/config.Battery34.capacity)
	print(config.Battery35.chargeState/config.Battery35.capacity)
	print(config.Battery36.chargeState/config.Battery36.capacity)
	print(config.Battery37.chargeState/config.Battery37.capacity)
	print(config.Battery38.chargeState/config.Battery38.capacity)
	print(config.Battery39.chargeState/config.Battery39.capacity)
	print(config.Battery40.chargeState/config.Battery40.capacity)
	print(config.Battery41.chargeState/config.Battery41.capacity)
	print(config.Battery42.chargeState/config.Battery42.capacity)
	print(config.Battery43.chargeState/config.Battery43.capacity)
	print(config.Battery44.chargeState/config.Battery44.capacity)
	print(config.Battery45.chargeState/config.Battery45.capacity)
	print(config.Battery46.chargeState/config.Battery46.capacity)
	print(config.Battery47.chargeState/config.Battery47.capacity)
	print(config.Battery48.chargeState/config.Battery48.capacity)
	print(config.Battery49.chargeState/config.Battery49.capacity)
	print(config.Battery50.chargeState/config.Battery50.capacity)


	config.outputData.loc[i] = [i,optimalSolution[0][0],optimalSolution[0][1],optimalSolution[0][2],optimalSolution[0][3],optimalSolution[0][4],optimalSolution[0][5],optimalSolution[0][6],optimalSolution[0][7],optimalSolution[0][8],
								optimalSolution[0][9],optimalSolution[0][10],optimalSolution[0][11],optimalSolution[0][12],optimalSolution[0][13],optimalSolution[0][14],optimalSolution[0][15],optimalSolution[0][16],optimalSolution[0][17],
								optimalSolution[0][18],optimalSolution[0][19],optimalSolution[0][20],optimalSolution[0][21],optimalSolution[0][22],optimalSolution[0][23],optimalSolution[0][24],optimalSolution[0][25],optimalSolution[0][26],
								optimalSolution[0][27],optimalSolution[0][28],optimalSolution[0][29],optimalSolution[0][30],optimalSolution[0][31],optimalSolution[0][32],optimalSolution[0][33],optimalSolution[0][34],optimalSolution[0][35],optimalSolution[0][36],optimalSolution[0][37],
								optimalSolution[0][38],optimalSolution[0][39],optimalSolution[0][40],optimalSolution[0][41],optimalSolution[0][42],optimalSolution[0][43],optimalSolution[0][44],optimalSolution[0][45],optimalSolution[0][46],optimalSolution[0][47],optimalSolution[0][48],
								optimalSolution[0][49],
								config.Battery1.chargeState/config.Battery1.capacity,config.Battery2.chargeState/config.Battery2.capacity,config.Battery3.chargeState/config.Battery3.capacity,
								config.Battery4.chargeState/config.Battery4.capacity,config.Battery5.chargeState/config.Battery5.capacity,config.Battery6.chargeState/config.Battery6.capacity,
								config.Battery7.chargeState/config.Battery7.capacity,config.Battery8.chargeState/config.Battery8.capacity,config.Battery9.chargeState/config.Battery9.capacity,
								config.Battery10.chargeState/config.Battery10.capacity,
								config.Battery11.chargeState/config.Battery11.capacity,config.Battery12.chargeState/config.Battery12.capacity,config.Battery13.chargeState/config.Battery13.capacity,
								config.Battery14.chargeState/config.Battery14.capacity,config.Battery15.chargeState/config.Battery15.capacity,config.Battery16.chargeState/config.Battery16.capacity,
								config.Battery17.chargeState/config.Battery17.capacity,config.Battery18.chargeState/config.Battery18.capacity,config.Battery19.chargeState/config.Battery19.capacity,
								config.Battery20.chargeState/config.Battery20.capacity,
								config.Battery21.chargeState/config.Battery21.capacity,config.Battery22.chargeState/config.Battery22.capacity,config.Battery23.chargeState/config.Battery23.capacity,
								config.Battery24.chargeState/config.Battery24.capacity,config.Battery25.chargeState/config.Battery25.capacity,config.Battery26.chargeState/config.Battery26.capacity,
								config.Battery27.chargeState/config.Battery27.capacity,config.Battery28.chargeState/config.Battery28.capacity,config.Battery29.chargeState/config.Battery29.capacity,
								config.Battery30.chargeState/config.Battery30.capacity,
								config.Battery31.chargeState/config.Battery31.capacity,config.Battery32.chargeState/config.Battery32.capacity,config.Battery33.chargeState/config.Battery33.capacity,
								config.Battery34.chargeState/config.Battery34.capacity,config.Battery35.chargeState/config.Battery35.capacity,config.Battery36.chargeState/config.Battery36.capacity,
								config.Battery37.chargeState/config.Battery37.capacity,config.Battery38.chargeState/config.Battery38.capacity,config.Battery39.chargeState/config.Battery39.capacity,
								config.Battery40.chargeState/config.Battery40.capacity,
								config.Battery41.chargeState/config.Battery41.capacity,config.Battery42.chargeState/config.Battery42.capacity,config.Battery43.chargeState/config.Battery43.capacity,
								config.Battery44.chargeState/config.Battery44.capacity,config.Battery45.chargeState/config.Battery45.capacity,config.Battery46.chargeState/config.Battery46.capacity,
								config.Battery47.chargeState/config.Battery47.capacity,config.Battery48.chargeState/config.Battery48.capacity,config.Battery49.chargeState/config.Battery49.capacity,
								config.Battery50.chargeState/config.Battery50.capacity,
								optimalSolution[0][50],optimalSolution[0][51],optimalSolution[0][52],optimalSolution[0][53],optimalSolution[0][54],optimalSolution[0][55],optimalSolution[0][56],optimalSolution[0][57],
								optimalSolution[0][58],optimalSolution[0][59],optimalSolution[0][60],optimalSolution[0][61],optimalSolution[0][62],optimalSolution[0][63],optimalSolution[0][64],optimalSolution[0][65],optimalSolution[0][66],
								optimalSolution[0][67],optimalSolution[0][68],optimalSolution[0][69],optimalSolution[0][70],optimalSolution[0][71],optimalSolution[0][72],optimalSolution[0][73],optimalSolution[0][74],optimalSolution[0][75],optimalSolution[0][76],optimalSolution[0][77],
								optimalSolution[0][78],optimalSolution[0][79],
								optimalSolution[0][80],optimalSolution[0][81],optimalSolution[0][82],optimalSolution[0][83],optimalSolution[0][84],optimalSolution[0][85],optimalSolution[0][86],optimalSolution[0][87],optimalSolution[0][88],
								optimalSolution[0][89],optimalSolution[0][90],optimalSolution[0][91],optimalSolution[0][92],optimalSolution[0][93],optimalSolution[0][94],optimalSolution[0][95],optimalSolution[0][96],optimalSolution[0][97],
								optimalSolution[0][98],optimalSolution[0][99],optimalSolution[0][100],optimalSolution[0][101],optimalSolution[0][102],optimalSolution[0][103],optimalSolution[0][104],optimalSolution[0][105],optimalSolution[0][106],
								optimalSolution[0][107],optimalSolution[0][108],optimalSolution[0][109],optimalSolution[0][110],optimalSolution[0][111],optimalSolution[0][112],optimalSolution[0][113],optimalSolution[0][114],optimalSolution[0][115],optimalSolution[0][116],optimalSolution[0][117],
								optimalSolution[0][118],optimalSolution[0][119],
								optimalSolution[0][120],optimalSolution[0][121],optimalSolution[0][122],optimalSolution[0][123],optimalSolution[0][124],optimalSolution[0][125],optimalSolution[0][126],optimalSolution[0][127],optimalSolution[0][128],optimalSolution[0][129],
								optimalSolution[0][130],optimalSolution[0][131],optimalSolution[0][132],optimalSolution[0][133],optimalSolution[0][134],optimalSolution[0][135],optimalSolution[0][136],optimalSolution[0][137],optimalSolution[0][138],optimalSolution[0][139],
								optimalSolution[0][140],optimalSolution[0][141],optimalSolution[0][142],optimalSolution[0][143],optimalSolution[0][144],optimalSolution[0][145],optimalSolution[0][146],optimalSolution[0][147],optimalSolution[0][148],optimalSolution[0][149],
								config.BUY_PRICE, optimalSolution[1]]
										

print(config.outputData)

os.chdir(config.OUTPUT_DATA_PATH)
dateTimeNow = functions.getCurrentTimeStamp()
config.outputData.to_csv("output-"+dateTimeNow+".csv")

plt.subplot(2,2,1)
plt.plot(config.outputData.loc[:,['Buy Price']])
plt.title("Buy Price")

plt.subplot(2,2,2)
plt.plot(config.outputData.loc[:,['V1']],label="V1")
plt.plot(config.outputData.loc[:,['V2']],label="V2")
plt.plot(config.outputData.loc[:,['V3']],label="V3")
plt.plot(config.outputData.loc[:,['V4']],label="V4")
plt.plot(config.outputData.loc[:,['V5']],label="V5")
plt.plot(config.outputData.loc[:,['V6']],label="V6")
plt.plot(config.outputData.loc[:,['V7']],label="V7")
plt.plot(config.outputData.loc[:,['V8']],label="V8")
plt.plot(config.outputData.loc[:,['V9']],label="V9")
plt.plot(config.outputData.loc[:,['V10']],label="V10")
plt.legend()
plt.title("Voltages")

plt.subplot(2,2,3)
plt.plot(config.outputData.loc[:,['Pf01']])
plt.title("Power Flow 01")

plt.subplot(2,2,4)
plt.plot(config.outputData.loc[:,['B4cs']])
plt.show()





#pseudocode for algorithm

'''
[1] - declare VPP event, declare initial buy price, declare AGGREGATOR_POWER_REQUEST value

[2] - define the set of usable batteries under following scenarios:

	[2a] - if this is the first event iteration, get all batteries with prices under the initial buy price
	[2b] - else, get the set of all batteries used in the last optimal power flow

[3] - discard all batteries that are at the lower charge limit (20%)

[4] - if the set can feasibly reach P based on power injection limits, move on. 
	  If the set cannot, increase the buy price and add all batteries that are below that buy price. Return to step [3].

[5] - Now that you have your set of batteries, update the bounds of the OPF so that only selected batteries are used. 
	  Still let batteries that cannot discharge still charge (but not over 80%)

[6] - solve opf under current conditions

[7] - update battery charge levels based on discharge and charge amounts. Loop for [2] - [7] until event is declared over by aggregator. 

'''


