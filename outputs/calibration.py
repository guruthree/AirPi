import output
import math
from string import rsplit

class Calibration(output.Output):
	requiredData = []
	optionalData = ["Light_Level", "Air_Quality", "Nitrogen_Dioxide", "Carbon_Monoxide", "Volume", "UVI", "Bucket_tips"]
	sharedClass = None

	def __init__(self,data):
		self.calibrations = []
		self.last = []
		self.lastpassed = []
		for i in self.optionalData:
			if i in data:
				[f, s] = rsplit(data[i], ',', 1)
				self.calibrations.append({'name': i, 'function': eval("lambda x: " + f), 'symbol': s})

		if Calibration.sharedClass == None:
			Calibration.sharedClass = self

	def calibrate(self,dataPoints):
		if self.lastpassed == dataPoints:
			# the same dataPoints object, so the calculations would turn out the same
			# so we can just return the result of the last calcs
			return self.last

		self.last = list(dataPoints) # recreate so we don't overwrite un-calibrated data
		for i in range(0, len(self.last)):
			self.last[i] = dict(self.last[i]) # recreate again
			for j in self.calibrations:
				if self.last[i]["name"] == j["name"]:
					if self.last[i]["value"] != None:
						self.last[i]["value"] = j["function"](self.last[i]["value"])
						self.last[i]["symbol"] = j["symbol"]
		self.lastpassed = dataPoints # update which object we last worked on
		return self.last

def findVal(key):
	found = 0
	num = 0
	for i in Calibration.sharedClass.last:
		if i["name"] == key and i["value"] != None:
			found = found + i["value"]
			num += 1
	# average for things like Temperature where we have multiple sensors
	if num != 0:
		found = found / float(num)
	return found

def calCheck(data):
	if "calibration" in data:
		if data["calibration"].lower() in ["on","true","1","yes"]:
			return 1
		else:
			return 0
	else:
		return 0
