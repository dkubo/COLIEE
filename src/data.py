# coding: utf-8

from xml.etree import ElementTree as ET
from collections import Counter
import re

# Get the Task Data
def getData(fpath, data):
	for subtree in ET.parse(fpath).getiterator("pair"):
		data.update({
			subtree.get("id"):
			{"label": subtree.get("label"),
				"t1": subtree.findtext("t1"),
				"t2": subtree.findtext("t2")}
		})
	return data

# split the paragraph to sentences
def split2sentence(paragraph):
	res, sensp, merge = [], [], ""
	opencnt, closecnt = 0, 0

	res = rm(paragraph.replace('\n', "").split("。"))
	# res = ["吾輩は「猫だっけ","」である","名前はまだない"]
	for part in res:
		counter = Counter(part)
		opencnt += counter['('] + counter['（'] + counter['「']
		closecnt += counter[')'] + counter['）'] + counter['」']

		if opencnt > closecnt:
			merge += part + "。"
		else:
			merge += part
			sensp.append(merge)
			merge = ""
	return sensp

# Get the each article in Civil Code 
def getCivilCode():
	civil = {}
	fname = "../data/COLIEE-2017_Japanese_Training_Data/civil_japanese_utf8.txt"

	with open(fname) as f:
		for line in f:
			jomatch = re.search(r'^第[〇一二三四五六七八九十百千]{1,6}条　', line)
			# 「漢数字 」は，条件の箇条書き→条文本文の続き?
			# 「英数字 」は，～条の～のやつ
			jomatch = re.search(r'^第[〇一二三四五六七八九十百千]{1,6}条　', line)
			if res:
				span = res.span()
				# print("---------------------")
				# print(line)
				jonum, jobun = line[0:span[1]-1], line[span[1]:-1]
				civil[jonum] = {"text":jobun}

	print(civil)	
			# if /^([0-9０-９〇一二三四五六七八九十百千]{1,6}条の[0-9０-９〇一二三四五六七八九十百千]{1,2}|第[0-9０-９〇一二三四五六七八九十百千]{1,6}条)/ =~ line.chomp:
			# 	jo = $&
			# 	civil[jo] = ''
			# 	jo_frg = 1
			# elif (jo_frg == 1) and (l != "\n"):
			# 	civil[jo] += str(line)
	return civil


# Get the clue representation
def getClueRep(fpath):
	"""
	接続語	強い	但し,ただし
	例外規定	強い	除いては,除く外は,除くほかは,除くの外は,のほかは,の他は,の外は
	例外規定	弱い	除き,除いて,除く外,除くほか,除くの外,のほか,の他,の外
	反則規定	弱い	に反して,に反し
	適用緩和	弱い	でも,かかわらず,よらないで,を問わず
	"""
	cluerep, exceptlist = [], ["接続語", "例外規定", "反則規定", "適用緩和"]
	pattern = ""
	with open(fpath) as f:
		for line in f:
			if not line.split("\t")[0] in exceptlist:
				cluerep += line.split("\t")[2].rstrip().split(",")
	cluerep = list(set(cluerep))
	cluerep.append("において")

	for rep in cluerep:
		pattern += rep+"|"

	return "("+pattern[0:-1]+")"

# remove the "" from List
def rm(array):
	return [x for x in array if x is not ""]

# Split sentences into legal requirements and effects
def split2reqeff(sent, pattern):
	sentlist = re.split(r'、|または|又は|かつ|且つ|，', sent)	# split using rep
	sentlist = rm(sentlist)	# remove the ""
	# sentlist = list(filter(lambda s:s != '', sentlist))	# remove the ""

	pairs, frg = {}, 0
	prereq, req = "", ""
	for part in sentlist:
		part = re.sub(r'。$', "", part)
		res = re.search(r'{0}$'.format(pattern), part)

		if res:		# requirements
			req = part[0:res.span()[0]]
			if (prereq not in pairs) and (prereq != ""):
				req = prereq + "、" + req

			if frg == 0:
				pairs[req], prereq, frg = "", req, 1
			else:	# if req→req
				del pairs[prereq]
				pairs[prereq+"、"+req] = ""
				prereq = prereq+"、"+req

		else:		# effects
			if not prereq in pairs:
				prereq += part
			else:
				if pairs[prereq] == "":
					pairs[prereq] += part
				else:
					pairs[prereq] += "、"+part
			frg = 0

	return pairs

if __name__ == '__main__':
	# data = {}
	# for year in range(18,28):
	# 	fpath = "../data/COLIEE-2017_Japanese_Training_Data/utf8/riteval_H{}.xml".format(str(year))
	# 	data = getData(fpath, data)

	# print(len(data))	# 581, N:281 Y:300
	fpath = "../result/clueRep.txt"
	pattern = getClueRep(fpath)
	# egsent = "その行為が故意であった場合は、それを罪とし、損害賠償請求権が与えられる。"	# req→eff
	# egsent = "その行為が故意であった場合は、それを罪とし、故意でなかった場合には、損害賠償請求権を無効とする。"	# req→eff, req→eff
	# egsent = "その行為が故意であった場合は、それを罪とし、損害賠償請求権を無効とする。"	# req→eff, eff
	# egsent = "その行為が故意であった場合は、又は、知りながら無視した場合には、損害賠償請求権を無効とし、訴追権を与えるとする。"	# req,req→eff
	# egsent = "訴追権を与えるとする。"	# eff (only)
	# egsent = "その行為が故意であった場合には、"	# req (only)
	pairs = split2reqeff(egsent, pattern)

