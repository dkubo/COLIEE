#coding:utf-8

require_relative '../../legalNLP/hanrei/src/sqlite3.rb'
require_relative '../../legalNLP/hanrei/src/senSplit.rb'
require 'natto'

"""
判決文・法律文書をもとに，分散表現作るための分かち書きデータ作る
"""

DB_PATH="../../legalNLP/hanrei/data/hanreiDB"

def wakati(result, nt)
	wakatilist = []
	result.each{|sentence|
		wakatilist.push(nt.parse(sentence).delete("\n"))
	}
	return wakatilist
end


def getHanrei()
	db = SQLight3.new(DB_PATH)
	wakatilist = []
	nt = Natto::MeCab.new(output_format_type: :wakati)
	# p nt.parse("特許法を適用した")
	sql = "select syubunPart, riyuPart from hanrei"
	cursorID = db.executeSQL(sql)
	cursorID.each do |tuple_id|
		syubun, riyu = tuple_id[0], tuple_id[1]
		begin
			sp = SenSplit.new(syubun+riyu)
			result = sp.split_period()	# 文ごとで取得
			wakatilist += wakati(result, nt)	# 分かち書き
		rescue
			puts tuple_id
		end
	end
	return wakatilist
end

def getHourei()
	wakatilist = []
	return wakatilist
end

def output(src, fname)
	File.open(fname, "w") do |f| 
		f.puts(src.join("\s"))
	end
end

def main()
	wakatilist = []
	p wakatilist.length
	wakatilist += getHanrei()
	output(wakatilist, "../result/hanreiWakati.txt")
	# p wakatilist.length
	# wakatilist += getHourei()
end

main()
