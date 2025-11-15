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
						config.Load46.loadValue,config.Load47.loadValue,config.Load48.loadValue,config.Load49.loadValue,config.Load50.loadValue])

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

			#voltage constraints
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[0],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[0],x[config.NODE_QUANTITY*2:]) - 2*(config.Line12.impedance*x[51]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[1],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[1],x[config.NODE_QUANTITY*2:]) - 2*(config.Line23.impedance*x[52]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[2],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[2],x[config.NODE_QUANTITY*2:]) - 2*(config.Line14.impedance*x[53]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[3],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[3],x[config.NODE_QUANTITY*2:]) - 2*(config.Line45.impedance*x[54]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[4],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[4],x[config.NODE_QUANTITY*2:]) - 2*(config.Line56.impedance*x[55]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[5],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[5],x[config.NODE_QUANTITY*2:]) - 2*(config.Line17.impedance*x[56]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[6],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[6],x[config.NODE_QUANTITY*2:]) - 2*(config.Line78.impedance*x[57]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[7],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[7],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[58]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[8],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[8],x[config.NODE_QUANTITY*2:]) - 2*(config.Line9x10.impedance*x[59]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[9],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[9],x[config.NODE_QUANTITY*2:]) - 2*(config.Line10x11.impedance*x[60]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[10],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[10],x[config.NODE_QUANTITY*2:]) - 2*(config.Line11x12.impedance*x[61]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[11],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[11],x[config.NODE_QUANTITY*2:]) - 2*(config.Line12x13.impedance*x[62]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[12],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[12],x[config.NODE_QUANTITY*2:]) - 2*(config.Line14.impedance*x[63]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[13],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[13],x[config.NODE_QUANTITY*2:]) - 2*(config.Line45.impedance*x[64]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[14],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[14],x[config.NODE_QUANTITY*2:]) - 2*(config.Line56.impedance*x[65]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[15],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[15],x[config.NODE_QUANTITY*2:]) - 2*(config.Line17.impedance*x[66]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[16],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[16],x[config.NODE_QUANTITY*2:]) - 2*(config.Line78.impedance*x[67]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[17],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[17],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[68]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[18],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[18],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[69]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[19],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[19],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[70]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[20],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[20],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[71]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[21],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[21],x[config.NODE_QUANTITY*2:]) - 2*(config.Line23.impedance*x[72]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[22],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[22],x[config.NODE_QUANTITY*2:]) - 2*(config.Line14.impedance*x[73]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[23],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[23],x[config.NODE_QUANTITY*2:]) - 2*(config.Line45.impedance*x[74]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[24],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[24],x[config.NODE_QUANTITY*2:]) - 2*(config.Line56.impedance*x[75]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[25],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[25],x[config.NODE_QUANTITY*2:]) - 2*(config.Line17.impedance*x[76]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[26],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[26],x[config.NODE_QUANTITY*2:]) - 2*(config.Line78.impedance*x[77]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[27],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[27],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[78]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[28],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[28],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[79]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[29],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[29],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[80]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[30],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[30],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[81]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[31],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[31],x[config.NODE_QUANTITY*2:]) - 2*(config.Line23.impedance*x[82]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[32],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[32],x[config.NODE_QUANTITY*2:]) - 2*(config.Line14.impedance*x[83]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[33],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[33],x[config.NODE_QUANTITY*2:]) - 2*(config.Line45.impedance*x[84]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[34],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[34],x[config.NODE_QUANTITY*2:]) - 2*(config.Line56.impedance*x[85]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[35],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[35],x[config.NODE_QUANTITY*2:]) - 2*(config.Line17.impedance*x[86]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[36],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[36],x[config.NODE_QUANTITY*2:]) - 2*(config.Line78.impedance*x[87]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[37],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[37],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[88]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[38],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[38],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[89]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[39],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[39],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[90]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[40],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[40],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[91]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[41],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[41],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[92]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[42],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[42],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[93]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[43],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[43],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[94]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[44],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[44],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[95]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[45],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[45],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[96]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[46],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[46],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[97]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[47],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[47],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[98]).real},
			{'type': 'eq','fun': lambda x: np.matmul(config.voltageRelationshipMatrixOne[48],x[config.NODE_QUANTITY*2:])*np.matmul(config.voltageRelationshipMatrixTwo[48],x[config.NODE_QUANTITY*2:]) - 2*(config.Line89.impedance*x[99]).real},

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
			{'type': 'ineq','fun': lambda x: -1*(config.Battery50.chargeState - (x[49])*(config.FIVE_MINUTE_SCALING_FACTOR))/(config.Battery50.capacity) + config.MAX_CHARGE_PERCENTAGE})


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
			(config.Node50.minVoltage,config.Node50.maxVoltage))

	startTime = time.time()

	#this idea of writing this line came from the scipy minimize documentation (See "Examples" section): https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#rdd2e1855725e-12
	costFunctionNested = lambda x: costFunction(x, usableBatteries)


	optimalSolution = optimize.minimize(costFunctionNested,initialGuess,constraints=constraints,bounds=bounds,method='SLSQP') #method="trust-constr"
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
			int(config.Battery50.sellPrice <= buyPrice)])

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
		int(config.Battery50.chargeState/config.Battery50.capacity > config.MIN_CHARGE_PERCENTAGE)])

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
					min(config.Battery50.chargeState*(config.FIVE_MINUTE_SCALING_FACTOR),config.Battery50.maxPower)*usableBatteries[49]]
					
	
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


#resets the simulation parameters to original values for iterative simulations
def resetSimulation():

	config.BUY_PRICE = .01
	config.PRICE_STEP = .01
	config.MIN_CHARGE_PERCENTAGE = 0.3
	config.MAX_CHARGE_PERCENTAGE = 0.8
	config.MAX_BAT_POWER_FLOW = 3000
	config.STOP = 0;
	config.NET_FLOW = 0
	config.NODE_QUANTITY = 50
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
										(config.Battery50.chargeState/config.Battery50.capacity)]
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

