import configuration as config
import functions
import matplotlib.pyplot as plt
import time
from datetime import datetime
import os
import re
import numpy as np

'''
SUMMARY: main code file used to run the simulation.
'''

def run():

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
		if config.NET_FLOW != 0:
			validateUsableBatteries = 0

		# if the usable battery set cannot met power demand, then raise the buy price
		while validateUsableBatteries == 0:

			config.BUY_PRICE += config.PRICE_STEP
			print("New Buy Price:",config.BUY_PRICE)

			usableBatteries = functions.getUsableBatteries(iterationValue,config.BUY_PRICE)
			validateUsableBatteries = functions.validateUsableBatteries(usableBatteries)

			#final conditional to stop the VPP
			if config.BUY_PRICE > config.MAX_SELL_PRICE and validateUsableBatteries == 0:
				config.STOP = 1
				print("VPP config.STOPPED: NOT ENOUGH STORAGE.")
				break

		if config.STOP:
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

		#run optimizer
		optimalSolution = functions.optimizer(usableBatteries)

		POWER_INJECTION_SUM = sum(optimalSolution[0][0:config.NODE_QUANTITY])
		
		#set the net flow value
		config.NET_FLOW = config.AGGREGATOR_POWER_REQUEST - TOTAL_LOAD + optimalSolution[0][config.NODE_QUANTITY]

		#printing for debugging 
		print("P inj:",optimalSolution[0][0:config.NODE_QUANTITY])
		print("P flo:",optimalSolution[0][config.NODE_QUANTITY:2*config.NODE_QUANTITY])
		print("V:",optimalSolution[0][2*config.NODE_QUANTITY:])
		print("Sell Price: ",config.BUY_PRICE)
		print("COST: ",POWER_INJECTION_SUM*config.BUY_PRICE)
		# if netFlow positive, then not supplying enough power to the substation, if negative oversupplying
		print("NET 01 FLOW: ",config.NET_FLOW)

		#update the battery charge states based on the optimizer results
		functions.updateBatteryChargeStates(optimalSolution[0][0:config.NODE_QUANTITY])

		#get the battery charge percentages
		batteryChargePercentages = functions.getBatteryChargePercentages()

		#more printing for debugging
		for q in range(len(batteryChargePercentages)):
			print(batteryChargePercentages[q])


		#form a row of output data for logs
		config.outputData.loc[i] = np.concatenate((np.array([i]),
									np.array(optimalSolution[0][0:config.NODE_QUANTITY]),
									np.array(batteryChargePercentages),
									np.array(optimalSolution[0][config.NODE_QUANTITY:]),
									np.array([config.BUY_PRICE, POWER_INJECTION_SUM*config.BUY_PRICE])))


	print(config.outputData)
	os.chdir(config.OUTPUT_DATA_PATH)
	dateTimeNow = functions.getCurrentTimeStamp()
	config.outputData.to_csv("output-"+dateTimeNow+".csv")

	#return the final BUY PRICE as a proxy for the cost of the VPP simulation
	if config.STOP == 1:
		return -1 
	else:
		return config.BUY_PRICE


functions.resetSimulation()										
run()


'''
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
'''

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


