import configuration as config
from scipy import optimize
import numpy as np
import time
import re
from datetime import datetime
import pandas as pd


'''
SUMMARY: all functions used in this code base. 
'''

#returns the sum of current load values for all nodes in the system
def getTotalLoad():

	TOTAL_LOAD = sum([config.Load1.loadValue,config.Load2.loadValue,config.Load3.loadValue,config.Load4.loadValue,config.Load5.loadValue,
						config.Load6.loadValue,config.Load7.loadValue,config.Load8.loadValue,config.Load9.loadValue,config.Load10.loadValue,
						config.Load11.loadValue,config.Load12.loadValue,config.Load13.loadValue,config.Load14.loadValue,config.Load15.loadValue,
						config.Load16.loadValue,config.Load17.loadValue,config.Load18.loadValue,config.Load19.loadValue,config.Load20.loadValue,
						config.Load21.loadValue,config.Load22.loadValue,config.Load23.loadValue,config.Load24.loadValue,config.Load25.loadValue,
						config.Load26.loadValue,config.Load27.loadValue,config.Load28.loadValue,config.Load29.loadValue,config.Load30.loadValue,
						config.Load31.loadValue,config.Load32.loadValue,config.Load33.loadValue,config.Load34.loadValue,config.Load35.loadValue,
						config.Load36.loadValue,config.Load37.loadValue,config.Load38.loadValue,config.Load39.loadValue,config.Load40.loadValue,
						config.Load41.loadValue,config.Load42.loadValue,config.Load43.loadValue,config.Load44.loadValue,config.Load45.loadValue,
						config.Load46.loadValue,config.Load47.loadValue,config.Load48.loadValue,config.Load49.loadValue,config.Load50.loadValue,
						config.Load51.loadValue,config.Load52.loadValue,config.Load53.loadValue,config.Load54.loadValue,config.Load55.loadValue,
						config.Load56.loadValue,config.Load57.loadValue,config.Load58.loadValue,config.Load59.loadValue,config.Load60.loadValue,
						config.Load61.loadValue,config.Load62.loadValue,config.Load63.loadValue,config.Load64.loadValue,config.Load65.loadValue,
						config.Load66.loadValue,config.Load67.loadValue,config.Load68.loadValue,config.Load69.loadValue,config.Load70.loadValue,
						config.Load71.loadValue,config.Load72.loadValue,config.Load73.loadValue,config.Load74.loadValue,config.Load75.loadValue,
						config.Load76.loadValue,config.Load77.loadValue,config.Load78.loadValue,config.Load79.loadValue,config.Load80.loadValue,
						config.Load81.loadValue,config.Load82.loadValue,config.Load83.loadValue,config.Load84.loadValue,config.Load85.loadValue,
						config.Load86.loadValue,config.Load87.loadValue,config.Load88.loadValue,config.Load89.loadValue,config.Load90.loadValue,
						config.Load91.loadValue,config.Load92.loadValue,config.Load93.loadValue,config.Load94.loadValue,config.Load95.loadValue,
						config.Load96.loadValue,config.Load97.loadValue,config.Load98.loadValue,config.Load99.loadValue,config.Load100.loadValue])

	return TOTAL_LOAD


# cost function for optimization solver
def costFunction(x,usableBatteries):

	#[Battery Power Injections, PowerFlows (starting at 01, 12, 23, etc.), Voltages starting at 1,2,3]

	'''
	usableBatteries = (-1*usableBatteries) + np.ones(config.NODE_QUANTITY)

	#zero out the costs of unselected batteries
	costMatrix = 	[config.Battery1.sellPrice*usableBatteries[0]*1000000, 
					config.Battery2.sellPrice*usableBatteries[1]*1000000, 
					config.Battery3.sellPrice*usableBatteries[2]*1000000,
					config.Battery4.sellPrice*usableBatteries[3]*1000000,
					config.Battery5.sellPrice*usableBatteries[4]*1000000,
					config.Battery6.sellPrice*usableBatteries[5]*1000000,
					config.Battery7.sellPrice*usableBatteries[6]*1000000,
					config.Battery8.sellPrice*usableBatteries[7]*1000000,
					config.Battery9.sellPrice*usableBatteries[8]*1000000,
					config.Battery10.sellPrice*usableBatteries[9]*1000000,
					config.Battery11.sellPrice*usableBatteries[10]*1000000,
					config.Battery12.sellPrice*usableBatteries[11]*1000000,
					config.Battery13.sellPrice*usableBatteries[12]*1000000,
					config.Battery14.sellPrice*usableBatteries[13]*1000000,
					config.Battery15.sellPrice*usableBatteries[14]*1000000,
					config.Battery16.sellPrice*usableBatteries[15]*1000000,
					config.Battery17.sellPrice*usableBatteries[16]*1000000,
					config.Battery18.sellPrice*usableBatteries[17]*1000000,
					config.Battery19.sellPrice*usableBatteries[18]*1000000,
					config.Battery20.sellPrice*usableBatteries[19]*1000000,
					config.Battery21.sellPrice*usableBatteries[20]*1000000,
					config.Battery22.sellPrice*usableBatteries[21]*1000000,
					config.Battery23.sellPrice*usableBatteries[22]*1000000,
					config.Battery24.sellPrice*usableBatteries[23]*1000000,
					config.Battery25.sellPrice*usableBatteries[24]*1000000,
					config.Battery26.sellPrice*usableBatteries[25]*1000000,
					config.Battery27.sellPrice*usableBatteries[26]*1000000,
					config.Battery28.sellPrice*usableBatteries[27]*1000000,
					config.Battery29.sellPrice*usableBatteries[28]*1000000,
					config.Battery30.sellPrice*usableBatteries[29]*1000000,
					config.Battery31.sellPrice*usableBatteries[30]*1000000,
					config.Battery32.sellPrice*usableBatteries[31]*1000000,
					config.Battery33.sellPrice*usableBatteries[32]*1000000,
					config.Battery34.sellPrice*usableBatteries[33]*1000000,
					config.Battery35.sellPrice*usableBatteries[34]*1000000,
					config.Battery36.sellPrice*usableBatteries[35]*1000000,
					config.Battery37.sellPrice*usableBatteries[36]*1000000,
					config.Battery38.sellPrice*usableBatteries[37]*1000000,
					config.Battery39.sellPrice*usableBatteries[38]*1000000,
					config.Battery40.sellPrice*usableBatteries[39]*1000000,
					config.Battery41.sellPrice*usableBatteries[40]*1000000,
					config.Battery42.sellPrice*usableBatteries[41]*1000000,
					config.Battery43.sellPrice*usableBatteries[42]*1000000,
					config.Battery44.sellPrice*usableBatteries[43]*1000000,
					config.Battery45.sellPrice*usableBatteries[44]*1000000,
					config.Battery46.sellPrice*usableBatteries[45]*1000000,
					config.Battery47.sellPrice*usableBatteries[46]*1000000,
					config.Battery48.sellPrice*usableBatteries[47]*1000000,
					config.Battery49.sellPrice*usableBatteries[48]*1000000,
					config.Battery50.sellPrice*usableBatteries[49]*1000000]
	'''



	#making the cost zero significantly speeds up solve time
	costMatrix = np.append(np.zeros(config.NODE_QUANTITY),np.zeros(config.NODE_QUANTITY*2))
			
			
	return np.matmul(costMatrix,x)


