import pandas as pd

'''
SUMMARY: configuration file that declares classes and instances of objects used in this code base. Martices, constants, and
file paths are created here as well. 

NOTE: all parameter values (e.g. line impedances, battery capacity, etc.) are not final and need to be analyzed for accuracy. At this time during code development, consider all parameters as non-final values. 


UNITS: units used for all values unless stated otherwise:

	Voltage: volts
	Power: watts
	Power Flow: watts
	Energy: watt hours
	Impedance: Ohms

'''

# Classes
class Battery:

	def __init__(self,node,chargeState,sellPrice,maxPower,minPower,capacity):
		self.node = node
		self.chargeState = chargeState
		self.sellPrice = sellPrice
		self.maxPower = maxPower
		self.minPower = minPower
		self.capacity = capacity

class Node:

	def __init__(self,minVoltage,maxVoltage):
		self.minVoltage = minVoltage
		self.maxVoltage = maxVoltage

class Line:

	def __init__(self,startNode,endNode,impedance,maxPowerFlow,minPowerFlow):
		self.startNode = startNode
		self.endNode = endNode
		self.impedance = impedance
		self.maxPowerFlow = maxPowerFlow
		self.minPowerFlow = minPowerFlow

class Load:
	def __init__(self,node,loadValue):
		self.node = node
		self.loadValue = loadValue



# Constants
BUY_PRICE = .01
PRICE_STEP = .01
MIN_CHARGE_PERCENTAGE = 0.3
MAX_CHARGE_PERCENTAGE = 0.8
MAX_BAT_POWER_FLOW = 3000
STOP = 0;
NET_FLOW = 0
NODE_QUANTITY = 50
FIVE_MINUTE_SCALING_FACTOR = 5/60

AGGREGATOR_POWER_REQUEST = 8000 #8000
LOAD_SCALING_FACTOR = .1


