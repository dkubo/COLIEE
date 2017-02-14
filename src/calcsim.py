# coding: utf-8

import data
import trainvec
from gensim.models import word2vec

def calcWMD(model, pair, civil):
	"""
	Calculate the WMDistance between Prob. and Civil Code
	"""
	totaldist, cnt = 0, 0
	sent = []
	# for cnt, (req, eff) in enumerate(pair.items()):
	for req, eff in pair.items():
		cnt += 1
		# t2内の各要件-効果ペアがそれぞれ閾値を超えたら正解？
		# print(req, "-", eff)
		mindist, minsent = calc(req, eff, civil)
		totaldist += mindist
		sent.append(minsent)
	return totaldist/cnt, sent

def calc(req, eff, civil):
	disthash = {}
	for jonum, article in civil.items():
		# print(jonum, article)
		for k, value in article.items():
			if (k != "title") and (type(value) == dict):
				for reqcivil, effcivil in value.items():
					dist1 = model.wmdistance(req, reqcivil)
					dist2 = model.wmdistance(eff, effcivil)
					disthash[(dist1+dist2)] = reqcivil+"-"+effcivil
						# print(dist1+dist2)
						# print(reqcivil, "-", effcivil)

	return min(disthash.keys()), disthash[min(disthash.keys())]
# 最小距離を返す

def eval(dist, ans):
	print(dist)
	if dist < 35:
		predict = "Y"
	else:
		predict = "N"
	
	print(predict, ans)
	if predict == ans:
		return 1
	else:
		return 0

def taskData():
	"""
	Get the task data
	"""
	# taskdata = {}
	# for year in range(18,28):
	# 	fpath = "../data/COLIEE-2017_Japanese_Training_Data/utf8/riteval_H{}.xml".format(str(year))
	# 	taskdata = data.getData(fpath, taskdata)
	# data.pickleFunc("../result/taskdata.pickle", taskdata, "save")
	taskdata = data.pickleFunc("../result/taskdata.pickle", None, "load")
	return taskdata

def civilCode(pattern):
	# civil = data.getCivilCode()
	# data.pickleFunc("../result/civil.pickle", civil, "save")
	civil = data.pickleFunc("../result/civil.pickle", None, "load")

	for jonum, article in civil.items():
		for k, v in article.items():
			if k != "title":
				sentences = data.split2sent(v.replace("　", ""))
				for sentence in sentences:
					civil[jonum][k] = data.split2reqeff(sentence, pattern)
	return civil

if __name__ == '__main__':

	# Get the task data
	taskdata = taskData()

	# Train the embedding
	mpath = "../result/hanrei.model"
	model = trainvec.loadModel(mpath)

	# Get the Clue Representation
	fpath = "../result/clueRep.txt"
	pattern = data.getClueRep(fpath)

	# Get the Civil Code
	civil = civilCode(pattern)

	# Split into legal requirements and effects
	probnum, correct = 0, 0
	for probid, v in taskdata.items():
		sentences = data.split2sent(v["t2"])
		ans = v["label"]
		totaldist = 0
		buf = []
		for sentence in sentences:
			pair = data.split2reqeff(sentence, pattern)

			# Calculate the WMD
			if type(pair) == dict:
				mindist, minsent = calcWMD(model, pair, civil)
				totaldist += mindist
				buf += minsent
		if totaldist != 0:
			probnum += 1
			print("--------------")
			print(probid, v["label"])
			print(sentences)
			print(buf)
			correct += eval(totaldist, ans)

	print("--------------")
	print("correct, probnum:", str(correct), str(probnum))
	print("acc:", str(correct/probnum))

		# trainvec.calcSimword(model, [u"借用"])

		# if pairs == {}:
		# 	"""
		# 	事実が記述されているものは，述語項構造解析？
		# 	「ためには」は，マッチした後者が要件で，前者が効果となる
		# 	"""
		# 	print("--------------")
		# 	print(k, v["t2"])
		# 	print(v["t2"].split("ためには"))
		# 	if len(v["t2"].split("ためには")) >= 2:
		# 		print("--------------")
		# 		print(k, v["t2"])
		# 		print(v["t2"].split("ためには"))
		# else:
		# 	print("--------------")
		# 	print(k, v["t2"])
		# 	print(pairs)



