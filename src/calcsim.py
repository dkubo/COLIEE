# coding: utf-8

import data
import trainvec

if __name__ == '__main__':

	# get the task data
	# taskdata = {}
	# for year in range(18,28):
	# 	fpath = "../data/COLIEE-2017_Japanese_Training_Data/utf8/riteval_H{}.xml".format(str(year))
	# 	taskdata = data.getData(fpath, taskdata)

	# train the embedding
	# mpath = "../result/hanrei.model"
	# model = trainvec.loadModel(mpath)

	# Get the Civil Code
	civil = data.getCivilCode()

	# Split into legal requirements and effects
	# fpath = "../result/clueRep.txt"
	# pattern = data.getClueRep(fpath)
	# for k, v in taskdata.items():
	# 	pairs = {}
	# 	sentences = data.split2sentence(v["t2"])
	# 	for sentence in sentences:
	# 		pairs.update(data.split2reqeff(sentence, pattern))
		# if pairs == {}:
			# """
			# 事実が記述されているものは，述語項構造解析？
			# 「ためには」は，マッチした後者が要件で，前者が効果となる
			# """
			# print("--------------")
			# print(k, v["t2"])
			# print(v["t2"].split("ためには"))
			# if len(v["t2"].split("ためには")) >= 2:
				# pass
				# print("--------------")
				# print(k, v["t2"])
				# print(v["t2"].split("ためには"))
		# else:
		# 	print("--------------")
		# 	print(k, v["t2"])
		# 	print(pairs)

	# Calc the wmd
	# trainvec.calcSimword(model, [u"借用"])
	# trainvec.calcWMD(sent1, sent2)