# function that solves the optimal power flow problem. Input is usableBatteries, which is an array that shows which batteries can be used in the opf
def optimizer(usableBatteries):

	print("Solving Optimal Power Flow.")
	initialGuess = np.zeros(3*config.NODE_QUANTITY)

	TOTAL_LOAD = getTotalLoad()

	constraints = (

			{'type': 'eq','fun': lambda x: x[config.NODE_QUANTITY] + config.AGGREGATOR_POWER_REQUEST - TOTAL_LOAD}, #power flowing from 0 to 1 needs to equal the power request

			#powerflow constraints
			{'type': 'eq','fun': lambda x: x[0] - config.Load1.loadValue - np.matmul(config.topologyMatrix[0],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[1] - config.Load2.loadValue - np.matmul(config.topologyMatrix[1],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[2] - config.Load3.loadValue - np.matmul(config.topologyMatrix[2],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[3] - config.Load4.loadValue - np.matmul(config.topologyMatrix[3],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[4] - config.Load5.loadValue - np.matmul(config.topologyMatrix[4],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[5] - config.Load6.loadValue - np.matmul(config.topologyMatrix[5],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[6] - config.Load7.loadValue - np.matmul(config.topologyMatrix[6],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[7] - config.Load8.loadValue - np.matmul(config.topologyMatrix[7],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[8] - config.Load9.loadValue - np.matmul(config.topologyMatrix[8],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[9] - config.Load10.loadValue - np.matmul(config.topologyMatrix[9],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[10] - config.Load11.loadValue - np.matmul(config.topologyMatrix[10],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[11] - config.Load12.loadValue - np.matmul(config.topologyMatrix[11],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[12] - config.Load13.loadValue - np.matmul(config.topologyMatrix[12],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[13] - config.Load14.loadValue - np.matmul(config.topologyMatrix[13],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[14] - config.Load15.loadValue - np.matmul(config.topologyMatrix[14],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[15] - config.Load16.loadValue - np.matmul(config.topologyMatrix[15],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[16] - config.Load17.loadValue - np.matmul(config.topologyMatrix[16],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[17] - config.Load18.loadValue - np.matmul(config.topologyMatrix[17],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[18] - config.Load19.loadValue - np.matmul(config.topologyMatrix[18],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[19] - config.Load20.loadValue - np.matmul(config.topologyMatrix[19],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[20] - config.Load21.loadValue - np.matmul(config.topologyMatrix[20],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[21] - config.Load22.loadValue - np.matmul(config.topologyMatrix[21],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[22] - config.Load23.loadValue - np.matmul(config.topologyMatrix[22],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[23] - config.Load24.loadValue - np.matmul(config.topologyMatrix[23],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[24] - config.Load25.loadValue - np.matmul(config.topologyMatrix[24],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[25] - config.Load26.loadValue - np.matmul(config.topologyMatrix[25],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[26] - config.Load27.loadValue - np.matmul(config.topologyMatrix[26],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[27] - config.Load28.loadValue - np.matmul(config.topologyMatrix[27],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[28] - config.Load29.loadValue - np.matmul(config.topologyMatrix[28],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[29] - config.Load30.loadValue - np.matmul(config.topologyMatrix[29],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[30] - config.Load31.loadValue - np.matmul(config.topologyMatrix[30],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[31] - config.Load32.loadValue - np.matmul(config.topologyMatrix[31],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[32] - config.Load33.loadValue - np.matmul(config.topologyMatrix[32],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[33] - config.Load34.loadValue - np.matmul(config.topologyMatrix[33],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[34] - config.Load35.loadValue - np.matmul(config.topologyMatrix[34],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[35] - config.Load36.loadValue - np.matmul(config.topologyMatrix[35],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[36] - config.Load37.loadValue - np.matmul(config.topologyMatrix[36],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[37] - config.Load38.loadValue - np.matmul(config.topologyMatrix[37],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[38] - config.Load39.loadValue - np.matmul(config.topologyMatrix[38],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[39] - config.Load40.loadValue - np.matmul(config.topologyMatrix[39],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[40] - config.Load41.loadValue - np.matmul(config.topologyMatrix[40],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[41] - config.Load42.loadValue - np.matmul(config.topologyMatrix[41],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[42] - config.Load43.loadValue - np.matmul(config.topologyMatrix[42],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[43] - config.Load44.loadValue - np.matmul(config.topologyMatrix[43],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[44] - config.Load45.loadValue - np.matmul(config.topologyMatrix[44],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[45] - config.Load46.loadValue - np.matmul(config.topologyMatrix[45],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[46] - config.Load47.loadValue - np.matmul(config.topologyMatrix[46],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[47] - config.Load48.loadValue - np.matmul(config.topologyMatrix[47],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[48] - config.Load49.loadValue - np.matmul(config.topologyMatrix[48],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[49] - config.Load50.loadValue - np.matmul(config.topologyMatrix[49],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},

			{'type': 'eq','fun': lambda x: x[50] - config.Load51.loadValue - np.matmul(config.topologyMatrix[50],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[51] - config.Load52.loadValue - np.matmul(config.topologyMatrix[51],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[52] - config.Load53.loadValue - np.matmul(config.topologyMatrix[52],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[53] - config.Load54.loadValue - np.matmul(config.topologyMatrix[53],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[54] - config.Load55.loadValue - np.matmul(config.topologyMatrix[54],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[55] - config.Load56.loadValue - np.matmul(config.topologyMatrix[55],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[56] - config.Load57.loadValue - np.matmul(config.topologyMatrix[56],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[57] - config.Load58.loadValue - np.matmul(config.topologyMatrix[57],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[58] - config.Load59.loadValue - np.matmul(config.topologyMatrix[58],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[59] - config.Load60.loadValue - np.matmul(config.topologyMatrix[59],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[60] - config.Load61.loadValue - np.matmul(config.topologyMatrix[60],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[61] - config.Load62.loadValue - np.matmul(config.topologyMatrix[61],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[62] - config.Load63.loadValue - np.matmul(config.topologyMatrix[62],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[63] - config.Load64.loadValue - np.matmul(config.topologyMatrix[63],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[64] - config.Load65.loadValue - np.matmul(config.topologyMatrix[64],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[65] - config.Load66.loadValue - np.matmul(config.topologyMatrix[65],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[66] - config.Load67.loadValue - np.matmul(config.topologyMatrix[66],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[67] - config.Load68.loadValue - np.matmul(config.topologyMatrix[67],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[68] - config.Load69.loadValue - np.matmul(config.topologyMatrix[68],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[69] - config.Load70.loadValue - np.matmul(config.topologyMatrix[69],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[70] - config.Load71.loadValue - np.matmul(config.topologyMatrix[70],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[71] - config.Load72.loadValue - np.matmul(config.topologyMatrix[71],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[72] - config.Load73.loadValue - np.matmul(config.topologyMatrix[72],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[73] - config.Load74.loadValue - np.matmul(config.topologyMatrix[73],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[74] - config.Load75.loadValue - np.matmul(config.topologyMatrix[74],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[75] - config.Load76.loadValue - np.matmul(config.topologyMatrix[75],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[76] - config.Load77.loadValue - np.matmul(config.topologyMatrix[76],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[77] - config.Load78.loadValue - np.matmul(config.topologyMatrix[77],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[78] - config.Load79.loadValue - np.matmul(config.topologyMatrix[78],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[79] - config.Load80.loadValue - np.matmul(config.topologyMatrix[79],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[80] - config.Load81.loadValue - np.matmul(config.topologyMatrix[80],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[81] - config.Load82.loadValue - np.matmul(config.topologyMatrix[81],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[82] - config.Load83.loadValue - np.matmul(config.topologyMatrix[82],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[83] - config.Load84.loadValue - np.matmul(config.topologyMatrix[83],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[84] - config.Load85.loadValue - np.matmul(config.topologyMatrix[84],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[85] - config.Load86.loadValue - np.matmul(config.topologyMatrix[85],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[86] - config.Load87.loadValue - np.matmul(config.topologyMatrix[86],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[87] - config.Load88.loadValue - np.matmul(config.topologyMatrix[87],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[88] - config.Load89.loadValue - np.matmul(config.topologyMatrix[88],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[89] - config.Load90.loadValue - np.matmul(config.topologyMatrix[89],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[90] - config.Load91.loadValue - np.matmul(config.topologyMatrix[90],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[91] - config.Load92.loadValue - np.matmul(config.topologyMatrix[91],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[92] - config.Load93.loadValue - np.matmul(config.topologyMatrix[92],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[93] - config.Load94.loadValue - np.matmul(config.topologyMatrix[93],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[94] - config.Load95.loadValue - np.matmul(config.topologyMatrix[94],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[95] - config.Load96.loadValue - np.matmul(config.topologyMatrix[95],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[96] - config.Load97.loadValue - np.matmul(config.topologyMatrix[96],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[97] - config.Load98.loadValue - np.matmul(config.topologyMatrix[97],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[98] - config.Load99.loadValue - np.matmul(config.topologyMatrix[98],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},
			{'type': 'eq','fun': lambda x: x[99] - config.Load100.loadValue - np.matmul(config.topologyMatrix[99],x[config.NODE_QUANTITY:config.NODE_QUANTITY*2])},

			#voltage constraints
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[0],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[0],x[config.NODE_QUANTITY*2:]) - 2*(config.Line12.impedance*x[101]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[1],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[1],x[config.NODE_QUANTITY*2:]) - 2*(config.Line23.impedance*x[102]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[2],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[2],x[config.NODE_QUANTITY*2:]) - 2*(config.Line14.impedance*x[103]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[3],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[3],x[config.NODE_QUANTITY*2:]) - 2*(config.Line45.impedance*x[104]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[4],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[4],x[config.NODE_QUANTITY*2:]) - 2*(config.Line56.impedance*x[105]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[5],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[5],x[config.NODE_QUANTITY*2:]) - 2*(config.Line17.impedance*x[106]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[6],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[6],x[config.NODE_QUANTITY*2:]) - 2*(config.Line78.impedance*x[107]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[7],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[7],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[108]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[8],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[8],x[config.NODE_QUANTITY*2:]) - 2*(config.Line9x10.impedance*x[109]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[9],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[9],x[config.NODE_QUANTITY*2:]) - 2*(config.Line10x11.impedance*x[110]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[10],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[10],x[config.NODE_QUANTITY*2:]) - 2*(config.Line11x12.impedance*x[111]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[11],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[11],x[config.NODE_QUANTITY*2:]) - 2*(config.Line12x13.impedance*x[112]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[12],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[12],x[config.NODE_QUANTITY*2:]) - 2*(config.Line14.impedance*x[113]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[13],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[13],x[config.NODE_QUANTITY*2:]) - 2*(config.Line45.impedance*x[114]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[14],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[14],x[config.NODE_QUANTITY*2:]) - 2*(config.Line56.impedance*x[115]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[15],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[15],x[config.NODE_QUANTITY*2:]) - 2*(config.Line17.impedance*x[116]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[16],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[16],x[config.NODE_QUANTITY*2:]) - 2*(config.Line78.impedance*x[117]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[17],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[17],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[118]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[18],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[18],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[119]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[19],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[19],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[120]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[20],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[20],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[121]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[21],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[21],x[config.NODE_QUANTITY*2:]) - 2*(config.Line23.impedance*x[122]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[22],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[22],x[config.NODE_QUANTITY*2:]) - 2*(config.Line14.impedance*x[123]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[23],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[23],x[config.NODE_QUANTITY*2:]) - 2*(config.Line45.impedance*x[124]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[24],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[24],x[config.NODE_QUANTITY*2:]) - 2*(config.Line56.impedance*x[125]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[25],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[25],x[config.NODE_QUANTITY*2:]) - 2*(config.Line17.impedance*x[126]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[26],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[26],x[config.NODE_QUANTITY*2:]) - 2*(config.Line78.impedance*x[127]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[27],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[27],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[128]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[28],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[28],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[129]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[29],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[29],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[130]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[30],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[30],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[131]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[31],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[31],x[config.NODE_QUANTITY*2:]) - 2*(config.Line23.impedance*x[132]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[32],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[32],x[config.NODE_QUANTITY*2:]) - 2*(config.Line14.impedance*x[133]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[33],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[33],x[config.NODE_QUANTITY*2:]) - 2*(config.Line45.impedance*x[134]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[34],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[34],x[config.NODE_QUANTITY*2:]) - 2*(config.Line56.impedance*x[135]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[35],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[35],x[config.NODE_QUANTITY*2:]) - 2*(config.Line17.impedance*x[136]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[36],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[36],x[config.NODE_QUANTITY*2:]) - 2*(config.Line78.impedance*x[137]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[37],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[37],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[138]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[38],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[38],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[139]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[39],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[39],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[140]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[40],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[40],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[141]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[41],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[41],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[142]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[42],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[42],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[143]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[43],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[43],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[144]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[44],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[44],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[145]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[45],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[45],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[146]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[46],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[46],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[147]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[47],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[47],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[148]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[48],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[48],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[149]).real},

			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[49],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[49],x[config.NODE_QUANTITY*2:]) - 2*(config.Line12.impedance*x[150]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[50],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[50],x[config.NODE_QUANTITY*2:]) - 2*(config.Line12.impedance*x[151]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[51],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[51],x[config.NODE_QUANTITY*2:]) - 2*(config.Line23.impedance*x[152]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[52],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[52],x[config.NODE_QUANTITY*2:]) - 2*(config.Line14.impedance*x[153]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[53],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[53],x[config.NODE_QUANTITY*2:]) - 2*(config.Line45.impedance*x[154]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[54],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[54],x[config.NODE_QUANTITY*2:]) - 2*(config.Line56.impedance*x[155]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[55],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[55],x[config.NODE_QUANTITY*2:]) - 2*(config.Line17.impedance*x[156]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[56],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[56],x[config.NODE_QUANTITY*2:]) - 2*(config.Line78.impedance*x[157]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[57],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[57],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[158]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[58],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[58],x[config.NODE_QUANTITY*2:]) - 2*(config.Line9x10.impedance*x[159]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[59],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[59],x[config.NODE_QUANTITY*2:]) - 2*(config.Line10x11.impedance*x[160]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[60],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[60],x[config.NODE_QUANTITY*2:]) - 2*(config.Line12.impedance*x[161]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[61],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[61],x[config.NODE_QUANTITY*2:]) - 2*(config.Line23.impedance*x[162]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[62],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[62],x[config.NODE_QUANTITY*2:]) - 2*(config.Line14.impedance*x[163]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[63],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[63],x[config.NODE_QUANTITY*2:]) - 2*(config.Line45.impedance*x[164]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[64],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[64],x[config.NODE_QUANTITY*2:]) - 2*(config.Line56.impedance*x[165]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[65],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[65],x[config.NODE_QUANTITY*2:]) - 2*(config.Line17.impedance*x[166]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[66],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[66],x[config.NODE_QUANTITY*2:]) - 2*(config.Line78.impedance*x[167]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[67],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[67],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[168]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[68],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[68],x[config.NODE_QUANTITY*2:]) - 2*(config.Line9x10.impedance*x[169]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[69],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[69],x[config.NODE_QUANTITY*2:]) - 2*(config.Line10x11.impedance*x[170]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[70],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[70],x[config.NODE_QUANTITY*2:]) - 2*(config.Line12.impedance*x[171]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[71],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[71],x[config.NODE_QUANTITY*2:]) - 2*(config.Line23.impedance*x[172]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[72],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[72],x[config.NODE_QUANTITY*2:]) - 2*(config.Line14.impedance*x[173]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[73],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[73],x[config.NODE_QUANTITY*2:]) - 2*(config.Line45.impedance*x[174]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[74],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[74],x[config.NODE_QUANTITY*2:]) - 2*(config.Line56.impedance*x[175]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[75],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[75],x[config.NODE_QUANTITY*2:]) - 2*(config.Line17.impedance*x[176]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[76],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[76],x[config.NODE_QUANTITY*2:]) - 2*(config.Line78.impedance*x[177]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[77],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[77],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[178]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[78],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[78],x[config.NODE_QUANTITY*2:]) - 2*(config.Line9x10.impedance*x[179]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[79],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[79],x[config.NODE_QUANTITY*2:]) - 2*(config.Line10x11.impedance*x[180]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[80],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[80],x[config.NODE_QUANTITY*2:]) - 2*(config.Line12.impedance*x[181]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[81],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[81],x[config.NODE_QUANTITY*2:]) - 2*(config.Line23.impedance*x[182]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[82],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[82],x[config.NODE_QUANTITY*2:]) - 2*(config.Line14.impedance*x[183]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[83],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[83],x[config.NODE_QUANTITY*2:]) - 2*(config.Line45.impedance*x[184]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[84],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[84],x[config.NODE_QUANTITY*2:]) - 2*(config.Line56.impedance*x[185]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[85],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[85],x[config.NODE_QUANTITY*2:]) - 2*(config.Line17.impedance*x[186]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[86],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[86],x[config.NODE_QUANTITY*2:]) - 2*(config.Line78.impedance*x[187]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[87],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[87],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[188]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[88],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[88],x[config.NODE_QUANTITY*2:]) - 2*(config.Line9x10.impedance*x[189]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[89],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[89],x[config.NODE_QUANTITY*2:]) - 2*(config.Line10x11.impedance*x[190]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[90],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[90],x[config.NODE_QUANTITY*2:]) - 2*(config.Line12.impedance*x[191]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[91],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[91],x[config.NODE_QUANTITY*2:]) - 2*(config.Line23.impedance*x[192]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[92],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[92],x[config.NODE_QUANTITY*2:]) - 2*(config.Line14.impedance*x[193]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[93],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[93],x[config.NODE_QUANTITY*2:]) - 2*(config.Line45.impedance*x[194]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[94],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[94],x[config.NODE_QUANTITY*2:]) - 2*(config.Line56.impedance*x[195]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[95],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[95],x[config.NODE_QUANTITY*2:]) - 2*(config.Line17.impedance*x[196]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[96],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[96],x[config.NODE_QUANTITY*2:]) - 2*(config.Line78.impedance*x[197]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[97],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[97],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[198]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[98],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[98],x[config.NODE_QUANTITY*2:]) - 2*(config.Line9x10.impedance*x[199]).real},

			#battery charge percentage constraints (basically, if you discharge or charge the battery, it can't end up above or below the max or min charging percentages)
			
			#for some reason the minimum charge state percentage constraints are giving unfeasible answers. 
			#when the usable batteries get close to 30%, essentially you are constraining the problem to use very little 
			#power from only a few batteries, so I think this triggers an infeasible answer.
			{'type': 'ineq','fun': lambda x: -1*(config.Battery1.chargeState - (x[0])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery1.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery2.chargeState - (x[1])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery2.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery3.chargeState - (x[2])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery3.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery4.chargeState - (x[3])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery4.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery5.chargeState - (x[4])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery5.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery6.chargeState - (x[5])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery6.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery7.chargeState - (x[6])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery7.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery8.chargeState - (x[7])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery8.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery9.chargeState - (x[8])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery9.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery10.chargeState - (x[9])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery10.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery11.chargeState - (x[10])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery11.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery12.chargeState - (x[11])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery12.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery13.chargeState - (x[12])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery13.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery14.chargeState - (x[13])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery14.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery15.chargeState - (x[14])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery15.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery16.chargeState - (x[15])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery16.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery17.chargeState - (x[16])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery17.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery18.chargeState - (x[17])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery18.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery19.chargeState - (x[18])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery19.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery20.chargeState - (x[19])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery20.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery21.chargeState - (x[20])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery21.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery22.chargeState - (x[21])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery22.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery23.chargeState - (x[22])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery23.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery24.chargeState - (x[23])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery24.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery25.chargeState - (x[24])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery25.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery26.chargeState - (x[25])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery26.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery27.chargeState - (x[26])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery27.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery28.chargeState - (x[27])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery28.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery29.chargeState - (x[28])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery29.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery30.chargeState - (x[29])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery30.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery31.chargeState - (x[30])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery31.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery32.chargeState - (x[31])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery32.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery33.chargeState - (x[32])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery33.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery34.chargeState - (x[33])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery34.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery35.chargeState - (x[34])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery35.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery36.chargeState - (x[35])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery36.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery37.chargeState - (x[36])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery37.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery38.chargeState - (x[37])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery38.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery39.chargeState - (x[38])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery39.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery40.chargeState - (x[39])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery40.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery41.chargeState - (x[40])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery41.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery42.chargeState - (x[41])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery42.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery43.chargeState - (x[42])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery43.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery44.chargeState - (x[43])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery44.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery45.chargeState - (x[44])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery45.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery46.chargeState - (x[45])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery46.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery47.chargeState - (x[46])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery47.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery48.chargeState - (x[47])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery48.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery49.chargeState - (x[48])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery49.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery50.chargeState - (x[49])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery50.capacity) + config.MAX_CHARGE_PERCENTAGE},

			{'type': 'ineq','fun': lambda x: -1*(config.Battery51.chargeState - (x[50])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery51.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery52.chargeState - (x[51])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery52.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery53.chargeState - (x[52])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery53.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery54.chargeState - (x[53])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery54.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery55.chargeState - (x[54])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery55.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery56.chargeState - (x[55])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery56.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery57.chargeState - (x[56])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery57.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery58.chargeState - (x[57])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery58.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery59.chargeState - (x[58])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery59.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery60.chargeState - (x[59])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery60.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery61.chargeState - (x[60])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery61.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery62.chargeState - (x[61])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery62.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery63.chargeState - (x[62])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery63.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery64.chargeState - (x[63])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery64.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery65.chargeState - (x[64])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery65.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery66.chargeState - (x[65])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery66.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery67.chargeState - (x[66])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery67.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery68.chargeState - (x[67])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery68.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery69.chargeState - (x[68])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery69.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery70.chargeState - (x[69])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery70.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery71.chargeState - (x[70])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery71.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery72.chargeState - (x[71])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery72.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery73.chargeState - (x[72])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery73.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery74.chargeState - (x[73])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery74.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery75.chargeState - (x[74])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery75.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery76.chargeState - (x[75])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery76.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery77.chargeState - (x[76])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery77.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery78.chargeState - (x[77])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery78.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery79.chargeState - (x[78])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery79.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery80.chargeState - (x[79])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery80.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery81.chargeState - (x[80])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery81.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery82.chargeState - (x[81])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery82.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery83.chargeState - (x[82])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery83.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery84.chargeState - (x[83])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery84.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery85.chargeState - (x[84])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery85.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery86.chargeState - (x[85])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery86.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery87.chargeState - (x[86])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery87.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery88.chargeState - (x[87])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery88.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery89.chargeState - (x[88])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery89.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery90.chargeState - (x[89])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery90.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery91.chargeState - (x[90])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery91.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery92.chargeState - (x[91])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery92.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery93.chargeState - (x[92])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery93.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery94.chargeState - (x[93])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery94.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery95.chargeState - (x[94])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery95.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery96.chargeState - (x[95])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery96.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery97.chargeState - (x[96])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery97.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery98.chargeState - (x[97])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery98.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery99.chargeState - (x[98])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery99.capacity) + config.MAX_CHARGE_PERCENTAGE},
			{'type': 'ineq','fun': lambda x: -1*(config.Battery100.chargeState - (x[99])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery100.capacity) + config.MAX_CHARGE_PERCENTAGE})


	#bounds
	#if a battery isnt selected, then the max power go to 0, so it cannot be used. Discharging batteries only.
	bounds = ((0,config.Battery1.maxPower*usableBatteries[0]),
			(0,config.Battery2.maxPower*usableBatteries[1]),
			(0,config.Battery3.maxPower*usableBatteries[2]),
			(0,config.Battery4.maxPower*usableBatteries[3]),
			(0,config.Battery5.maxPower*usableBatteries[4]),	
			(0,config.Battery6.maxPower*usableBatteries[5]),	
			(0,config.Battery7.maxPower*usableBatteries[6]),
			(0,config.Battery8.maxPower*usableBatteries[7]),
			(0,config.Battery9.maxPower*usableBatteries[8]),
			(0,config.Battery10.maxPower*usableBatteries[9]),
			(0,config.Battery11.maxPower*usableBatteries[10]),
			(0,config.Battery12.maxPower*usableBatteries[11]), 	
			(0,config.Battery13.maxPower*usableBatteries[12]),
			(0,config.Battery14.maxPower*usableBatteries[13]),	
			(0,config.Battery15.maxPower*usableBatteries[14]),
			(0,config.Battery16.maxPower*usableBatteries[15]),	
			(0,config.Battery17.maxPower*usableBatteries[16]),
			(0,config.Battery18.maxPower*usableBatteries[17]),
			(0,config.Battery19.maxPower*usableBatteries[18]),
			(0,config.Battery20.maxPower*usableBatteries[19]),
			(0,config.Battery21.maxPower*usableBatteries[20]),
			(0,config.Battery22.maxPower*usableBatteries[21]), 	
			(0,config.Battery23.maxPower*usableBatteries[22]),	
			(0,config.Battery24.maxPower*usableBatteries[23]),	
			(0,config.Battery25.maxPower*usableBatteries[24]),	
			(0,config.Battery26.maxPower*usableBatteries[25]),	
			(0,config.Battery27.maxPower*usableBatteries[26]),
			(0,config.Battery28.maxPower*usableBatteries[27]),
			(0,config.Battery29.maxPower*usableBatteries[28]),
			(0,config.Battery30.maxPower*usableBatteries[29]),
			(0,config.Battery31.maxPower*usableBatteries[30]),
			(0,config.Battery32.maxPower*usableBatteries[31]), 
			(0,config.Battery33.maxPower*usableBatteries[32]),	
			(0,config.Battery34.maxPower*usableBatteries[33]),
			(0,config.Battery35.maxPower*usableBatteries[34]),	
			(0,config.Battery36.maxPower*usableBatteries[35]),	
			(0,config.Battery37.maxPower*usableBatteries[36]),
			(0,config.Battery38.maxPower*usableBatteries[37]),
			(0,config.Battery39.maxPower*usableBatteries[38]),
			(0,config.Battery40.maxPower*usableBatteries[39]),
			(0,config.Battery41.maxPower*usableBatteries[40]),
			(0,config.Battery42.maxPower*usableBatteries[41]), 	
			(0,config.Battery43.maxPower*usableBatteries[42]),	
			(0,config.Battery44.maxPower*usableBatteries[43]),
			(0,config.Battery45.maxPower*usableBatteries[44]),	
			(0,config.Battery46.maxPower*usableBatteries[45]),	
			(0,config.Battery47.maxPower*usableBatteries[46]),
			(0,config.Battery48.maxPower*usableBatteries[47]),
			(0,config.Battery49.maxPower*usableBatteries[48]),
			(0,config.Battery50.maxPower*usableBatteries[49]),
			(0,config.Battery51.maxPower*usableBatteries[50]),
			(0,config.Battery52.maxPower*usableBatteries[51]),
			(0,config.Battery53.maxPower*usableBatteries[52]),
			(0,config.Battery54.maxPower*usableBatteries[53]),
			(0,config.Battery55.maxPower*usableBatteries[54]),	
			(0,config.Battery56.maxPower*usableBatteries[55]),	
			(0,config.Battery57.maxPower*usableBatteries[56]),
			(0,config.Battery58.maxPower*usableBatteries[57]),
			(0,config.Battery59.maxPower*usableBatteries[58]),
			(0,config.Battery60.maxPower*usableBatteries[59]),
			(0,config.Battery61.maxPower*usableBatteries[60]),
			(0,config.Battery62.maxPower*usableBatteries[61]),
			(0,config.Battery63.maxPower*usableBatteries[62]),
			(0,config.Battery64.maxPower*usableBatteries[63]),
			(0,config.Battery65.maxPower*usableBatteries[64]),	
			(0,config.Battery66.maxPower*usableBatteries[65]),	
			(0,config.Battery67.maxPower*usableBatteries[66]),
			(0,config.Battery68.maxPower*usableBatteries[67]),
			(0,config.Battery69.maxPower*usableBatteries[68]),
			(0,config.Battery70.maxPower*usableBatteries[69]),
			(0,config.Battery71.maxPower*usableBatteries[70]),
			(0,config.Battery72.maxPower*usableBatteries[71]),
			(0,config.Battery73.maxPower*usableBatteries[72]),
			(0,config.Battery74.maxPower*usableBatteries[73]),
			(0,config.Battery75.maxPower*usableBatteries[74]),	
			(0,config.Battery76.maxPower*usableBatteries[75]),	
			(0,config.Battery77.maxPower*usableBatteries[76]),
			(0,config.Battery78.maxPower*usableBatteries[77]),
			(0,config.Battery79.maxPower*usableBatteries[78]),
			(0,config.Battery80.maxPower*usableBatteries[79]),
			(0,config.Battery81.maxPower*usableBatteries[80]),
			(0,config.Battery82.maxPower*usableBatteries[81]),
			(0,config.Battery83.maxPower*usableBatteries[82]),
			(0,config.Battery84.maxPower*usableBatteries[83]),
			(0,config.Battery85.maxPower*usableBatteries[84]),	
			(0,config.Battery86.maxPower*usableBatteries[85]),	
			(0,config.Battery87.maxPower*usableBatteries[86]),
			(0,config.Battery88.maxPower*usableBatteries[87]),
			(0,config.Battery89.maxPower*usableBatteries[88]),
			(0,config.Battery90.maxPower*usableBatteries[89]),
			(0,config.Battery91.maxPower*usableBatteries[90]),
			(0,config.Battery92.maxPower*usableBatteries[91]),
			(0,config.Battery93.maxPower*usableBatteries[92]),
			(0,config.Battery94.maxPower*usableBatteries[93]),
			(0,config.Battery95.maxPower*usableBatteries[94]),	
			(0,config.Battery96.maxPower*usableBatteries[95]),	
			(0,config.Battery97.maxPower*usableBatteries[96]),
			(0,config.Battery98.maxPower*usableBatteries[97]),
			(0,config.Battery99.maxPower*usableBatteries[98]),
			(0,config.Battery100.maxPower*usableBatteries[99]),

			(config.Line01.minPowerFlow,config.Line01.maxPowerFlow),
			(config.Line12.minPowerFlow,config.Line12.maxPowerFlow),
			(config.Line23.minPowerFlow,config.Line23.maxPowerFlow),
			(config.Line14.minPowerFlow,config.Line14.maxPowerFlow),
			(config.Line45.minPowerFlow,config.Line45.maxPowerFlow),
			(config.Line56.minPowerFlow,config.Line56.maxPowerFlow),
			(config.Line17.minPowerFlow,config.Line17.maxPowerFlow),
			(config.Line78.minPowerFlow,config.Line78.maxPowerFlow),
			(config.Line89.minPowerFlow,config.Line89.maxPowerFlow),
			(config.Line9x10.minPowerFlow,config.Line9x10.maxPowerFlow),
			(config.Line10x11.minPowerFlow,config.Line10x11.maxPowerFlow),
			(config.Line11x12.minPowerFlow,config.Line11x12.maxPowerFlow),
			(config.Line12x13.minPowerFlow,config.Line12x13.maxPowerFlow),
			(config.Line13x14.minPowerFlow,config.Line13x14.maxPowerFlow),
			(config.Line14x15.minPowerFlow,config.Line14x15.maxPowerFlow),
			(config.Line15x16.minPowerFlow,config.Line15x16.maxPowerFlow),
			(config.Line16x17.minPowerFlow,config.Line16x17.maxPowerFlow),
			(config.Line17x18.minPowerFlow,config.Line17x18.maxPowerFlow),
			(config.Line18x19.minPowerFlow,config.Line18x19.maxPowerFlow),
			(config.Line19x20.minPowerFlow,config.Line19x20.maxPowerFlow),
			(config.Line3x21.minPowerFlow,config.Line3x21.maxPowerFlow),
			(config.Line21x22.minPowerFlow,config.Line21x22.maxPowerFlow),
			(config.Line22x23.minPowerFlow,config.Line22x23.maxPowerFlow),
			(config.Line23x24.minPowerFlow,config.Line23x24.maxPowerFlow),
			(config.Line24x25.minPowerFlow,config.Line24x25.maxPowerFlow),
			(config.Line25x26.minPowerFlow,config.Line25x26.maxPowerFlow),
			(config.Line26x27.minPowerFlow,config.Line26x27.maxPowerFlow),
			(config.Line27x28.minPowerFlow,config.Line27x28.maxPowerFlow),
			(config.Line28x29.minPowerFlow,config.Line28x29.maxPowerFlow),
			(config.Line29x30.minPowerFlow,config.Line29x30.maxPowerFlow),
			(config.Line6x31.minPowerFlow,config.Line6x31.maxPowerFlow),
			(config.Line31x32.minPowerFlow,config.Line31x32.maxPowerFlow),
			(config.Line32x33.minPowerFlow,config.Line32x33.maxPowerFlow),
			(config.Line33x34.minPowerFlow,config.Line33x34.maxPowerFlow),
			(config.Line34x35.minPowerFlow,config.Line34x35.maxPowerFlow),
			(config.Line35x36.minPowerFlow,config.Line35x36.maxPowerFlow),
			(config.Line36x37.minPowerFlow,config.Line36x37.maxPowerFlow),
			(config.Line37x38.minPowerFlow,config.Line37x38.maxPowerFlow),
			(config.Line38x39.minPowerFlow,config.Line38x39.maxPowerFlow),
			(config.Line39x40.minPowerFlow,config.Line39x40.maxPowerFlow),
			(config.Line36x41.minPowerFlow,config.Line36x41.maxPowerFlow),
			(config.Line41x42.minPowerFlow,config.Line41x42.maxPowerFlow),
			(config.Line42x43.minPowerFlow,config.Line42x43.maxPowerFlow),
			(config.Line43x44.minPowerFlow,config.Line43x44.maxPowerFlow),
			(config.Line44x45.minPowerFlow,config.Line44x45.maxPowerFlow),
			(config.Line45x46.minPowerFlow,config.Line45x46.maxPowerFlow),
			(config.Line46x47.minPowerFlow,config.Line46x47.maxPowerFlow),
			(config.Line47x48.minPowerFlow,config.Line47x48.maxPowerFlow),
			(config.Line48x49.minPowerFlow,config.Line48x49.maxPowerFlow),
			(config.Line49x50.minPowerFlow,config.Line49x50.maxPowerFlow),

			(config.Line01.minPowerFlow,config.Line01.maxPowerFlow),
			(config.Line12.minPowerFlow,config.Line12.maxPowerFlow),
			(config.Line23.minPowerFlow,config.Line23.maxPowerFlow),
			(config.Line14.minPowerFlow,config.Line14.maxPowerFlow),
			(config.Line45.minPowerFlow,config.Line45.maxPowerFlow),
			(config.Line56.minPowerFlow,config.Line56.maxPowerFlow),
			(config.Line17.minPowerFlow,config.Line17.maxPowerFlow),
			(config.Line78.minPowerFlow,config.Line78.maxPowerFlow),
			(config.Line89.minPowerFlow,config.Line89.maxPowerFlow),
			(config.Line9x10.minPowerFlow,config.Line9x10.maxPowerFlow),
			(config.Line10x11.minPowerFlow,config.Line10x11.maxPowerFlow),
			(config.Line11x12.minPowerFlow,config.Line11x12.maxPowerFlow),
			(config.Line12x13.minPowerFlow,config.Line12x13.maxPowerFlow),
			(config.Line13x14.minPowerFlow,config.Line13x14.maxPowerFlow),
			(config.Line14x15.minPowerFlow,config.Line14x15.maxPowerFlow),
			(config.Line15x16.minPowerFlow,config.Line15x16.maxPowerFlow),
			(config.Line16x17.minPowerFlow,config.Line16x17.maxPowerFlow),
			(config.Line17x18.minPowerFlow,config.Line17x18.maxPowerFlow),
			(config.Line18x19.minPowerFlow,config.Line18x19.maxPowerFlow),
			(config.Line19x20.minPowerFlow,config.Line19x20.maxPowerFlow),
			(config.Line3x21.minPowerFlow,config.Line3x21.maxPowerFlow),
			(config.Line21x22.minPowerFlow,config.Line21x22.maxPowerFlow),
			(config.Line22x23.minPowerFlow,config.Line22x23.maxPowerFlow),
			(config.Line23x24.minPowerFlow,config.Line23x24.maxPowerFlow),
			(config.Line24x25.minPowerFlow,config.Line24x25.maxPowerFlow),
			(config.Line25x26.minPowerFlow,config.Line25x26.maxPowerFlow),
			(config.Line26x27.minPowerFlow,config.Line26x27.maxPowerFlow),
			(config.Line27x28.minPowerFlow,config.Line27x28.maxPowerFlow),
			(config.Line28x29.minPowerFlow,config.Line28x29.maxPowerFlow),
			(config.Line29x30.minPowerFlow,config.Line29x30.maxPowerFlow),
			(config.Line6x31.minPowerFlow,config.Line6x31.maxPowerFlow),
			(config.Line31x32.minPowerFlow,config.Line31x32.maxPowerFlow),
			(config.Line32x33.minPowerFlow,config.Line32x33.maxPowerFlow),
			(config.Line33x34.minPowerFlow,config.Line33x34.maxPowerFlow),
			(config.Line34x35.minPowerFlow,config.Line34x35.maxPowerFlow),
			(config.Line35x36.minPowerFlow,config.Line35x36.maxPowerFlow),
			(config.Line36x37.minPowerFlow,config.Line36x37.maxPowerFlow),
			(config.Line37x38.minPowerFlow,config.Line37x38.maxPowerFlow),
			(config.Line38x39.minPowerFlow,config.Line38x39.maxPowerFlow),
			(config.Line39x40.minPowerFlow,config.Line39x40.maxPowerFlow),
			(config.Line36x41.minPowerFlow,config.Line36x41.maxPowerFlow),
			(config.Line41x42.minPowerFlow,config.Line41x42.maxPowerFlow),
			(config.Line42x43.minPowerFlow,config.Line42x43.maxPowerFlow),
			(config.Line43x44.minPowerFlow,config.Line43x44.maxPowerFlow),
			(config.Line44x45.minPowerFlow,config.Line44x45.maxPowerFlow),
			(config.Line45x46.minPowerFlow,config.Line45x46.maxPowerFlow),
			(config.Line46x47.minPowerFlow,config.Line46x47.maxPowerFlow),
			(config.Line47x48.minPowerFlow,config.Line47x48.maxPowerFlow),
			(config.Line48x49.minPowerFlow,config.Line48x49.maxPowerFlow),
			(config.Line49x50.minPowerFlow,config.Line49x50.maxPowerFlow),


			(config.Node1.minVoltage,config.Node1.maxVoltage),
			(config.Node2.minVoltage,config.Node2.maxVoltage),
			(config.Node3.minVoltage,config.Node3.maxVoltage),
			(config.Node4.minVoltage,config.Node4.maxVoltage),
			(config.Node5.minVoltage,config.Node5.maxVoltage),
			(config.Node6.minVoltage,config.Node6.maxVoltage),
			(config.Node7.minVoltage,config.Node7.maxVoltage),
			(config.Node8.minVoltage,config.Node8.maxVoltage),
			(config.Node9.minVoltage,config.Node9.maxVoltage),
			(config.Node10.minVoltage,config.Node10.maxVoltage),
			(config.Node11.minVoltage,config.Node11.maxVoltage),
			(config.Node12.minVoltage,config.Node12.maxVoltage),
			(config.Node13.minVoltage,config.Node13.maxVoltage),
			(config.Node14.minVoltage,config.Node14.maxVoltage),
			(config.Node15.minVoltage,config.Node15.maxVoltage),
			(config.Node16.minVoltage,config.Node16.maxVoltage),
			(config.Node17.minVoltage,config.Node17.maxVoltage),
			(config.Node18.minVoltage,config.Node18.maxVoltage),
			(config.Node19.minVoltage,config.Node19.maxVoltage),
			(config.Node20.minVoltage,config.Node20.maxVoltage),
			(config.Node21.minVoltage,config.Node21.maxVoltage),
			(config.Node22.minVoltage,config.Node22.maxVoltage),
			(config.Node23.minVoltage,config.Node23.maxVoltage),
			(config.Node24.minVoltage,config.Node24.maxVoltage),
			(config.Node25.minVoltage,config.Node25.maxVoltage),
			(config.Node26.minVoltage,config.Node26.maxVoltage),
			(config.Node27.minVoltage,config.Node27.maxVoltage),
			(config.Node28.minVoltage,config.Node28.maxVoltage),
			(config.Node29.minVoltage,config.Node29.maxVoltage),
			(config.Node30.minVoltage,config.Node30.maxVoltage),
			(config.Node31.minVoltage,config.Node31.maxVoltage),
			(config.Node32.minVoltage,config.Node32.maxVoltage),
			(config.Node33.minVoltage,config.Node33.maxVoltage),
			(config.Node34.minVoltage,config.Node34.maxVoltage),
			(config.Node35.minVoltage,config.Node35.maxVoltage),
			(config.Node36.minVoltage,config.Node36.maxVoltage),
			(config.Node37.minVoltage,config.Node37.maxVoltage),
			(config.Node38.minVoltage,config.Node38.maxVoltage),
			(config.Node39.minVoltage,config.Node39.maxVoltage),
			(config.Node40.minVoltage,config.Node40.maxVoltage),
			(config.Node41.minVoltage,config.Node41.maxVoltage),
			(config.Node42.minVoltage,config.Node42.maxVoltage),
			(config.Node43.minVoltage,config.Node43.maxVoltage),
			(config.Node44.minVoltage,config.Node44.maxVoltage),
			(config.Node45.minVoltage,config.Node45.maxVoltage),
			(config.Node46.minVoltage,config.Node46.maxVoltage),
			(config.Node47.minVoltage,config.Node47.maxVoltage),
			(config.Node48.minVoltage,config.Node48.maxVoltage),
			(config.Node49.minVoltage,config.Node49.maxVoltage),
			(config.Node50.minVoltage,config.Node50.maxVoltage),

			(config.Node51.minVoltage,config.Node51.maxVoltage),
			(config.Node52.minVoltage,config.Node52.maxVoltage),
			(config.Node53.minVoltage,config.Node53.maxVoltage),
			(config.Node54.minVoltage,config.Node54.maxVoltage),
			(config.Node55.minVoltage,config.Node55.maxVoltage),
			(config.Node56.minVoltage,config.Node56.maxVoltage),
			(config.Node57.minVoltage,config.Node57.maxVoltage),
			(config.Node58.minVoltage,config.Node58.maxVoltage),
			(config.Node59.minVoltage,config.Node59.maxVoltage),
			(config.Node60.minVoltage,config.Node60.maxVoltage),
			(config.Node61.minVoltage,config.Node61.maxVoltage),
			(config.Node62.minVoltage,config.Node62.maxVoltage),
			(config.Node63.minVoltage,config.Node63.maxVoltage),
			(config.Node64.minVoltage,config.Node64.maxVoltage),
			(config.Node65.minVoltage,config.Node65.maxVoltage),
			(config.Node66.minVoltage,config.Node66.maxVoltage),
			(config.Node67.minVoltage,config.Node67.maxVoltage),
			(config.Node68.minVoltage,config.Node68.maxVoltage),
			(config.Node69.minVoltage,config.Node69.maxVoltage),
			(config.Node70.minVoltage,config.Node70.maxVoltage),
			(config.Node71.minVoltage,config.Node71.maxVoltage),
			(config.Node72.minVoltage,config.Node72.maxVoltage),
			(config.Node73.minVoltage,config.Node73.maxVoltage),
			(config.Node74.minVoltage,config.Node74.maxVoltage),
			(config.Node75.minVoltage,config.Node75.maxVoltage),
			(config.Node76.minVoltage,config.Node76.maxVoltage),
			(config.Node77.minVoltage,config.Node77.maxVoltage),
			(config.Node78.minVoltage,config.Node78.maxVoltage),
			(config.Node79.minVoltage,config.Node79.maxVoltage),
			(config.Node80.minVoltage,config.Node80.maxVoltage),
			(config.Node81.minVoltage,config.Node81.maxVoltage),
			(config.Node82.minVoltage,config.Node82.maxVoltage),
			(config.Node83.minVoltage,config.Node83.maxVoltage),
			(config.Node84.minVoltage,config.Node84.maxVoltage),
			(config.Node85.minVoltage,config.Node85.maxVoltage),
			(config.Node86.minVoltage,config.Node86.maxVoltage),
			(config.Node87.minVoltage,config.Node87.maxVoltage),
			(config.Node88.minVoltage,config.Node88.maxVoltage),
			(config.Node89.minVoltage,config.Node89.maxVoltage),
			(config.Node90.minVoltage,config.Node90.maxVoltage),
			(config.Node91.minVoltage,config.Node91.maxVoltage),
			(config.Node92.minVoltage,config.Node92.maxVoltage),
			(config.Node93.minVoltage,config.Node93.maxVoltage),
			(config.Node94.minVoltage,config.Node94.maxVoltage),
			(config.Node95.minVoltage,config.Node95.maxVoltage),
			(config.Node96.minVoltage,config.Node96.maxVoltage),
			(config.Node97.minVoltage,config.Node97.maxVoltage),
			(config.Node98.minVoltage,config.Node98.maxVoltage),
			(config.Node99.minVoltage,config.Node99.maxVoltage),
			(config.Node100.minVoltage,config.Node100.maxVoltage))

	startTime = time.time()

	#this idea of writing this line came from the scipy minimize documentation (See "Examples" section): https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#rdd2e1855725e-12
	costFunctionNested = lambda x: costFunction(x, usableBatteries)

	optimalSolution = optimize.minimize(costFunctionNested,initialGuess,constraints=constraints,bounds=bounds) #method="trust-constr"
	endTime = time.time()
	runTime = endTime - startTime
	print("Optimal Power Flow finished in run time of",runTime,"seconds.")

	return [optimalSolution.x,optimalSolution.fun]


# updates the Battery Charge States based on charging or discharging activity in previous opf round
def updateBatteryChargeStates(powerInjectionValues):
	config.Battery1.chargeState = config.Battery1.chargeState - powerInjectionValues[0]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery2.chargeState = config.Battery2.chargeState - powerInjectionValues[1]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery3.chargeState = config.Battery3.chargeState - powerInjectionValues[2]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery4.chargeState = config.Battery4.chargeState - powerInjectionValues[3]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery5.chargeState = config.Battery5.chargeState - powerInjectionValues[4]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery6.chargeState = config.Battery6.chargeState - powerInjectionValues[5]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery7.chargeState = config.Battery7.chargeState - powerInjectionValues[6]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery8.chargeState = config.Battery8.chargeState - powerInjectionValues[7]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery9.chargeState = config.Battery9.chargeState - powerInjectionValues[8]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery10.chargeState = config.Battery10.chargeState - powerInjectionValues[9]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery11.chargeState = config.Battery11.chargeState - powerInjectionValues[10]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery12.chargeState = config.Battery12.chargeState - powerInjectionValues[11]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery13.chargeState = config.Battery13.chargeState - powerInjectionValues[12]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery14.chargeState = config.Battery14.chargeState - powerInjectionValues[13]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery15.chargeState = config.Battery15.chargeState - powerInjectionValues[14]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery16.chargeState = config.Battery16.chargeState - powerInjectionValues[15]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery17.chargeState = config.Battery17.chargeState - powerInjectionValues[16]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery18.chargeState = config.Battery18.chargeState - powerInjectionValues[17]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery19.chargeState = config.Battery19.chargeState - powerInjectionValues[18]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery20.chargeState = config.Battery20.chargeState - powerInjectionValues[19]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery21.chargeState = config.Battery21.chargeState - powerInjectionValues[20]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery22.chargeState = config.Battery22.chargeState - powerInjectionValues[21]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery23.chargeState = config.Battery23.chargeState - powerInjectionValues[22]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery24.chargeState = config.Battery24.chargeState - powerInjectionValues[23]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery25.chargeState = config.Battery25.chargeState - powerInjectionValues[24]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery26.chargeState = config.Battery26.chargeState - powerInjectionValues[25]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery27.chargeState = config.Battery27.chargeState - powerInjectionValues[26]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery28.chargeState = config.Battery28.chargeState - powerInjectionValues[27]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery29.chargeState = config.Battery29.chargeState - powerInjectionValues[28]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery30.chargeState = config.Battery30.chargeState - powerInjectionValues[29]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery31.chargeState = config.Battery31.chargeState - powerInjectionValues[30]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery32.chargeState = config.Battery32.chargeState - powerInjectionValues[31]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery33.chargeState = config.Battery33.chargeState - powerInjectionValues[32]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery34.chargeState = config.Battery34.chargeState - powerInjectionValues[33]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery35.chargeState = config.Battery35.chargeState - powerInjectionValues[34]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery36.chargeState = config.Battery36.chargeState - powerInjectionValues[35]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery37.chargeState = config.Battery37.chargeState - powerInjectionValues[36]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery38.chargeState = config.Battery38.chargeState - powerInjectionValues[37]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery39.chargeState = config.Battery39.chargeState - powerInjectionValues[38]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery40.chargeState = config.Battery40.chargeState - powerInjectionValues[39]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery41.chargeState = config.Battery41.chargeState - powerInjectionValues[40]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery42.chargeState = config.Battery42.chargeState - powerInjectionValues[41]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery43.chargeState = config.Battery43.chargeState - powerInjectionValues[42]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery44.chargeState = config.Battery44.chargeState - powerInjectionValues[43]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery45.chargeState = config.Battery45.chargeState - powerInjectionValues[44]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery46.chargeState = config.Battery46.chargeState - powerInjectionValues[45]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery47.chargeState = config.Battery47.chargeState - powerInjectionValues[46]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery48.chargeState = config.Battery48.chargeState - powerInjectionValues[47]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery49.chargeState = config.Battery49.chargeState - powerInjectionValues[48]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery50.chargeState = config.Battery50.chargeState - powerInjectionValues[49]*(config.FIVE_MINUTE_SCALING_FACTOR)

	config.Battery51.chargeState = config.Battery51.chargeState - powerInjectionValues[50]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery52.chargeState = config.Battery52.chargeState - powerInjectionValues[51]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery53.chargeState = config.Battery53.chargeState - powerInjectionValues[52]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery54.chargeState = config.Battery54.chargeState - powerInjectionValues[53]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery55.chargeState = config.Battery55.chargeState - powerInjectionValues[54]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery56.chargeState = config.Battery56.chargeState - powerInjectionValues[55]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery57.chargeState = config.Battery57.chargeState - powerInjectionValues[56]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery58.chargeState = config.Battery58.chargeState - powerInjectionValues[57]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery59.chargeState = config.Battery59.chargeState - powerInjectionValues[58]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery60.chargeState = config.Battery60.chargeState - powerInjectionValues[59]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery61.chargeState = config.Battery61.chargeState - powerInjectionValues[60]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery62.chargeState = config.Battery62.chargeState - powerInjectionValues[61]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery63.chargeState = config.Battery63.chargeState - powerInjectionValues[62]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery64.chargeState = config.Battery64.chargeState - powerInjectionValues[63]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery65.chargeState = config.Battery65.chargeState - powerInjectionValues[64]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery66.chargeState = config.Battery66.chargeState - powerInjectionValues[65]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery67.chargeState = config.Battery67.chargeState - powerInjectionValues[66]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery68.chargeState = config.Battery68.chargeState - powerInjectionValues[67]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery69.chargeState = config.Battery69.chargeState - powerInjectionValues[68]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery70.chargeState = config.Battery70.chargeState - powerInjectionValues[69]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery71.chargeState = config.Battery71.chargeState - powerInjectionValues[70]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery72.chargeState = config.Battery72.chargeState - powerInjectionValues[71]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery73.chargeState = config.Battery73.chargeState - powerInjectionValues[72]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery74.chargeState = config.Battery74.chargeState - powerInjectionValues[73]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery75.chargeState = config.Battery75.chargeState - powerInjectionValues[74]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery76.chargeState = config.Battery76.chargeState - powerInjectionValues[75]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery77.chargeState = config.Battery77.chargeState - powerInjectionValues[76]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery78.chargeState = config.Battery78.chargeState - powerInjectionValues[77]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery79.chargeState = config.Battery79.chargeState - powerInjectionValues[78]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery80.chargeState = config.Battery80.chargeState - powerInjectionValues[79]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery81.chargeState = config.Battery81.chargeState - powerInjectionValues[80]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery82.chargeState = config.Battery82.chargeState - powerInjectionValues[81]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery83.chargeState = config.Battery83.chargeState - powerInjectionValues[82]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery84.chargeState = config.Battery84.chargeState - powerInjectionValues[83]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery85.chargeState = config.Battery85.chargeState - powerInjectionValues[84]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery86.chargeState = config.Battery86.chargeState - powerInjectionValues[85]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery87.chargeState = config.Battery87.chargeState - powerInjectionValues[86]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery88.chargeState = config.Battery88.chargeState - powerInjectionValues[87]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery89.chargeState = config.Battery89.chargeState - powerInjectionValues[88]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery90.chargeState = config.Battery90.chargeState - powerInjectionValues[89]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery91.chargeState = config.Battery91.chargeState - powerInjectionValues[90]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery92.chargeState = config.Battery92.chargeState - powerInjectionValues[91]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery93.chargeState = config.Battery93.chargeState - powerInjectionValues[92]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery94.chargeState = config.Battery94.chargeState - powerInjectionValues[93]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery95.chargeState = config.Battery95.chargeState - powerInjectionValues[94]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery96.chargeState = config.Battery96.chargeState - powerInjectionValues[95]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery97.chargeState = config.Battery97.chargeState - powerInjectionValues[96]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery98.chargeState = config.Battery98.chargeState - powerInjectionValues[97]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery99.chargeState = config.Battery99.chargeState - powerInjectionValues[98]*(config.FIVE_MINUTE_SCALING_FACTOR)
	config.Battery100.chargeState = config.Battery100.chargeState - powerInjectionValues[99]*(config.FIVE_MINUTE_SCALING_FACTOR)
	
	return None



# defines the usable set of batteries for the upcoming opf based on buy price and minimum charge
def getUsableBatteries(iterationValue,buyPrice,lastRoundBatteries=None):

	#generates a boolean array where the value is 0 if over the buy price and 1 if less than the buy price
	if (iterationValue == 0) or (lastRoundBatteries is None): 

		usableBatteries = np.transpose([
			int(config.Battery1.sellPrice <= buyPrice),
			int(config.Battery2.sellPrice <= buyPrice),
			int(config.Battery3.sellPrice <= buyPrice),
			int(config.Battery4.sellPrice <= buyPrice),
			int(config.Battery5.sellPrice <= buyPrice),
			int(config.Battery6.sellPrice <= buyPrice),
			int(config.Battery7.sellPrice <= buyPrice),
			int(config.Battery8.sellPrice <= buyPrice),
			int(config.Battery9.sellPrice <= buyPrice),
			int(config.Battery10.sellPrice <= buyPrice),
			int(config.Battery11.sellPrice <= buyPrice),
			int(config.Battery12.sellPrice <= buyPrice),
			int(config.Battery13.sellPrice <= buyPrice),
			int(config.Battery14.sellPrice <= buyPrice),
			int(config.Battery15.sellPrice <= buyPrice),
			int(config.Battery16.sellPrice <= buyPrice),
			int(config.Battery17.sellPrice <= buyPrice),
			int(config.Battery18.sellPrice <= buyPrice),
			int(config.Battery19.sellPrice <= buyPrice),
			int(config.Battery20.sellPrice <= buyPrice),
			int(config.Battery21.sellPrice <= buyPrice),
			int(config.Battery22.sellPrice <= buyPrice),
			int(config.Battery23.sellPrice <= buyPrice),
			int(config.Battery24.sellPrice <= buyPrice),
			int(config.Battery25.sellPrice <= buyPrice),
			int(config.Battery26.sellPrice <= buyPrice),
			int(config.Battery27.sellPrice <= buyPrice),
			int(config.Battery28.sellPrice <= buyPrice),
			int(config.Battery29.sellPrice <= buyPrice),
			int(config.Battery30.sellPrice <= buyPrice),
			int(config.Battery31.sellPrice <= buyPrice),
			int(config.Battery32.sellPrice <= buyPrice),
			int(config.Battery33.sellPrice <= buyPrice),
			int(config.Battery34.sellPrice <= buyPrice),
			int(config.Battery35.sellPrice <= buyPrice),
			int(config.Battery36.sellPrice <= buyPrice),
			int(config.Battery37.sellPrice <= buyPrice),
			int(config.Battery38.sellPrice <= buyPrice),
			int(config.Battery39.sellPrice <= buyPrice),
			int(config.Battery40.sellPrice <= buyPrice),
			int(config.Battery41.sellPrice <= buyPrice),
			int(config.Battery42.sellPrice <= buyPrice),
			int(config.Battery43.sellPrice <= buyPrice),
			int(config.Battery44.sellPrice <= buyPrice),
			int(config.Battery45.sellPrice <= buyPrice),
			int(config.Battery46.sellPrice <= buyPrice),
			int(config.Battery47.sellPrice <= buyPrice),
			int(config.Battery48.sellPrice <= buyPrice),
			int(config.Battery49.sellPrice <= buyPrice),
			int(config.Battery50.sellPrice <= buyPrice),

			int(config.Battery51.sellPrice <= buyPrice),
			int(config.Battery52.sellPrice <= buyPrice),
			int(config.Battery53.sellPrice <= buyPrice),
			int(config.Battery54.sellPrice <= buyPrice),
			int(config.Battery55.sellPrice <= buyPrice),
			int(config.Battery56.sellPrice <= buyPrice),
			int(config.Battery57.sellPrice <= buyPrice),
			int(config.Battery58.sellPrice <= buyPrice),
			int(config.Battery59.sellPrice <= buyPrice),
			int(config.Battery60.sellPrice <= buyPrice),
			int(config.Battery61.sellPrice <= buyPrice),
			int(config.Battery62.sellPrice <= buyPrice),
			int(config.Battery63.sellPrice <= buyPrice),
			int(config.Battery64.sellPrice <= buyPrice),
			int(config.Battery65.sellPrice <= buyPrice),
			int(config.Battery66.sellPrice <= buyPrice),
			int(config.Battery67.sellPrice <= buyPrice),
			int(config.Battery68.sellPrice <= buyPrice),
			int(config.Battery69.sellPrice <= buyPrice),
			int(config.Battery70.sellPrice <= buyPrice),
			int(config.Battery71.sellPrice <= buyPrice),
			int(config.Battery72.sellPrice <= buyPrice),
			int(config.Battery73.sellPrice <= buyPrice),
			int(config.Battery74.sellPrice <= buyPrice),
			int(config.Battery75.sellPrice <= buyPrice),
			int(config.Battery76.sellPrice <= buyPrice),
			int(config.Battery77.sellPrice <= buyPrice),
			int(config.Battery78.sellPrice <= buyPrice),
			int(config.Battery79.sellPrice <= buyPrice),
			int(config.Battery80.sellPrice <= buyPrice),
			int(config.Battery81.sellPrice <= buyPrice),
			int(config.Battery82.sellPrice <= buyPrice),
			int(config.Battery83.sellPrice <= buyPrice),
			int(config.Battery84.sellPrice <= buyPrice),
			int(config.Battery85.sellPrice <= buyPrice),
			int(config.Battery86.sellPrice <= buyPrice),
			int(config.Battery87.sellPrice <= buyPrice),
			int(config.Battery88.sellPrice <= buyPrice),
			int(config.Battery89.sellPrice <= buyPrice),
			int(config.Battery90.sellPrice <= buyPrice),
			int(config.Battery91.sellPrice <= buyPrice),
			int(config.Battery92.sellPrice <= buyPrice),
			int(config.Battery93.sellPrice <= buyPrice),
			int(config.Battery94.sellPrice <= buyPrice),
			int(config.Battery95.sellPrice <= buyPrice),
			int(config.Battery96.sellPrice <= buyPrice),
			int(config.Battery97.sellPrice <= buyPrice),
			int(config.Battery98.sellPrice <= buyPrice),
			int(config.Battery99.sellPrice <= buyPrice),
			int(config.Battery100.sellPrice <= buyPrice)])

	else:
		usableBatteries = lastRoundBatteries

	#ensures that all batteries are above their minimum charge state
	usableBatteryChargeStateLow = np.transpose([
		int(config.Battery1.chargeState/config.Battery1.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery2.chargeState/config.Battery2.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery3.chargeState/config.Battery3.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery4.chargeState/config.Battery4.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery5.chargeState/config.Battery5.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery6.chargeState/config.Battery6.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery7.chargeState/config.Battery7.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery8.chargeState/config.Battery8.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery9.chargeState/config.Battery9.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery10.chargeState/config.Battery10.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery11.chargeState/config.Battery11.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery12.chargeState/config.Battery12.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery13.chargeState/config.Battery13.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery14.chargeState/config.Battery14.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery15.chargeState/config.Battery15.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery16.chargeState/config.Battery16.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery17.chargeState/config.Battery17.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery18.chargeState/config.Battery18.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery19.chargeState/config.Battery19.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery20.chargeState/config.Battery20.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery21.chargeState/config.Battery21.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery22.chargeState/config.Battery22.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery23.chargeState/config.Battery23.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery24.chargeState/config.Battery24.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery25.chargeState/config.Battery25.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery26.chargeState/config.Battery26.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery27.chargeState/config.Battery27.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery28.chargeState/config.Battery28.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery29.chargeState/config.Battery29.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery30.chargeState/config.Battery30.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery31.chargeState/config.Battery31.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery32.chargeState/config.Battery32.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery33.chargeState/config.Battery33.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery34.chargeState/config.Battery34.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery35.chargeState/config.Battery35.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery36.chargeState/config.Battery36.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery37.chargeState/config.Battery37.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery38.chargeState/config.Battery38.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery39.chargeState/config.Battery39.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery40.chargeState/config.Battery40.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery41.chargeState/config.Battery41.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery42.chargeState/config.Battery42.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery43.chargeState/config.Battery43.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery44.chargeState/config.Battery44.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery45.chargeState/config.Battery45.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery46.chargeState/config.Battery46.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery47.chargeState/config.Battery47.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery48.chargeState/config.Battery48.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery49.chargeState/config.Battery49.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery50.chargeState/config.Battery50.capacity > config.MIN_CHARGE_PERCENTAGE),

		int(config.Battery51.chargeState/config.Battery51.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery52.chargeState/config.Battery52.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery53.chargeState/config.Battery53.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery54.chargeState/config.Battery54.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery55.chargeState/config.Battery55.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery56.chargeState/config.Battery56.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery57.chargeState/config.Battery57.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery58.chargeState/config.Battery58.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery59.chargeState/config.Battery59.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery60.chargeState/config.Battery60.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery61.chargeState/config.Battery61.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery62.chargeState/config.Battery62.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery63.chargeState/config.Battery63.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery64.chargeState/config.Battery64.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery65.chargeState/config.Battery65.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery66.chargeState/config.Battery66.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery67.chargeState/config.Battery67.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery68.chargeState/config.Battery68.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery69.chargeState/config.Battery69.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery70.chargeState/config.Battery70.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery71.chargeState/config.Battery71.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery72.chargeState/config.Battery72.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery73.chargeState/config.Battery73.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery74.chargeState/config.Battery74.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery75.chargeState/config.Battery75.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery76.chargeState/config.Battery76.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery77.chargeState/config.Battery77.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery78.chargeState/config.Battery78.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery79.chargeState/config.Battery79.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery80.chargeState/config.Battery80.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery81.chargeState/config.Battery81.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery82.chargeState/config.Battery82.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery83.chargeState/config.Battery83.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery84.chargeState/config.Battery84.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery85.chargeState/config.Battery85.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery86.chargeState/config.Battery86.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery87.chargeState/config.Battery87.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery88.chargeState/config.Battery88.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery89.chargeState/config.Battery89.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery90.chargeState/config.Battery90.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery91.chargeState/config.Battery91.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery92.chargeState/config.Battery92.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery93.chargeState/config.Battery93.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery94.chargeState/config.Battery94.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery95.chargeState/config.Battery95.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery96.chargeState/config.Battery96.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery97.chargeState/config.Battery97.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery98.chargeState/config.Battery98.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery99.chargeState/config.Battery99.capacity > config.MIN_CHARGE_PERCENTAGE),
		int(config.Battery100.chargeState/config.Battery100.capacity > config.MIN_CHARGE_PERCENTAGE)])

	'''
	usableBatteryChargeStateHigh = np.transpose([
		int(config.Battery1.chargeState/config.Battery1.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery2.chargeState/config.Battery2.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery3.chargeState/config.Battery3.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery4.chargeState/config.Battery4.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery5.chargeState/config.Battery5.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery6.chargeState/config.Battery6.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery7.chargeState/config.Battery7.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery8.chargeState/config.Battery8.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery9.chargeState/config.Battery9.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery10.chargeState/config.Battery10.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery11.chargeState/config.Battery11.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery12.chargeState/config.Battery12.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery13.chargeState/config.Battery13.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery14.chargeState/config.Battery14.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery15.chargeState/config.Battery15.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery16.chargeState/config.Battery16.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery17.chargeState/config.Battery17.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery18.chargeState/config.Battery18.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery19.chargeState/config.Battery19.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery20.chargeState/config.Battery20.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery21.chargeState/config.Battery21.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery22.chargeState/config.Battery22.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery23.chargeState/config.Battery23.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery24.chargeState/config.Battery24.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery25.chargeState/config.Battery25.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery26.chargeState/config.Battery26.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery27.chargeState/config.Battery27.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery28.chargeState/config.Battery28.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery29.chargeState/config.Battery29.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery30.chargeState/config.Battery30.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery31.chargeState/config.Battery31.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery32.chargeState/config.Battery32.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery33.chargeState/config.Battery33.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery34.chargeState/config.Battery34.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery35.chargeState/config.Battery35.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery36.chargeState/config.Battery36.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery37.chargeState/config.Battery37.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery38.chargeState/config.Battery38.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery39.chargeState/config.Battery39.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery40.chargeState/config.Battery40.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery41.chargeState/config.Battery41.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery42.chargeState/config.Battery42.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery43.chargeState/config.Battery43.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery44.chargeState/config.Battery44.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery45.chargeState/config.Battery45.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery46.chargeState/config.Battery46.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery47.chargeState/config.Battery47.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery48.chargeState/config.Battery48.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery49.chargeState/config.Battery49.capacity < config.MAX_CHARGE_PERCENTAGE),
		int(config.Battery50.chargeState/config.Battery50.capacity < config.MAX_CHARGE_PERCENTAGE)])
		'''
	#usableBatteryChargeState = np.multiply(usableBatteryChargeStateHigh,usableBatteryChargeStateLow)
	usableBatteriesCount = sum(np.multiply(usableBatteries,usableBatteryChargeStateLow))
	print("Retrieved",usableBatteriesCount,"usable batteries below set buy price $",buyPrice,"/kW.")

	#this should return a list of batteries to remove from the opf, i.e. set their power injection bounds to 0
	return np.multiply(usableBatteries,usableBatteryChargeStateLow)


#validate the selected batteries can actively meet power request
def validateUsableBatteries(usableBatteries):

	#take the minimum value of the charge state or the maximum power, because that will determine if the batteries can meet demand.
	powerCapacity = [min(config.Battery1.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery1.maxPower)*usableBatteries[0],
					min(config.Battery2.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery2.maxPower)*usableBatteries[1],
					min(config.Battery3.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery3.maxPower)*usableBatteries[2],
					min(config.Battery4.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery4.maxPower)*usableBatteries[3],
					min(config.Battery5.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery5.maxPower)*usableBatteries[4],
					min(config.Battery6.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery6.maxPower)*usableBatteries[5],
					min(config.Battery7.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery7.maxPower)*usableBatteries[6],
					min(config.Battery8.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery8.maxPower)*usableBatteries[7],
					min(config.Battery9.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery9.maxPower)*usableBatteries[8],
					min(config.Battery10.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery10.maxPower)*usableBatteries[9],
					min(config.Battery11.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery11.maxPower)*usableBatteries[10],
					min(config.Battery12.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery12.maxPower)*usableBatteries[11],
					min(config.Battery13.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery13.maxPower)*usableBatteries[12],
					min(config.Battery14.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery14.maxPower)*usableBatteries[13],
					min(config.Battery15.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery15.maxPower)*usableBatteries[14],
					min(config.Battery16.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery16.maxPower)*usableBatteries[15],
					min(config.Battery17.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery17.maxPower)*usableBatteries[16],
					min(config.Battery18.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery18.maxPower)*usableBatteries[17],
					min(config.Battery19.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery19.maxPower)*usableBatteries[18],
					min(config.Battery20.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery20.maxPower)*usableBatteries[19],
					min(config.Battery21.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery21.maxPower)*usableBatteries[20],
					min(config.Battery22.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery22.maxPower)*usableBatteries[21],
					min(config.Battery23.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery23.maxPower)*usableBatteries[22],
					min(config.Battery24.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery24.maxPower)*usableBatteries[23],
					min(config.Battery25.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery25.maxPower)*usableBatteries[24],
					min(config.Battery26.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery26.maxPower)*usableBatteries[25],
					min(config.Battery27.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery27.maxPower)*usableBatteries[26],
					min(config.Battery28.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery28.maxPower)*usableBatteries[27],
					min(config.Battery29.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery29.maxPower)*usableBatteries[28],
					min(config.Battery30.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery30.maxPower)*usableBatteries[29],
					min(config.Battery31.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery31.maxPower)*usableBatteries[30],
					min(config.Battery32.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery32.maxPower)*usableBatteries[31],
					min(config.Battery33.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery33.maxPower)*usableBatteries[32],
					min(config.Battery34.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery34.maxPower)*usableBatteries[33],
					min(config.Battery35.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery35.maxPower)*usableBatteries[34],
					min(config.Battery36.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery36.maxPower)*usableBatteries[35],
					min(config.Battery37.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery37.maxPower)*usableBatteries[36],
					min(config.Battery38.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery38.maxPower)*usableBatteries[37],
					min(config.Battery39.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery39.maxPower)*usableBatteries[38],
					min(config.Battery40.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery40.maxPower)*usableBatteries[39],
					min(config.Battery41.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery41.maxPower)*usableBatteries[40],
					min(config.Battery42.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery42.maxPower)*usableBatteries[41],
					min(config.Battery43.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery43.maxPower)*usableBatteries[42],
					min(config.Battery44.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery44.maxPower)*usableBatteries[43],
					min(config.Battery45.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery45.maxPower)*usableBatteries[44],
					min(config.Battery46.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery46.maxPower)*usableBatteries[45],
					min(config.Battery47.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery47.maxPower)*usableBatteries[46],
					min(config.Battery48.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery48.maxPower)*usableBatteries[47],
					min(config.Battery49.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery49.maxPower)*usableBatteries[48],
					min(config.Battery50.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery50.maxPower)*usableBatteries[49],

					min(config.Battery51.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery51.maxPower)*usableBatteries[50],
					min(config.Battery52.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery52.maxPower)*usableBatteries[51],
					min(config.Battery53.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery53.maxPower)*usableBatteries[52],
					min(config.Battery54.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery54.maxPower)*usableBatteries[53],
					min(config.Battery55.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery55.maxPower)*usableBatteries[54],
					min(config.Battery56.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery56.maxPower)*usableBatteries[55],
					min(config.Battery57.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery57.maxPower)*usableBatteries[56],
					min(config.Battery58.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery58.maxPower)*usableBatteries[57],
					min(config.Battery59.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery59.maxPower)*usableBatteries[58],
					min(config.Battery60.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery60.maxPower)*usableBatteries[59],
					min(config.Battery61.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery61.maxPower)*usableBatteries[60],
					min(config.Battery62.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery62.maxPower)*usableBatteries[61],
					min(config.Battery63.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery63.maxPower)*usableBatteries[62],
					min(config.Battery64.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery64.maxPower)*usableBatteries[63],
					min(config.Battery65.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery65.maxPower)*usableBatteries[64],
					min(config.Battery66.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery66.maxPower)*usableBatteries[65],
					min(config.Battery67.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery67.maxPower)*usableBatteries[66],
					min(config.Battery68.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery68.maxPower)*usableBatteries[67],
					min(config.Battery69.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery69.maxPower)*usableBatteries[68],
					min(config.Battery70.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery70.maxPower)*usableBatteries[69],
					min(config.Battery71.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery71.maxPower)*usableBatteries[70],
					min(config.Battery72.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery72.maxPower)*usableBatteries[71],
					min(config.Battery73.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery73.maxPower)*usableBatteries[72],
					min(config.Battery74.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery74.maxPower)*usableBatteries[73],
					min(config.Battery75.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery75.maxPower)*usableBatteries[74],
					min(config.Battery76.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery76.maxPower)*usableBatteries[75],
					min(config.Battery77.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery77.maxPower)*usableBatteries[76],
					min(config.Battery78.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery78.maxPower)*usableBatteries[77],
					min(config.Battery79.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery79.maxPower)*usableBatteries[78],
					min(config.Battery80.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery80.maxPower)*usableBatteries[79],
					min(config.Battery81.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery81.maxPower)*usableBatteries[80],
					min(config.Battery82.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery82.maxPower)*usableBatteries[81],
					min(config.Battery83.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery83.maxPower)*usableBatteries[82],
					min(config.Battery84.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery84.maxPower)*usableBatteries[83],
					min(config.Battery85.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery85.maxPower)*usableBatteries[84],
					min(config.Battery86.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery86.maxPower)*usableBatteries[85],
					min(config.Battery87.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery87.maxPower)*usableBatteries[86],
					min(config.Battery88.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery88.maxPower)*usableBatteries[87],
					min(config.Battery89.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery89.maxPower)*usableBatteries[88],
					min(config.Battery90.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery90.maxPower)*usableBatteries[89],
					min(config.Battery91.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery91.maxPower)*usableBatteries[90],
					min(config.Battery92.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery92.maxPower)*usableBatteries[91],
					min(config.Battery93.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery93.maxPower)*usableBatteries[92],
					min(config.Battery94.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery94.maxPower)*usableBatteries[93],
					min(config.Battery95.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery95.maxPower)*usableBatteries[94],
					min(config.Battery96.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery96.maxPower)*usableBatteries[95],
					min(config.Battery97.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery97.maxPower)*usableBatteries[96],
					min(config.Battery98.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery98.maxPower)*usableBatteries[97],
					min(config.Battery99.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery99.maxPower)*usableBatteries[98],
					min(config.Battery100.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery100.maxPower)*usableBatteries[99]]
					
	
	# use 2x the power request
	if sum(powerCapacity) > 2*config.AGGREGATOR_POWER_REQUEST:
		print("Batteries can meet 2x the Aggregator's power request.")
		return 1
	else:
		print("Batteries CANNOT meet 2x the Aggregator's power request.")
		return 0 



def getCurrentTimeStamp():

	dateTimeNow = str(datetime.now())
	dateTimeNow = re.sub(r"[.\/: ]","-",dateTimeNow)
	return dateTimeNow[:-7]



#retrieve load data from input file
def getUpdatedLoad(inputFile,iterationValue):
	

	config.Load1.loadValue = inputFile.loc[iterationValue][2]*config.LOAD_SCALING_FACTOR
	config.Load2.loadValue = inputFile.loc[iterationValue][3]*config.LOAD_SCALING_FACTOR
	config.Load3.loadValue = inputFile.loc[iterationValue][4]*config.LOAD_SCALING_FACTOR
	config.Load4.loadValue = inputFile.loc[iterationValue][5]*config.LOAD_SCALING_FACTOR
	config.Load5.loadValue = inputFile.loc[iterationValue][6]*config.LOAD_SCALING_FACTOR
	config.Load6.loadValue = inputFile.loc[iterationValue][7]*config.LOAD_SCALING_FACTOR
	config.Load7.loadValue = inputFile.loc[iterationValue][8]*config.LOAD_SCALING_FACTOR
	config.Load8.loadValue = inputFile.loc[iterationValue][9]*config.LOAD_SCALING_FACTOR
	config.Load9.loadValue = inputFile.loc[iterationValue][10]*config.LOAD_SCALING_FACTOR
	config.Load10.loadValue = inputFile.loc[iterationValue][11]*config.LOAD_SCALING_FACTOR
	config.Load11.loadValue = inputFile.loc[iterationValue][12]*config.LOAD_SCALING_FACTOR
	config.Load12.loadValue = inputFile.loc[iterationValue][13]*config.LOAD_SCALING_FACTOR
	config.Load13.loadValue = inputFile.loc[iterationValue][14]*config.LOAD_SCALING_FACTOR
	config.Load14.loadValue = inputFile.loc[iterationValue][15]*config.LOAD_SCALING_FACTOR
	config.Load15.loadValue = inputFile.loc[iterationValue][16]*config.LOAD_SCALING_FACTOR
	config.Load16.loadValue = inputFile.loc[iterationValue][17]*config.LOAD_SCALING_FACTOR
	config.Load17.loadValue = inputFile.loc[iterationValue][18]*config.LOAD_SCALING_FACTOR
	config.Load18.loadValue = inputFile.loc[iterationValue][19]*config.LOAD_SCALING_FACTOR
	config.Load19.loadValue = inputFile.loc[iterationValue][20]*config.LOAD_SCALING_FACTOR
	config.Load20.loadValue = inputFile.loc[iterationValue][21]*config.LOAD_SCALING_FACTOR
	config.Load21.loadValue = inputFile.loc[iterationValue][22]*config.LOAD_SCALING_FACTOR
	config.Load22.loadValue = inputFile.loc[iterationValue][23]*config.LOAD_SCALING_FACTOR
	config.Load23.loadValue = inputFile.loc[iterationValue][24]*config.LOAD_SCALING_FACTOR
	config.Load24.loadValue = inputFile.loc[iterationValue][25]*config.LOAD_SCALING_FACTOR
	config.Load25.loadValue = inputFile.loc[iterationValue][26]*config.LOAD_SCALING_FACTOR
	config.Load26.loadValue = inputFile.loc[iterationValue][27]*config.LOAD_SCALING_FACTOR
	config.Load27.loadValue = inputFile.loc[iterationValue][28]*config.LOAD_SCALING_FACTOR
	config.Load28.loadValue = inputFile.loc[iterationValue][29]*config.LOAD_SCALING_FACTOR
	config.Load29.loadValue = inputFile.loc[iterationValue][30]*config.LOAD_SCALING_FACTOR
	config.Load30.loadValue = inputFile.loc[iterationValue][31]*config.LOAD_SCALING_FACTOR
	config.Load31.loadValue = inputFile.loc[iterationValue][32]*config.LOAD_SCALING_FACTOR
	config.Load32.loadValue = inputFile.loc[iterationValue][33]*config.LOAD_SCALING_FACTOR
	config.Load33.loadValue = inputFile.loc[iterationValue][34]*config.LOAD_SCALING_FACTOR
	config.Load34.loadValue = inputFile.loc[iterationValue][35]*config.LOAD_SCALING_FACTOR
	config.Load35.loadValue = inputFile.loc[iterationValue][36]*config.LOAD_SCALING_FACTOR
	config.Load36.loadValue = inputFile.loc[iterationValue][37]*config.LOAD_SCALING_FACTOR
	config.Load37.loadValue = inputFile.loc[iterationValue][38]*config.LOAD_SCALING_FACTOR
	config.Load38.loadValue = inputFile.loc[iterationValue][39]*config.LOAD_SCALING_FACTOR
	config.Load39.loadValue = inputFile.loc[iterationValue][40]*config.LOAD_SCALING_FACTOR
	config.Load40.loadValue = inputFile.loc[iterationValue][41]*config.LOAD_SCALING_FACTOR
	config.Load41.loadValue = inputFile.loc[iterationValue][42]*config.LOAD_SCALING_FACTOR
	config.Load42.loadValue = inputFile.loc[iterationValue][43]*config.LOAD_SCALING_FACTOR
	config.Load43.loadValue = inputFile.loc[iterationValue][44]*config.LOAD_SCALING_FACTOR
	config.Load44.loadValue = inputFile.loc[iterationValue][45]*config.LOAD_SCALING_FACTOR
	config.Load45.loadValue = inputFile.loc[iterationValue][46]*config.LOAD_SCALING_FACTOR
	config.Load46.loadValue = inputFile.loc[iterationValue][47]*config.LOAD_SCALING_FACTOR
	config.Load47.loadValue = inputFile.loc[iterationValue][48]*config.LOAD_SCALING_FACTOR
	config.Load48.loadValue = inputFile.loc[iterationValue][49]*config.LOAD_SCALING_FACTOR
	config.Load49.loadValue = inputFile.loc[iterationValue][50]*config.LOAD_SCALING_FACTOR
	config.Load50.loadValue = inputFile.loc[iterationValue][51]*config.LOAD_SCALING_FACTOR

	config.Load51.loadValue = inputFile.loc[iterationValue][52]*config.LOAD_SCALING_FACTOR
	config.Load52.loadValue = inputFile.loc[iterationValue][53]*config.LOAD_SCALING_FACTOR
	config.Load53.loadValue = inputFile.loc[iterationValue][54]*config.LOAD_SCALING_FACTOR
	config.Load54.loadValue = inputFile.loc[iterationValue][55]*config.LOAD_SCALING_FACTOR
	config.Load55.loadValue = inputFile.loc[iterationValue][56]*config.LOAD_SCALING_FACTOR
	config.Load56.loadValue = inputFile.loc[iterationValue][57]*config.LOAD_SCALING_FACTOR
	config.Load57.loadValue = inputFile.loc[iterationValue][58]*config.LOAD_SCALING_FACTOR
	config.Load58.loadValue = inputFile.loc[iterationValue][59]*config.LOAD_SCALING_FACTOR
	config.Load59.loadValue = inputFile.loc[iterationValue][60]*config.LOAD_SCALING_FACTOR
	config.Load60.loadValue = inputFile.loc[iterationValue][61]*config.LOAD_SCALING_FACTOR
	config.Load61.loadValue = inputFile.loc[iterationValue][62]*config.LOAD_SCALING_FACTOR
	config.Load62.loadValue = inputFile.loc[iterationValue][63]*config.LOAD_SCALING_FACTOR
	config.Load63.loadValue = inputFile.loc[iterationValue][64]*config.LOAD_SCALING_FACTOR
	config.Load64.loadValue = inputFile.loc[iterationValue][65]*config.LOAD_SCALING_FACTOR
	config.Load65.loadValue = inputFile.loc[iterationValue][66]*config.LOAD_SCALING_FACTOR
	config.Load66.loadValue = inputFile.loc[iterationValue][67]*config.LOAD_SCALING_FACTOR
	config.Load67.loadValue = inputFile.loc[iterationValue][68]*config.LOAD_SCALING_FACTOR
	config.Load68.loadValue = inputFile.loc[iterationValue][69]*config.LOAD_SCALING_FACTOR
	config.Load69.loadValue = inputFile.loc[iterationValue][70]*config.LOAD_SCALING_FACTOR
	config.Load70.loadValue = inputFile.loc[iterationValue][71]*config.LOAD_SCALING_FACTOR
	config.Load71.loadValue = inputFile.loc[iterationValue][72]*config.LOAD_SCALING_FACTOR
	config.Load72.loadValue = inputFile.loc[iterationValue][73]*config.LOAD_SCALING_FACTOR
	config.Load73.loadValue = inputFile.loc[iterationValue][74]*config.LOAD_SCALING_FACTOR
	config.Load74.loadValue = inputFile.loc[iterationValue][75]*config.LOAD_SCALING_FACTOR
	config.Load75.loadValue = inputFile.loc[iterationValue][76]*config.LOAD_SCALING_FACTOR
	config.Load76.loadValue = inputFile.loc[iterationValue][77]*config.LOAD_SCALING_FACTOR
	config.Load77.loadValue = inputFile.loc[iterationValue][78]*config.LOAD_SCALING_FACTOR
	config.Load78.loadValue = inputFile.loc[iterationValue][79]*config.LOAD_SCALING_FACTOR
	config.Load79.loadValue = inputFile.loc[iterationValue][80]*config.LOAD_SCALING_FACTOR
	config.Load80.loadValue = inputFile.loc[iterationValue][81]*config.LOAD_SCALING_FACTOR
	config.Load81.loadValue = inputFile.loc[iterationValue][82]*config.LOAD_SCALING_FACTOR
	config.Load82.loadValue = inputFile.loc[iterationValue][83]*config.LOAD_SCALING_FACTOR
	config.Load83.loadValue = inputFile.loc[iterationValue][84]*config.LOAD_SCALING_FACTOR
	config.Load84.loadValue = inputFile.loc[iterationValue][85]*config.LOAD_SCALING_FACTOR
	config.Load85.loadValue = inputFile.loc[iterationValue][86]*config.LOAD_SCALING_FACTOR
	config.Load86.loadValue = inputFile.loc[iterationValue][87]*config.LOAD_SCALING_FACTOR
	config.Load87.loadValue = inputFile.loc[iterationValue][88]*config.LOAD_SCALING_FACTOR
	config.Load88.loadValue = inputFile.loc[iterationValue][89]*config.LOAD_SCALING_FACTOR
	config.Load89.loadValue = inputFile.loc[iterationValue][90]*config.LOAD_SCALING_FACTOR
	config.Load90.loadValue = inputFile.loc[iterationValue][91]*config.LOAD_SCALING_FACTOR
	config.Load91.loadValue = inputFile.loc[iterationValue][92]*config.LOAD_SCALING_FACTOR
	config.Load92.loadValue = inputFile.loc[iterationValue][93]*config.LOAD_SCALING_FACTOR
	config.Load93.loadValue = inputFile.loc[iterationValue][94]*config.LOAD_SCALING_FACTOR
	config.Load94.loadValue = inputFile.loc[iterationValue][95]*config.LOAD_SCALING_FACTOR
	config.Load95.loadValue = inputFile.loc[iterationValue][96]*config.LOAD_SCALING_FACTOR
	config.Load96.loadValue = inputFile.loc[iterationValue][97]*config.LOAD_SCALING_FACTOR
	config.Load97.loadValue = inputFile.loc[iterationValue][98]*config.LOAD_SCALING_FACTOR
	config.Load98.loadValue = inputFile.loc[iterationValue][99]*config.LOAD_SCALING_FACTOR
	config.Load99.loadValue = inputFile.loc[iterationValue][100]*config.LOAD_SCALING_FACTOR
	config.Load100.loadValue = inputFile.loc[iterationValue][101]*config.LOAD_SCALING_FACTOR
	
	TOTAL_LOAD = getTotalLoad()

	print("Total Load: ",TOTAL_LOAD)




# a function to randomize the battery sell prices
def randomizePrices():

	maxSellPrice = .3
	config.Battery1.sellPrice = np.random.rand()*maxSellPrice
	config.Battery2.sellPrice = np.random.rand()*maxSellPrice
	config.Battery3.sellPrice = np.random.rand()*maxSellPrice
	config.Battery4.sellPrice = np.random.rand()*maxSellPrice
	config.Battery5.sellPrice = np.random.rand()*maxSellPrice
	config.Battery6.sellPrice = np.random.rand()*maxSellPrice
	config.Battery7.sellPrice = np.random.rand()*maxSellPrice
	config.Battery8.sellPrice = np.random.rand()*maxSellPrice
	config.Battery9.sellPrice = np.random.rand()*maxSellPrice
	config.Battery10.sellPrice = np.random.rand()*maxSellPrice
	config.Battery11.sellPrice = np.random.rand()*maxSellPrice
	config.Battery12.sellPrice = np.random.rand()*maxSellPrice
	config.Battery13.sellPrice = np.random.rand()*maxSellPrice
	config.Battery14.sellPrice = np.random.rand()*maxSellPrice
	config.Battery15.sellPrice = np.random.rand()*maxSellPrice
	config.Battery16.sellPrice = np.random.rand()*maxSellPrice
	config.Battery17.sellPrice = np.random.rand()*maxSellPrice
	config.Battery18.sellPrice = np.random.rand()*maxSellPrice
	config.Battery19.sellPrice = np.random.rand()*maxSellPrice
	config.Battery20.sellPrice = np.random.rand()*maxSellPrice
	config.Battery21.sellPrice = np.random.rand()*maxSellPrice
	config.Battery22.sellPrice = np.random.rand()*maxSellPrice
	config.Battery23.sellPrice = np.random.rand()*maxSellPrice
	config.Battery24.sellPrice = np.random.rand()*maxSellPrice
	config.Battery25.sellPrice = np.random.rand()*maxSellPrice
	config.Battery26.sellPrice = np.random.rand()*maxSellPrice
	config.Battery27.sellPrice = np.random.rand()*maxSellPrice
	config.Battery28.sellPrice = np.random.rand()*maxSellPrice
	config.Battery29.sellPrice = np.random.rand()*maxSellPrice
	config.Battery30.sellPrice = np.random.rand()*maxSellPrice
	config.Battery31.sellPrice = np.random.rand()*maxSellPrice
	config.Battery32.sellPrice = np.random.rand()*maxSellPrice
	config.Battery33.sellPrice = np.random.rand()*maxSellPrice
	config.Battery34.sellPrice = np.random.rand()*maxSellPrice
	config.Battery35.sellPrice = np.random.rand()*maxSellPrice
	config.Battery36.sellPrice = np.random.rand()*maxSellPrice
	config.Battery37.sellPrice = np.random.rand()*maxSellPrice
	config.Battery38.sellPrice = np.random.rand()*maxSellPrice
	config.Battery39.sellPrice = np.random.rand()*maxSellPrice
	config.Battery40.sellPrice = np.random.rand()*maxSellPrice
	config.Battery41.sellPrice = np.random.rand()*maxSellPrice
	config.Battery42.sellPrice = np.random.rand()*maxSellPrice
	config.Battery43.sellPrice = np.random.rand()*maxSellPrice
	config.Battery44.sellPrice = np.random.rand()*maxSellPrice
	config.Battery45.sellPrice = np.random.rand()*maxSellPrice
	config.Battery46.sellPrice = np.random.rand()*maxSellPrice
	config.Battery47.sellPrice = np.random.rand()*maxSellPrice
	config.Battery48.sellPrice = np.random.rand()*maxSellPrice
	config.Battery49.sellPrice = np.random.rand()*maxSellPrice
	config.Battery50.sellPrice = np.random.rand()*maxSellPrice

	config.Battery51.sellPrice = np.random.rand()*maxSellPrice
	config.Battery52.sellPrice = np.random.rand()*maxSellPrice
	config.Battery53.sellPrice = np.random.rand()*maxSellPrice
	config.Battery54.sellPrice = np.random.rand()*maxSellPrice
	config.Battery55.sellPrice = np.random.rand()*maxSellPrice
	config.Battery56.sellPrice = np.random.rand()*maxSellPrice
	config.Battery57.sellPrice = np.random.rand()*maxSellPrice
	config.Battery58.sellPrice = np.random.rand()*maxSellPrice
	config.Battery59.sellPrice = np.random.rand()*maxSellPrice
	config.Battery60.sellPrice = np.random.rand()*maxSellPrice
	config.Battery61.sellPrice = np.random.rand()*maxSellPrice
	config.Battery62.sellPrice = np.random.rand()*maxSellPrice
	config.Battery63.sellPrice = np.random.rand()*maxSellPrice
	config.Battery64.sellPrice = np.random.rand()*maxSellPrice
	config.Battery65.sellPrice = np.random.rand()*maxSellPrice
	config.Battery66.sellPrice = np.random.rand()*maxSellPrice
	config.Battery67.sellPrice = np.random.rand()*maxSellPrice
	config.Battery68.sellPrice = np.random.rand()*maxSellPrice
	config.Battery69.sellPrice = np.random.rand()*maxSellPrice
	config.Battery70.sellPrice = np.random.rand()*maxSellPrice
	config.Battery71.sellPrice = np.random.rand()*maxSellPrice
	config.Battery72.sellPrice = np.random.rand()*maxSellPrice
	config.Battery73.sellPrice = np.random.rand()*maxSellPrice
	config.Battery74.sellPrice = np.random.rand()*maxSellPrice
	config.Battery75.sellPrice = np.random.rand()*maxSellPrice
	config.Battery76.sellPrice = np.random.rand()*maxSellPrice
	config.Battery77.sellPrice = np.random.rand()*maxSellPrice
	config.Battery78.sellPrice = np.random.rand()*maxSellPrice
	config.Battery79.sellPrice = np.random.rand()*maxSellPrice
	config.Battery80.sellPrice = np.random.rand()*maxSellPrice
	config.Battery81.sellPrice = np.random.rand()*maxSellPrice
	config.Battery82.sellPrice = np.random.rand()*maxSellPrice
	config.Battery83.sellPrice = np.random.rand()*maxSellPrice
	config.Battery84.sellPrice = np.random.rand()*maxSellPrice
	config.Battery85.sellPrice = np.random.rand()*maxSellPrice
	config.Battery86.sellPrice = np.random.rand()*maxSellPrice
	config.Battery87.sellPrice = np.random.rand()*maxSellPrice
	config.Battery88.sellPrice = np.random.rand()*maxSellPrice
	config.Battery89.sellPrice = np.random.rand()*maxSellPrice
	config.Battery90.sellPrice = np.random.rand()*maxSellPrice
	config.Battery91.sellPrice = np.random.rand()*maxSellPrice
	config.Battery92.sellPrice = np.random.rand()*maxSellPrice
	config.Battery93.sellPrice = np.random.rand()*maxSellPrice
	config.Battery94.sellPrice = np.random.rand()*maxSellPrice
	config.Battery95.sellPrice = np.random.rand()*maxSellPrice
	config.Battery96.sellPrice = np.random.rand()*maxSellPrice
	config.Battery97.sellPrice = np.random.rand()*maxSellPrice
	config.Battery98.sellPrice = np.random.rand()*maxSellPrice
	config.Battery99.sellPrice = np.random.rand()*maxSellPrice
	config.Battery100.sellPrice = np.random.rand()*maxSellPrice


#resets the simulation parameters to original values for iterative simulations
def resetSimulation():

	config.BUY_PRICE = .01
	config.PRICE_STEP = .01
	config.MIN_CHARGE_PERCENTAGE = 0.3
	config.MAX_CHARGE_PERCENTAGE = 0.8
	config.MAX_BAT_POWER_FLOW = 3000
	config.STOP = 0;
	config.NET_FLOW = 0
	config.NODE_QUANTITY = 100
	config.FIVE_MINUTE_SCALING_FACTOR = 5/60

	config.Battery1.chargeState = 10000
	config.Battery2.chargeState = 10000
	config.Battery3.chargeState = 10000
	config.Battery4.chargeState = 10000
	config.Battery5.chargeState = 10000
	config.Battery6.chargeState = 10000
	config.Battery7.chargeState = 10000
	config.Battery8.chargeState = 10000
	config.Battery9.chargeState = 10000
	config.Battery10.chargeState = 10000
	config.Battery11.chargeState = 10000
	config.Battery12.chargeState = 10000
	config.Battery13.chargeState = 10000
	config.Battery14.chargeState = 10000
	config.Battery15.chargeState = 10000
	config.Battery16.chargeState = 10000
	config.Battery17.chargeState = 10000
	config.Battery18.chargeState = 10000
	config.Battery19.chargeState = 10000
	config.Battery20.chargeState = 10000
	config.Battery21.chargeState = 10000
	config.Battery22.chargeState = 10000
	config.Battery23.chargeState = 10000
	config.Battery24.chargeState = 10000
	config.Battery25.chargeState = 10000
	config.Battery26.chargeState = 10000
	config.Battery27.chargeState = 10000
	config.Battery28.chargeState = 10000
	config.Battery29.chargeState = 10000
	config.Battery30.chargeState = 10000
	config.Battery31.chargeState = 10000
	config.Battery32.chargeState = 10000
	config.Battery33.chargeState = 10000
	config.Battery34.chargeState = 10000
	config.Battery35.chargeState = 10000
	config.Battery36.chargeState = 10000
	config.Battery37.chargeState = 10000
	config.Battery38.chargeState = 10000
	config.Battery39.chargeState = 10000
	config.Battery40.chargeState = 10000
	config.Battery41.chargeState = 10000
	config.Battery42.chargeState = 10000
	config.Battery43.chargeState = 10000
	config.Battery44.chargeState = 10000
	config.Battery45.chargeState = 10000
	config.Battery46.chargeState = 10000
	config.Battery47.chargeState = 10000
	config.Battery48.chargeState = 10000
	config.Battery49.chargeState = 10000
	config.Battery50.chargeState = 10000

	config.Battery51.chargeState = 10000
	config.Battery52.chargeState = 10000
	config.Battery53.chargeState = 10000
	config.Battery54.chargeState = 10000
	config.Battery55.chargeState = 10000
	config.Battery56.chargeState = 10000
	config.Battery57.chargeState = 10000
	config.Battery58.chargeState = 10000
	config.Battery59.chargeState = 10000
	config.Battery60.chargeState = 10000
	config.Battery61.chargeState = 10000
	config.Battery62.chargeState = 10000
	config.Battery63.chargeState = 10000
	config.Battery64.chargeState = 10000
	config.Battery65.chargeState = 10000
	config.Battery66.chargeState = 10000
	config.Battery67.chargeState = 10000
	config.Battery68.chargeState = 10000
	config.Battery69.chargeState = 10000
	config.Battery70.chargeState = 10000
	config.Battery71.chargeState = 10000
	config.Battery72.chargeState = 10000
	config.Battery73.chargeState = 10000
	config.Battery74.chargeState = 10000
	config.Battery75.chargeState = 10000
	config.Battery76.chargeState = 10000
	config.Battery77.chargeState = 10000
	config.Battery78.chargeState = 10000
	config.Battery79.chargeState = 10000
	config.Battery80.chargeState = 10000
	config.Battery81.chargeState = 10000
	config.Battery82.chargeState = 10000
	config.Battery83.chargeState = 10000
	config.Battery84.chargeState = 10000
	config.Battery85.chargeState = 10000
	config.Battery86.chargeState = 10000
	config.Battery87.chargeState = 10000
	config.Battery88.chargeState = 10000
	config.Battery89.chargeState = 10000
	config.Battery90.chargeState = 10000
	config.Battery91.chargeState = 10000
	config.Battery92.chargeState = 10000
	config.Battery93.chargeState = 10000
	config.Battery94.chargeState = 10000
	config.Battery95.chargeState = 10000
	config.Battery96.chargeState = 10000
	config.Battery97.chargeState = 10000
	config.Battery98.chargeState = 10000
	config.Battery99.chargeState = 10000
	config.Battery100.chargeState = 10000




def getBatteryChargePercentages():

		getBatteryChargePercentages = [(config.Battery1.chargeState/config.Battery1.capacity),
										(config.Battery2.chargeState/config.Battery2.capacity),
										(config.Battery3.chargeState/config.Battery3.capacity),
										(config.Battery4.chargeState/config.Battery4.capacity),
										(config.Battery5.chargeState/config.Battery5.capacity),
										(config.Battery6.chargeState/config.Battery6.capacity),
										(config.Battery7.chargeState/config.Battery7.capacity),
										(config.Battery8.chargeState/config.Battery8.capacity),
										(config.Battery9.chargeState/config.Battery9.capacity),
										(config.Battery10.chargeState/config.Battery10.capacity),
										(config.Battery11.chargeState/config.Battery11.capacity),
										(config.Battery12.chargeState/config.Battery12.capacity),
										(config.Battery13.chargeState/config.Battery13.capacity),
										(config.Battery14.chargeState/config.Battery14.capacity),
										(config.Battery15.chargeState/config.Battery15.capacity),
										(config.Battery16.chargeState/config.Battery16.capacity),
										(config.Battery17.chargeState/config.Battery17.capacity),
										(config.Battery18.chargeState/config.Battery18.capacity),
										(config.Battery19.chargeState/config.Battery19.capacity),
										(config.Battery20.chargeState/config.Battery20.capacity),
										(config.Battery21.chargeState/config.Battery21.capacity),
										(config.Battery22.chargeState/config.Battery22.capacity),
										(config.Battery23.chargeState/config.Battery23.capacity),
										(config.Battery24.chargeState/config.Battery24.capacity),
										(config.Battery25.chargeState/config.Battery25.capacity),
										(config.Battery26.chargeState/config.Battery26.capacity),
										(config.Battery27.chargeState/config.Battery27.capacity),
										(config.Battery28.chargeState/config.Battery28.capacity),
										(config.Battery29.chargeState/config.Battery29.capacity),
										(config.Battery30.chargeState/config.Battery30.capacity),
										(config.Battery31.chargeState/config.Battery31.capacity),
										(config.Battery32.chargeState/config.Battery32.capacity),
										(config.Battery33.chargeState/config.Battery33.capacity),
										(config.Battery34.chargeState/config.Battery34.capacity),
										(config.Battery35.chargeState/config.Battery35.capacity),
										(config.Battery36.chargeState/config.Battery36.capacity),
										(config.Battery37.chargeState/config.Battery37.capacity),
										(config.Battery38.chargeState/config.Battery38.capacity),
										(config.Battery39.chargeState/config.Battery39.capacity),
										(config.Battery40.chargeState/config.Battery40.capacity),
										(config.Battery41.chargeState/config.Battery41.capacity),
										(config.Battery42.chargeState/config.Battery42.capacity),
										(config.Battery43.chargeState/config.Battery43.capacity),
										(config.Battery44.chargeState/config.Battery44.capacity),
										(config.Battery45.chargeState/config.Battery45.capacity),
										(config.Battery46.chargeState/config.Battery46.capacity),
										(config.Battery47.chargeState/config.Battery47.capacity),
										(config.Battery48.chargeState/config.Battery48.capacity),
										(config.Battery49.chargeState/config.Battery49.capacity),
										(config.Battery50.chargeState/config.Battery50.capacity),

										(config.Battery51.chargeState/config.Battery51.capacity),
										(config.Battery52.chargeState/config.Battery52.capacity),
										(config.Battery53.chargeState/config.Battery53.capacity),
										(config.Battery54.chargeState/config.Battery54.capacity),
										(config.Battery55.chargeState/config.Battery55.capacity),
										(config.Battery56.chargeState/config.Battery56.capacity),
										(config.Battery57.chargeState/config.Battery57.capacity),
										(config.Battery58.chargeState/config.Battery58.capacity),
										(config.Battery59.chargeState/config.Battery59.capacity),
										(config.Battery60.chargeState/config.Battery60.capacity),
										(config.Battery61.chargeState/config.Battery61.capacity),
										(config.Battery62.chargeState/config.Battery62.capacity),
										(config.Battery63.chargeState/config.Battery63.capacity),
										(config.Battery64.chargeState/config.Battery64.capacity),
										(config.Battery65.chargeState/config.Battery65.capacity),
										(config.Battery66.chargeState/config.Battery66.capacity),
										(config.Battery67.chargeState/config.Battery67.capacity),
										(config.Battery68.chargeState/config.Battery68.capacity),
										(config.Battery69.chargeState/config.Battery69.capacity),
										(config.Battery70.chargeState/config.Battery70.capacity),
										(config.Battery71.chargeState/config.Battery71.capacity),
										(config.Battery72.chargeState/config.Battery72.capacity),
										(config.Battery73.chargeState/config.Battery73.capacity),
										(config.Battery74.chargeState/config.Battery74.capacity),
										(config.Battery75.chargeState/config.Battery75.capacity),
										(config.Battery76.chargeState/config.Battery76.capacity),
										(config.Battery77.chargeState/config.Battery77.capacity),
										(config.Battery78.chargeState/config.Battery78.capacity),
										(config.Battery79.chargeState/config.Battery79.capacity),
										(config.Battery80.chargeState/config.Battery80.capacity),
										(config.Battery81.chargeState/config.Battery81.capacity),
										(config.Battery82.chargeState/config.Battery82.capacity),
										(config.Battery83.chargeState/config.Battery83.capacity),
										(config.Battery84.chargeState/config.Battery84.capacity),
										(config.Battery85.chargeState/config.Battery85.capacity),
										(config.Battery86.chargeState/config.Battery86.capacity),
										(config.Battery87.chargeState/config.Battery87.capacity),
										(config.Battery88.chargeState/config.Battery88.capacity),
										(config.Battery89.chargeState/config.Battery89.capacity),
										(config.Battery90.chargeState/config.Battery90.capacity),
										(config.Battery91.chargeState/config.Battery91.capacity),
										(config.Battery92.chargeState/config.Battery92.capacity),
										(config.Battery93.chargeState/config.Battery93.capacity),
										(config.Battery94.chargeState/config.Battery94.capacity),
										(config.Battery95.chargeState/config.Battery95.capacity),
										(config.Battery96.chargeState/config.Battery96.capacity),
										(config.Battery97.chargeState/config.Battery97.capacity),
										(config.Battery98.chargeState/config.Battery98.capacity),
										(config.Battery99.chargeState/config.Battery99.capacity),
										(config.Battery100.chargeState/config.Battery100.capacity)]
		return getBatteryChargePercentages


'''
			(config.Battery12.minPower,config.Battery12.maxPower),
			(config.Battery13.minPower,config.Battery13.maxPower),
			(config.Battery14.minPower,config.Battery14.maxPower),
			(config.Battery15.minPower,config.Battery15.maxPower),
			(config.Battery16.minPower,config.Battery16.maxPower),
			(config.Battery17.minPower,config.Battery17.maxPower),
			(config.Battery18.minPower,config.Battery18.maxPower),
			(config.Battery19.minPower,config.Battery19.maxPower),
			(config.Battery20.minPower,config.Battery20.maxPower),
			(config.Battery21.minPower,config.Battery21.maxPower),
			(config.Battery22.minPower,config.Battery22.maxPower),
			(config.Battery23.minPower,config.Battery23.maxPower),
			(config.Battery24.minPower,config.Battery24.maxPower),
			(config.Battery25.minPower,config.Battery25.maxPower),
			(config.Battery26.minPower,config.Battery26.maxPower),
			(config.Battery27.minPower,config.Battery27.maxPower),
			(config.Battery28.minPower,config.Battery28.maxPower),
			(config.Battery29.minPower,config.Battery29.maxPower),
			(config.Battery30.minPower,config.Battery30.maxPower),
			(config.Battery31.minPower,config.Battery31.maxPower),
			(config.Battery32.minPower,config.Battery32.maxPower),
			(config.Battery33.minPower,config.Battery33.maxPower),
			(config.Battery34.minPower,config.Battery34.maxPower),
			(config.Battery35.minPower,config.Battery35.maxPower),
			(config.Battery36.minPower,config.Battery36.maxPower),
			(config.Battery37.minPower,config.Battery37.maxPower),
			(config.Battery38.minPower,config.Battery38.maxPower),
			(config.Battery39.minPower,config.Battery39.maxPower),
			(config.Battery40.minPower,config.Battery40.maxPower),
			'''






'''
MIN AND MAX CHARGE CONSTRAINTS

{'type': 'ineq','fun': lambda x: 	(config.Battery1.chargeState - x[0]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery1.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery1.chargeState - x[0]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery1.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery2.chargeState - x[1]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery2.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery2.chargeState - x[1]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery2.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery3.chargeState - x[2]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery3.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery3.chargeState - x[2]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery3.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery4.chargeState - x[3]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery4.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery4.chargeState - x[3]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery4.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery5.chargeState - x[4]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery5.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery5.chargeState - x[4]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery5.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery6.chargeState - x[5]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery6.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery6.chargeState - x[5]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery6.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery7.chargeState - x[6]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery7.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery7.chargeState - x[6]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery7.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery8.chargeState - x[7]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery8.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery8.chargeState - x[7]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery8.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery9.chargeState - x[8]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery9.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery9.chargeState - x[8]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery9.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery10.chargeState - x[9]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery10.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery10.chargeState - x[9]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery10.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery11.chargeState - x[10]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery11.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery11.chargeState - x[10]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery11.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery12.chargeState - x[11]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery12.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery12.chargeState - x[11]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery12.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery13.chargeState - x[12]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery13.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery13.chargeState - x[12]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery13.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery14.chargeState - x[13]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery14.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery14.chargeState - x[13]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery14.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery15.chargeState - x[14]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery15.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery15.chargeState - x[14]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery15.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery16.chargeState - x[15]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery16.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery16.chargeState - x[15]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery16.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery17.chargeState - x[16]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery17.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery17.chargeState - x[16]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery17.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery18.chargeState - x[17]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery18.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery18.chargeState - x[17]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery18.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery19.chargeState - x[18]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery19.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery19.chargeState - x[18]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery19.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery20.chargeState - x[19]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery20.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery20.chargeState - x[19]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery20.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery21.chargeState - x[20]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery21.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery21.chargeState - x[20]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery21.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery22.chargeState - x[21]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery22.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery22.chargeState - x[21]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery22.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery23.chargeState - x[22]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery23.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery23.chargeState - x[22]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery23.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery24.chargeState - x[23]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery24.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery24.chargeState - x[23]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery24.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery25.chargeState - x[24]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery25.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery25.chargeState - x[24]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery25.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery26.chargeState - x[25]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery26.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery26.chargeState - x[25]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery26.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery27.chargeState - x[26]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery27.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery27.chargeState - x[26]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery27.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery28.chargeState - x[27]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery28.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery28.chargeState - x[27]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery28.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery29.chargeState - x[28]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery29.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery29.chargeState - x[28]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery29.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery30.chargeState - x[29]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery30.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery30.chargeState - x[29]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery30.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery31.chargeState - x[30]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery31.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery31.chargeState - x[30]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery31.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery32.chargeState - x[31]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery32.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery32.chargeState - x[31]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery32.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery33.chargeState - x[32]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery33.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery33.chargeState - x[32]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery33.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery34.chargeState - x[33]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery34.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery34.chargeState - x[33]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery34.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery35.chargeState - x[34]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery35.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery35.chargeState - x[34]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery35.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery36.chargeState - x[35]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery36.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery36.chargeState - x[35]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery36.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery37.chargeState - x[36]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery37.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery37.chargeState - x[36]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery37.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery38.chargeState - x[37]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery38.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery38.chargeState - x[37]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery38.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery39.chargeState - x[38]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery39.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery39.chargeState - x[38]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery39.capacity) + config.MAX_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: 	(config.Battery40.chargeState - x[39]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery40.capacity) - config.MIN_CHARGE_PERCENTAGE},
{'type': 'ineq','fun': lambda x: -1*(config.Battery40.chargeState - x[39]*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery40.capacity) + config.MAX_CHARGE_PERCENTAGE})
'''



'''
					config.Battery1.sellPrice, 
					config.Battery2.sellPrice, 
					config.Battery3.sellPrice,
					config.Battery4.sellPrice,
					config.Battery5.sellPrice,
					config.Battery6.sellPrice,
					config.Battery7.sellPrice,
					config.Battery8.sellPrice,
					config.Battery9.sellPrice,
					config.Battery10.sellPrice,
					config.Battery11.sellPrice,
					config.Battery12.sellPrice,
					config.Battery13.sellPrice,
					config.Battery14.sellPrice,
					config.Battery15.sellPrice,
					config.Battery16.sellPrice,
					config.Battery17.sellPrice,
					config.Battery18.sellPrice,
					config.Battery19.sellPrice,
					config.Battery20.sellPrice,
					config.Battery21.sellPrice,
					config.Battery22.sellPrice,
					config.Battery23.sellPrice,
					config.Battery24.sellPrice,
					config.Battery25.sellPrice,
					config.Battery26.sellPrice,
					config.Battery27.sellPrice,
					config.Battery28.sellPrice,
					config.Battery29.sellPrice,
					config.Battery30.sellPrice,
					config.Battery31.sellPrice,
					config.Battery32.sellPrice,
					config.Battery33.sellPrice,
					config.Battery34.sellPrice,
					config.Battery35.sellPrice,
					config.Battery36.sellPrice,
					config.Battery37.sellPrice,
					config.Battery38.sellPrice,
					config.Battery39.sellPrice,
					config.Battery40.sellPrice,
'''

