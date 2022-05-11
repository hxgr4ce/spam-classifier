#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project 4
Hadley Lim
13 April 2022
I have neither given nor received unauthorized aid on this program.	
"""
import math

#input
spamTrain = input("Enter training file for spam:")
hamTrain = input("Enter training file for ham:")
spamTest = input("Enter test file for spam:")
hamTest = input("Enter test file for ham:")

with open(spamTrain, 'r') as f:
    spamContent = f.readlines()

with open(hamTrain, 'r') as f:
    hamContent = f.readlines()
    
with open(spamTest, 'r') as f:
    spamTestContent = f.readlines()

with open(hamTest, 'r') as f:
    hamTestContent = f.readlines()

vocabList = {}
spamVocabFreq = {}
hamVocabFreq = {}

numSpam = 0
numHam = 0
numTestSpam = 0
numTestHam = 0

"""
TRAINING
"""
#generating vocabList
def makeVocab(content):
    for line in range (0, len(content)):
        if content[line][0:9] == "<SUBJECT>":            
            currLine = line
            while content[currLine][0:7] != "</BODY>":
                if content[currLine][:1] != "<":
                    wordList = content[currLine].split()
                    if wordList != []: 
                        for word in wordList:
                            if word.lower() not in vocabList: vocabList[word.lower()] = None
                            
                currLine += 1

makeVocab(spamContent)
makeVocab(hamContent)

for word in vocabList:
    spamVocabFreq[word] = 0
    hamVocabFreq[word] = 0

#tabulating word frequencies in spam training set
for line in range(0, len(spamContent)):
    if spamContent[line][0:9] == "<SUBJECT>":
        numSpam += 1
        currLine = line
        allEmailWords = []
        while spamContent[currLine][0:7] != "</BODY>":
            if spamContent[currLine][:1] != "<":
                wordList = spamContent[currLine].split()
                if wordList != []: 
                    for word in wordList:
                        if word.lower() not in allEmailWords:
                            spamVocabFreq[word.lower()] += 1
                            allEmailWords.append(word.lower())
            currLine += 1

#tabulating word frequencies in ham training set
for line in range(0, len(hamContent)):
    if hamContent[line][0:9] == "<SUBJECT>":
        numHam += 1
        currLine = line
        allEmailWords = []
        while hamContent[currLine][0:7] != "</BODY>":
            if hamContent[currLine][:1] != "<":
                wordList = hamContent[currLine].split()
                if wordList != []: 
                    for word in wordList:
                        if word.lower() not in allEmailWords:
                            hamVocabFreq[word.lower()] += 1
                            allEmailWords.append(word.lower())
            currLine += 1

"""
TESTING
"""
#calculating priors and posteriors
spamPrior = numSpam/(numSpam + numHam)
hamPrior = numHam/(numSpam + numHam)

posteriors = {}
for feature in vocabList:
    posteriors[feature] = {}
    posteriors[feature]["given Spam"] = (spamVocabFreq[feature] + 1)/ (numSpam + 2)
    posteriors[feature]["given Ham"] = (hamVocabFreq[feature] + 1)/ (numHam + 2)

numCorrect = 0
#processing each email in spam testing set
emailNumber = 0
for line in range (0, len(spamTestContent)):
    if spamTestContent[line][0:9] == "<SUBJECT>":
        emailNumber += 1
        numTestSpam += 1
        featureSet = {}
        for word in vocabList:
            featureSet[word] = False
        currLine = line
        while spamTestContent[currLine][0:7] != "</BODY>":
            if spamTestContent[currLine][:1] != "<":
                wordList = spamTestContent[currLine].split()
                if wordList != []: 
                    for word in wordList:
                        if word.lower() in vocabList: featureSet[word.lower()] = True
            currLine += 1
        
        #Calculations for this specific email
        numTrue = 0
        #probability of being spam
        spamProb = math.log(spamPrior)
        for feature in featureSet:
            if featureSet[feature] == True:
                spamProb += math.log(posteriors[feature]["given Spam"])
                numTrue += 1
            elif featureSet[feature] == False:
                spamProb += math.log(1-posteriors[feature]["given Spam"])
        #probability of being ham
        hamProb = math.log(hamPrior)
        for feature in featureSet:
            if featureSet[feature] == True:
                hamProb += math.log(posteriors[feature]["given Ham"])
            elif featureSet[feature] == False:
                hamProb += math.log(1-posteriors[feature]["given Ham"])
        
        #Output
        classification = "ham"
        if spamProb > hamProb: classification = "spam"
        
        grade = "wrong"
        if classification == "spam": 
            grade = "right"
            numCorrect += 1
        
        print("TEST", emailNumber, str(numTrue) + "/" + str(len(featureSet)), \
              "features true", f'{spamProb:.3f}', f'{hamProb:.3f}', classification, grade)

#processing each email in ham testing set
emailNumber = 0
for line in range (0, len(hamTestContent)):
    if hamTestContent[line][0:9] == "<SUBJECT>":
        emailNumber += 1
        numTestHam += 1
        featureSet = {}
        for word in vocabList:
            featureSet[word] = False
        currLine = line
        while hamTestContent[currLine][0:7] != "</BODY>":
            if hamTestContent[currLine][:1] != "<":
                wordList = hamTestContent[currLine].split()
                if wordList != []: 
                    for word in wordList:
                        if word.lower() in vocabList: featureSet[word.lower()] = True
            currLine += 1
        
        #Calculations for this specific email
        numTrue = 0
        #probability of being spam
        spamProb = math.log(spamPrior)
        for feature in featureSet:
            #print("spam prob is now:", spamProb)
            if featureSet[feature] == True:
                spamProb += math.log(posteriors[feature]["given Spam"])
                numTrue += 1
            elif featureSet[feature] == False:
                spamProb += math.log(1-posteriors[feature]["given Spam"])
        #probability of being ham
        hamProb = math.log(hamPrior)
        for feature in featureSet:
            #print("ham prob is now:", hamProb)
            if featureSet[feature] == True:
                hamProb += math.log(posteriors[feature]["given Ham"])
            elif featureSet[feature] == False:
                hamProb += math.log(1-posteriors[feature]["given Ham"])
        
        #Output
        classification = "ham"
        if spamProb > hamProb: classification = "spam"
        
        grade = "wrong"
        if classification == "ham": 
            grade = "right"
            numCorrect += 1
        
        print("TEST", emailNumber, str(numTrue) + "/" + str(len(featureSet)), \
              "features true", f'{spamProb:.3f}', f'{hamProb:.3f}', classification, grade)

print("Total:", str(numCorrect)+"/"+str(numTestHam+numTestSpam), "emails classified correctly.")