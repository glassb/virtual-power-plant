import run 
import configuration as config
import pandas as pd
import functions
import os



OUTPUT_ANALYSIS_PATH = "/Users/benjaminglass/Desktop/EC601/virtual-power-plant/outputFiles"
outputAnalysis = pd.DataFrame(columns=['Power Request','Load Scaling Factor','Cost Result'])

POWER_REQUESTS = [8200,8400,8600,8800,9000,9200,9400,9600,10000]
SCALING_FACTORS = [.1,.11,.12,.13,.14,.15,.16,.17,.18,.19,.2]


for i in range(len(POWER_REQUESTS)):
	for j in range(len(SCALING_FACTORS)):

		functions.resetSimulation()

		config.AGGREGATOR_POWER_REQUEST = POWER_REQUESTS[i]
		config.LOAD_SCALING_FACTOR = SCALING_FACTORS[j]

		print(config.AGGREGATOR_POWER_REQUEST)
		print(config.LOAD_SCALING_FACTOR)

		result = run.run()

		#got this tip from gemini to use len(outputAnalysis) in the loc method
		outputAnalysis.loc[len(outputAnalysis)] = [config.AGGREGATOR_POWER_REQUEST,config.LOAD_SCALING_FACTOR,result]
		print(outputAnalysis)


print(outputAnalysis)

os.chdir(OUTPUT_ANALYSIS_PATH)
dateTimeNow = functions.getCurrentTimeStamp()
outputAnalysis.to_csv("analysisOutput-"+dateTimeNow+".csv")