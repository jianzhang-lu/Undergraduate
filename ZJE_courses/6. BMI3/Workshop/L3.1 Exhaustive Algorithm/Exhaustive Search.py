#!/usr/bin/env python
# -*-coding:utf-8 -*-

from typing import Set

def PatternCount(text: str, pattern: str) -> int:
	"""
	@brief: Count occurance of pattern in a string.
	@args:
		text: the target string
		pattern: the pattern to search in the target string
	@returns:
		Number of occurance of $pattern in $text
	"""
	count = 0
	k = len(pattern)
	for i in range(0, len(text)-k+1, 1):
		if text[i:i+k] == pattern:
			count += 1
	return count

def FrequentWords(text: str, k:int) -> Set[str]:
	"""
	@brief: Find the most fequent substring with length k in the target string
	@args:
		text: the target string
		pattern: length of the pattern
	@returns:
		the most fequent substring with length k
	"""
	count = []
	max_count = 0
	frequent_word = []
	for i in range(0, len(text)-k+1, 1):
		pattern = text[i:i+k]
		cur_count = PatternCount(text, pattern)
		count.append(cur_count)
		if cur_count > max_count:
			max_count = cur_count
	for i in range(0, len(count), 1):
		if count[i] == max_count:
			frequent_word.append(text[i:i+k])
	return set(frequent_word)

def HammingDistance(s1: str, s2: str) -> int:
	"""
	@brief: Return the hamming distance between s1 and s2. len(s1) should be equal to len(s2)
	@args:
		s1: the first string
		s2: the second string
	"""
	assert (len(s1) == len(s2))
	hamming_distance = 0
	for i in range(len(s1)):
		if s1[i] != s2[i]:
			hamming_distance += 1
	return hamming_distance

def ApproximatePatternCount(text: str, pattern: str, d: int) -> int:
	"""
	@brief: Count occurance of pattern in a string allowing mismatch d.
	@args:
		text: the target string
		pattern: the pattern to search in the target string
	@returns:
		Number of occurance of $pattern in $text
	"""
	count = 0
	for i in range(len(text)-len(pattern)+1):
		cur_pattern = text[i:i+len(pattern)]
		if HammingDistance(pattern, cur_pattern) <= d:
			count += 1
	return count

def SymbolToNumber(symbol: str) -> int:
	"""
	@brief: should be ordered by lexicographical order  {'A':0, 'C':1, 'G':2, 'T':3}
	"""
	s_to_n = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
	return s_to_n[symbol]

def NumberToSymbol(num: int) -> str:
	"""
	@brief: reverse function of SymbolToNumber
	"""
	n_to_s = ['A', 'C', 'G', 'T']
	return n_to_s[num]

def PatternToNumber(pattern: str) -> int:
	if len(pattern) == 0:
		return 0
	else:
		length = len(pattern)
		return 4 * PatternToNumber(pattern[0:length-1]) + SymbolToNumber(pattern[length-1])

def NumberToPattern(index: int, k: int) -> str:
	"""
	k should be the length of output string
	"""
	if k == 1:
		return NumberToSymbol(index)
	quotient = index // 4
	remainder = index % 4
	front = NumberToPattern(quotient, k-1)
	behind = NumberToSymbol(remainder)
	return front + behind

def ImmediateNeighbors(pattern: str) -> Set[str]:
	n_list = ['A', 'C', 'G', 'T']
	neighborhood = set()
	neighborhood.add(pattern)
	for i in range(len(pattern)):
		pattern_list = list(pattern)
		for n in range(len(n_list)):
			if pattern_list[i] != n_list[n]:
				pattern_list[i] = n_list[n]
				new_pattern = ''.join(pattern_list)
				neighborhood.add(new_pattern)
	return neighborhood

def Neighbors(pattern: str, d: int) -> Set[str]:
	n_list = ['A', 'C', 'G', 'T']
	if d == 0:
		return {pattern}
	if len(pattern) == 1:
		return {'A', 'C', 'G', 'T'}

	neighborhood = set()
	first_pattern = pattern[0]
	suffix_pattern = pattern[1:]
	suffix_neighbor = Neighbors(suffix_pattern, d)
	for i in suffix_neighbor:
		if HammingDistance(i, suffix_pattern) < d:
			for n in n_list:
				neighborhood.add(n + i)
		else:
			neighborhood.add(first_pattern + i)
	return neighborhood

def FrequentWordsWithMismatches(text: str, k: int, d: int) -> Set[str]:
	result = set()
	close, count = [], []
	# 创立close和count列表，长度为4的j次方，默认全是0
	for i in range(4**k):
		close.append(0)
		count.append(0)
	# 寻找每个k-mer的neighborhood，将其close变为1
	for j in range(len(text)-k+1):
		cur_pattern = text[j:j+k]
		neighborhood = Neighbors(cur_pattern, d)
		for n in neighborhood:
			num_index = PatternToNumber(n)
			close[num_index] = 1
	# 针对所有close=1的pattern寻找Approximate Pattern Count
	for m in range(len(close)):
		if close[m] == 1:
			pattern = NumberToPattern(m, k)
			count[m] = ApproximatePatternCount(text, pattern, d)

	max_count = max(count)
	for n in range(len(count)):
		if count[n] == max_count:
			result_pattern = NumberToPattern(n, k)
			result.add(result_pattern)

	return result