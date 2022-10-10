#!/bin/python
#-*- coding: utf-8 -*-
#Popova was here
import _tkinter
import sys
import math
from matplotlib import rcParams 
import matplotlib.pyplot as plt
import numpy as np 
rcParams['font.family'] = "StixGeneral"


def encryption(filename, shift):
	with open("Зашифровано.txt", 'w', encoding = 'utf-8') as sfr:
		with open(filename, 'r', encoding = 'utf-8') as org:
			for line in org:
				for char in line.lower():
					if 'а'<=char<='я':
						nomer = ord(char) - ord('а')
						char = chr(ord('а')+(nomer+shift)%32)
					sfr.write(char)


def deciphering(filename, shift, outname):
	with open(outname, 'w', encoding = 'utf-8') as itog:
		with open(filename, 'r', encoding = 'utf-8') as sfr:
			for line in sfr:
				for char in line:
					if 'а'<=char<='я':
						nomer = ord(char) - ord('а')
						char = chr(ord('а')+(nomer-shift)%32)
					itog.write(char)

					
def training(filename):			
	alf = dict([[chr(i),0.0] for i in range(ord('а'),ord('я')+1)])
	count = 0.0		
	with open(filename, 'r', encoding = 'utf-8') as text:
		for line in text:
			line = line.lower()
			for char in line:
				if 'а'<=char<='я':
					alf[char] += 1
				count += 1	
	with open("Распределение.txt", 'w', encoding = 'utf-8') as dist:
		for key in alf.keys():
			dist.write(key + ":" + str(alf[key]/count)+'\n')

			
def autodec(TrueShift):
	theor = {}
	exsper = dict([[chr(i),0.0] for i in range(ord('а'),ord('я')+1)])
	count = 0.0	
	X_square = 0.0
	mass_X = []
	f = []
	with open("temptext.txt", 'w', encoding = 'utf-8') as t_text:
		for line in sys.stdin:		
			t_text.write(line)
	with open("Распределение.txt", 'r', encoding = 'utf-8') as text:
		for line in text:
			element = line.rstrip().split(':')
			theor[element[0]] = float(element[1])
			
	n = len(theor)
	for shift in range(1,33):
		with open("temptext.txt", 'r', encoding = 'utf-8') as t_text:
			for line in t_text:
				line = line.lower()
				for char in line:
					if 'а'<=char<='я':
						nomer = ord(char) - ord('а')
						new_char = ord('а')+(nomer-shift)%32
						exsper[chr(new_char)] += 1 
					count += 1	
			for key in exsper.keys():
				count2=count
				t = theor[key] * count
				X_square += pow(t-exsper[key],2)/t
			mass_X.append(X_square)
			if shift==int(TrueShift):
				simvol = sorted(list(exsper.keys()))
				chance=[exsper[i] for i in simvol]		
				band = np.arange(len(simvol))	
			for key in exsper.keys():
				exsper[key] = 0.0
			X_square = 0.0
			count = 0.0
	print("Значение X^2 у истинного смещения: " + str(mass_X[TrueShift-1]))	
	deciphering("temptext.txt", mass_X.index(min(mass_X))+1, "АвтоРасшифровано.txt")
	plt.bar(band, chance)
	plt.xticks(band, simvol)
	plt.bar(range(len(simvol)), [count2*theor[i] for i in simvol], color="red", alpha=0.5)
	plt.show()

	
	
	
def main():
	if (sys.argv[1] == "Ш"):
		encryption(sys.argv[2],	int(sys.argv[3]))
	elif (sys.argv[1] == "Д"):
		deciphering(sys.argv[2], int(sys.argv[3]), "Расшифровано.txt")
	elif (sys.argv[1] == "О"):
		training(sys.argv[2])
	elif (sys.argv[1] == "А"):
		autodec(int(sys.argv[2]))
		
		
if __name__ == "__main__":
	main()
