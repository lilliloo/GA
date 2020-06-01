# -*- coding: utf-8 -*-
"""
Created on Tue May  5 10:32:05 2020

@author: lilliloo
"""

#-----------------------------------------#

# Theme : Onemax Problem

#-----------------------------------------#

#符号:バイナリエンコーディング
#0と1で遺伝子を表現する
#
#選択:エリート主義
#もっとも適用度の高い個体を選択する
#
#交叉:二点交叉
#遺伝子の一部にランダムな二点を選択し、
#その間にある遺伝子を入れ替える
#
#変異:置換
#遺伝子を対立する数値に置き換える
#0.1%~1% 高くても数%
#低すぎると局所収束。高すぎると収束しない。
#
#世代:定常状態モデル
#生成した子孫を適用度の低い個体と入れ替える。

import random
import numpy as np
import matplotlib.pyplot as plt

class genom :
    genom_list = None
    evaluation = None
    
    def _init_(self, genom_list, evaluation):
        self.genom_list = genom_list
        self.evaluation = evaluation
    
    def getGenom(self):
        return self.genom_list
    
    def getEvaluation(self):
        return self.evaluation
    
    def setGenom(self, genom_list):
        self.genom_list = genom_list
    
    def setEvaluation(self, evaluation):
        self.evaluation = evaluation

# -----  Main  ------#

# Parameter 
# 遺伝子情報の長さ
GENOM_LENGTH = 20
# 遺伝子集団の大きさ
MAX_GENOM_LIST = 10
# 遺伝子選択数
SELECT_GENOM = 2
# 個体突然変異確率 @GitHubに上げたコードでは0.1の10%になってます
INDIVIDUAL_MUTATION = 0.01
# 遺伝子突然変異確率 @GitHubに上げたコードでは0.1の10%になってます
GENOM_MUTATION = 0.01
# 繰り返す世代数
MAX_GENERATION = 40

def create_genom(length):
    genom = []
    for i in range(length):
        genom.append(random.randint(0,1))   
    return genom

def evaluation(genom):
    eva = sum(genom)
    return eva

def select_elite(generation, elites):
    generation.sort(reverse = True)
    elites = generation[:elites]
    return elites
def crossover(parent1, parent2):
    cross1 = random.randint(0,GENOM_LENGTH)
    cross2 = random.randint(cross1,GENOM_LENGTH)
    
    genom1 = parent1[1]
    genom2 = parent2[1]
    
    child_genom = genom1[:cross1] + genom2[cross1:cross2] + genom1[cross2:] 
    child = [evaluation(child_genom), child_genom]
    return child

def create_next_generation(elites):
    next_generation = elites
    while len(next_generation) < MAX_GENOM_LIST :
        parent = []
        while len(parent) < 2:
            r = random.randint(0,len(elites)-1)
            if r not in parent:
                parent.append(r)
        child = crossover(elites[parent[0]], elites[parent[1]])
        next_generation.append(child)
        
    return next_generation
        
def mutation(offspring):
    for i in range(GENOM_LENGTH): 
        p = random.random()
        if ( p < GENOM_MUTATION):
            if offspring[i] == 0:
                offspring[i] = 1
            else:
                offspring[i] = 0  
    return offspring
        
if __name__ == "__main__":
    generation = []
    elite_rate = 4
    max_evaluation = []
    al = []
    
    #１世代の生成
    for i in range(MAX_GENOM_LIST):
        Genom = create_genom(GENOM_LENGTH)
        Evaluation = evaluation(Genom)
        generation.append([Evaluation, Genom])
    generation.sort(reverse = True)
    max_evaluation.append(generation[0][0])
    max_gene_evaluation = generation[0][0]
    al.append(generation)
    
    flag = 0
#    while max_gene_evaluation > 18:
    for i in range(100):
        pre_generation = al[i]
    ##    # エリートの抽出
        elites = select_elite(pre_generation, elite_rate)
    ##    # 子の生成
        children = create_next_generation(elites)
    ##    # mutation
        for j in range(MAX_GENOM_LIST):
            offspring = children[j][1]
            offspring = mutation(offspring)
            #再評価
            eva = evaluation(offspring)
            children[j][0] = eva
            children[j][1] = offspring
        
        children.sort(reverse = True)
        max_evaluation.append(children[0][0])   
        al.append(children)

plt.figure(figsize = (10, 10))
plt.plot(np.arange(len(max_evaluation)), max_evaluation)
    
    
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        