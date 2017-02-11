# coding: utf-8

from gensim.models import word2vec

def calcSimword(model, word):
	result = model.most_similar(positive=word)
	for x in result:
		print(x[0], x[1])

def calcWMD(sent1, sent2):
	dist = model.wmdistance(sent1, sent2)	
	print(dist)

def loadModel(mpath):
	return word2vec.Word2Vec.load(mpath)

if __name__ == '__main__':
	wakati = "../result/hanreiWakati.txt"
	mpath = "../result/hanrei.model"
	# data = word2vec.Text8Corpus(wakati)
	# model = word2vec.Word2Vec(data, size=200, window=5, min_count=5, workers=15)
	# data = word2vec.Text8Corpus("../result/sample.txt")
	# model = word2vec.Word2Vec(data, size=50, min_count=1, workers=15)
	# model.save("../result/hanrei.model")
	model = loadModel(mpath)
	# print(model.vocab)
	# calcSimword(model, [u"特許"])
	# sent1, sent2, sent3 = "特許は重要だ", "新案を提出した", "特許法は無視できない"
	# calcWMD(sent1, sent2)


	