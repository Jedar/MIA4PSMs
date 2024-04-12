from backwords.backwords_trainer import backwords_counter
from lib4mc.MonteCarloLib import MonteCarloLib
from lib4mc.ProbLib import expand_2d
from nwords_simulator import NWordsMonteCarlo
import pickle
import os


file = open("../test.pickle",'rb')
p = pickle.load(file)
print(p)