# Battery Instances
Battery1 = Battery(node=1, chargeState=10000, sellPrice=.05, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500) 
Battery2 = Battery(node=2, chargeState=10000, sellPrice=.03, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery3 = Battery(node=3, chargeState=10000, sellPrice=.05, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery4 = Battery(node=4, chargeState=10000, sellPrice=.97, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery5 = Battery(node=5, chargeState=10000, sellPrice=.01, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery6 = Battery(node=6, chargeState=10000, sellPrice=.02, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery7 = Battery(node=7, chargeState=10000, sellPrice=.03, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery8 = Battery(node=8, chargeState=10000, sellPrice=.04, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery9 = Battery(node=9, chargeState=10000, sellPrice=.01, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery10 = Battery(node=10, chargeState=10000, sellPrice=.11, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery11 = Battery(node=11, chargeState=10000, sellPrice=.21, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery12 = Battery(node=12, chargeState=10000, sellPrice=.15, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery13 = Battery(node=13, chargeState=10000, sellPrice=.02, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery14 = Battery(node=14, chargeState=10000, sellPrice=.31, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery15 = Battery(node=15, chargeState=10000, sellPrice=.01, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery16 = Battery(node=16, chargeState=10000, sellPrice=.02, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery17 = Battery(node=17, chargeState=10000, sellPrice=.03, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery18 = Battery(node=18, chargeState=10000, sellPrice=.01, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery19 = Battery(node=19, chargeState=10000, sellPrice=.16, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery20 = Battery(node=20, chargeState=10000, sellPrice=.18, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery21 = Battery(node=21, chargeState=10000, sellPrice=.09, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery22 = Battery(node=22, chargeState=10000, sellPrice=.10, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery23 = Battery(node=23, chargeState=10000, sellPrice=.02, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery24 = Battery(node=24, chargeState=10000, sellPrice=.04, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery25 = Battery(node=25, chargeState=10000, sellPrice=.05, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery26 = Battery(node=26, chargeState=10000, sellPrice=.19, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery27 = Battery(node=27, chargeState=10000, sellPrice=.06, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery28 = Battery(node=28, chargeState=10000, sellPrice=.04, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery29 = Battery(node=29, chargeState=10000, sellPrice=.1, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery30 = Battery(node=30, chargeState=10000, sellPrice=.04, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery31 = Battery(node=31, chargeState=10000, sellPrice=.03, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery32 = Battery(node=32, chargeState=10000, sellPrice=.21, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery33 = Battery(node=33, chargeState=10000, sellPrice=.04, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery34 = Battery(node=34, chargeState=10000, sellPrice=.09, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery35 = Battery(node=35, chargeState=10000, sellPrice=.08, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery36 = Battery(node=36, chargeState=10000, sellPrice=.30, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery37 = Battery(node=37, chargeState=10000, sellPrice=.02, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery38 = Battery(node=38, chargeState=10000, sellPrice=.04, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery39 = Battery(node=39, chargeState=10000, sellPrice=.09, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery40 = Battery(node=40, chargeState=10000, sellPrice=.01, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery41 = Battery(node=41, chargeState=10000, sellPrice=.03, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery42 = Battery(node=42, chargeState=10000, sellPrice=.01, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery43 = Battery(node=43, chargeState=10000, sellPrice=.005, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery44 = Battery(node=44, chargeState=10000, sellPrice=.02, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery45 = Battery(node=45, chargeState=10000, sellPrice=.04, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery46 = Battery(node=46, chargeState=10000, sellPrice=.01, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery47 = Battery(node=47, chargeState=10000, sellPrice=.06, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery48 = Battery(node=48, chargeState=10000, sellPrice=.1, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery49 = Battery(node=49, chargeState=10000, sellPrice=.09, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
Battery50 = Battery(node=50, chargeState=10000, sellPrice=.1, maxPower=MAX_BAT_POWER_FLOW, minPower=-MAX_BAT_POWER_FLOW,capacity=13500)
#prices are $/watt
#Tesla PowerWalls have 13.5 kWh capacity according to Gemini


#Node Instances
Node1 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node2 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node3 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node4 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node5 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node6 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node7 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node8 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node9 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node10 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node11 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node12 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node13 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node14 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node15 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node16 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node17 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node18 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node19 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node20 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node21 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node22 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node23 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node24 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node25 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node26 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node27 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node28 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node29 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node30 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node31 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node32 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node33 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node34 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node35 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node36 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node37 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node38 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node39 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node40 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node41 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node42 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node43 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node44 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node45 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node46 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node47 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node48 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node49 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
Node50 = Node(minVoltage=.95*240, maxVoltage=1.05*240)
#choosing 240V as a secondary distribution line voltage


#Line instances
Line01 = Line(startNode=0,endNode=1,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line12 = Line(startNode=1,endNode=2,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line23 = Line(startNode=2,endNode=3,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line14 = Line(startNode=1,endNode=4,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line45 = Line(startNode=4,endNode=5,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line56 = Line(startNode=5,endNode=6,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line17 = Line(startNode=1,endNode=7,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line78 = Line(startNode=7,endNode=8,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line89 = Line(startNode=8,endNode=9,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line9x10 = Line(startNode=9,endNode=10,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line10x11 = Line(startNode=10,endNode=11,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line11x12 = Line(startNode=11,endNode=12,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line12x13 = Line(startNode=12,endNode=13,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line13x14 = Line(startNode=13,endNode=14,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line14x15 = Line(startNode=14,endNode=15,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line15x16 = Line(startNode=15,endNode=16,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line16x17 = Line(startNode=16,endNode=17,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line17x18 = Line(startNode=17,endNode=18,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line18x19 = Line(startNode=18,endNode=19,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line19x20 = Line(startNode=19,endNode=20,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line3x21 = Line(startNode=3,endNode=21,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line21x22 = Line(startNode=21,endNode=22,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line22x23 = Line(startNode=22,endNode=23,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line23x24 = Line(startNode=23,endNode=24,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line24x25 = Line(startNode=24,endNode=25,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line25x26 = Line(startNode=25,endNode=26,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line26x27 = Line(startNode=26,endNode=27,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line27x28 = Line(startNode=27,endNode=28,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line28x29 = Line(startNode=28,endNode=29,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line29x30 = Line(startNode=29,endNode=30,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line6x31 = Line(startNode=6,endNode=31,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line31x32 = Line(startNode=31,endNode=32,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line32x33 = Line(startNode=32,endNode=33,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line33x34 = Line(startNode=33,endNode=34,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line34x35 = Line(startNode=34,endNode=35,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line35x36 = Line(startNode=35,endNode=36,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line36x37 = Line(startNode=36,endNode=37,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line37x38 = Line(startNode=37,endNode=38,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line38x39 = Line(startNode=38,endNode=39,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line39x40 = Line(startNode=39,endNode=40,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line36x41 = Line(startNode=36,endNode=41,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line41x42 = Line(startNode=41,endNode=42,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line42x43 = Line(startNode=42,endNode=43,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line43x44 = Line(startNode=43,endNode=44,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line44x45 = Line(startNode=44,endNode=45,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line45x46 = Line(startNode=45,endNode=46,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line46x47 = Line(startNode=46,endNode=47,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line47x48 = Line(startNode=47,endNode=48,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line48x49 = Line(startNode=48,endNode=49,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
Line49x50 = Line(startNode=49,endNode=50,impedance=.35+0j,minPowerFlow = -50000,maxPowerFlow=50000)
#ACSR resistance .35 ohms per 1000 ft (researched)
#According to ChatGPT, 50000 W is a reasonable limit for secondary distribution power flow 

#Load instances
Load1 = Load(node = 1,loadValue = 0)
Load2 = Load(node = 2,loadValue = 0)
Load3 = Load(node = 3,loadValue = 0)
Load4 = Load(node = 4,loadValue = 0)
Load5 = Load(node = 5,loadValue = 0)
Load6 = Load(node = 6,loadValue = 0)
Load7 = Load(node = 7,loadValue = 0)
Load8 = Load(node = 8,loadValue = 0)
Load9 = Load(node = 9,loadValue = 0)
Load10 = Load(node = 10,loadValue = 0)
Load11 = Load(node = 11,loadValue = 0)
Load12 = Load(node = 12,loadValue = 0)
Load13 = Load(node = 13,loadValue = 0)
Load14 = Load(node = 14,loadValue = 0)
Load15 = Load(node = 15,loadValue = 0)
Load16 = Load(node = 16,loadValue = 0)
Load17 = Load(node = 17,loadValue = 0)
Load18 = Load(node = 18,loadValue = 0)
Load19 = Load(node = 19,loadValue = 0)
Load20 = Load(node = 20,loadValue = 0)
Load21 = Load(node = 21,loadValue = 0)
Load22 = Load(node = 22,loadValue = 0)
Load23 = Load(node = 23,loadValue = 0)
Load24 = Load(node = 24,loadValue = 0)
Load25 = Load(node = 25,loadValue = 0)
Load26 = Load(node = 26,loadValue = 0)
Load27 = Load(node = 27,loadValue = 0)
Load28 = Load(node = 28,loadValue = 0)
Load29 = Load(node = 29,loadValue = 0)
Load30 = Load(node = 30,loadValue = 0)
Load31 = Load(node = 31,loadValue = 0)
Load32 = Load(node = 32,loadValue = 0)
Load33 = Load(node = 33,loadValue = 0)
Load34 = Load(node = 34,loadValue = 0)
Load35 = Load(node = 35,loadValue = 0)
Load36 = Load(node = 36,loadValue = 0)
Load37 = Load(node = 37,loadValue = 0)
Load38 = Load(node = 38,loadValue = 0)
Load39 = Load(node = 39,loadValue = 0)
Load40 = Load(node = 40,loadValue = 0)
Load41 = Load(node = 41,loadValue = 0)
Load42 = Load(node = 42,loadValue = 0)
Load43 = Load(node = 43,loadValue = 0)
Load44 = Load(node = 44,loadValue = 0)
Load45 = Load(node = 45,loadValue = 0)
Load46 = Load(node = 46,loadValue = 0)
Load47 = Load(node = 47,loadValue = 0)
Load48 = Load(node = 48,loadValue = 0)
Load49 = Load(node = 49,loadValue = 0)
Load50 = Load(node = 50,loadValue = 0)


MAX_SELL_PRICE = max(Battery1.sellPrice,Battery2.sellPrice,Battery3.sellPrice,Battery4.sellPrice,Battery5.sellPrice,Battery6.sellPrice,Battery7.sellPrice,Battery8.sellPrice,Battery9.sellPrice,
					Battery10.sellPrice,Battery11.sellPrice,Battery12.sellPrice,Battery13.sellPrice,Battery14.sellPrice,Battery15.sellPrice,Battery16.sellPrice,Battery17.sellPrice,Battery18.sellPrice,
					Battery19.sellPrice,Battery20.sellPrice,Battery21.sellPrice,Battery22.sellPrice,Battery23.sellPrice,Battery24.sellPrice,Battery25.sellPrice,Battery26.sellPrice,Battery27.sellPrice,
					Battery18.sellPrice,Battery29.sellPrice,Battery30.sellPrice,Battery31.sellPrice,Battery32.sellPrice,Battery33.sellPrice,Battery34.sellPrice,Battery35.sellPrice,Battery36.sellPrice,
					Battery37.sellPrice,Battery38.sellPrice,Battery39.sellPrice,Battery40.sellPrice,Battery41.sellPrice,Battery42.sellPrice,Battery43.sellPrice,Battery44.sellPrice,Battery45.sellPrice,
					Battery46.sellPrice,Battery47.sellPrice,Battery48.sellPrice,Battery49.sellPrice,Battery50.sellPrice)


# Matrices
topologyMatrix = [[-1,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,1,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1]]

voltageRelationshipMatrixOne = [[1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[1,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[1,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,-1,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1]]

voltageRelationshipMatrixTwo = [[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
								[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]]
				

# Datasets
OUTPUT_DATA_PATH = "/Users/benjaminglass/Desktop/EC601/virtual-power-plant/outputFiles"
outputData = pd.DataFrame(columns=['iteration','Pi1','Pi2','Pi3','Pi4','Pi5','Pi6','Pi7','Pi8','Pi9','Pi10',
												'Pi11','Pi12','Pi13','Pi14','Pi15','Pi16','Pi17','Pi18','Pi19','Pi20',
												'Pi21','Pi22','Pi23','Pi24','Pi25','Pi26','Pi27','Pi28','Pi29','Pi30',
												'Pi31','Pi32','Pi33','Pi34','Pi35','Pi36','Pi37','Pi38','Pi39','Pi40',
												'Pi41','Pi42','Pi43','Pi44','Pi45','Pi46','Pi47','Pi48','Pi49','Pi50',

												'B1cs','B2cs','B3cs','B4cs','B5cs','B6cs','B7cs','B8cs','B9cs','B10cs',
												'B11cs','B12cs','B13cs','B14cs','B15cs','B16cs','B17cs','B18cs','B19cs','B20cs',
												'B21cs','B22cs','B23cs','B24cs','B25cs','B26cs','B27cs','B28cs','B29cs','B30cs',
												'B31cs','B32cs','B33cs','B34cs','B35cs','B36cs','B37cs','B38cs','B39cs','B40cs',
												'B41cs','B42cs','B43cs','B44cs','B45cs','B46cs','B47cs','B48cs','B49cs','B50cs',

												'Pf01','Pf12','Pf23','Pf14','Pf45','Pf56','Pf17','Pf78','Pf89',"Pf9x10",
												'Pf10x11','Pf11x12','Pf12x13','Pf13x14','Pf14x15','Pf15x16','Pf16x17','Pf17x18','Pf18x19',"Pf19x20",
												'Pf3x21','Pf21x22','Pf22x23','Pf23x24','Pf24x25','Pf25x26','Pf26x27','Pf27x28','Pf28x29',"Pf29x30",
												'Pf6x31','Pf31x32','Pf32x33','Pf33x34','Pf34x35','Pf35x36','Pf36x37','Pf37x38','Pf38x39',"Pf39x40",
												'P36x41','Pf41x42','Pf42x43','Pf43x44','Pf44x45','Pf45x46','Pf46x47','Pf47x48','Pf48x49',"Pf49x50",

												'V1','V2','V3','V4','V5','V6','V7','V8','V9',"V10",
												'V11','V12','V13','V14','V15','V16','V17','V18','V19',"V20",
												'V21','V22','V23','V24','V25','V26','V27','V28','V29',"V30",
												'V31','V32','V33','V34','V35','V36','V37','V38','V39',"V40",
												'V41','V42','V43','V44','V45','V46','V47','V48','V49',"V50",
												"Buy Price","Optimal Cost"])


INPUT_LOAD_PATH = "/Users/benjaminglass/Desktop/EC601/virtual-power-plant/inputFiles/load.csv"
loadData = pd.read_csv(INPUT_LOAD_PATH,header=None)











