#!/usr/bin/env python
import csv
from collections import deque

NUM_OF_CANDIDATES = 8

#run voting rounds
def vote(candidates):
    winner = None
    i = 1
    print('\n\nInitial vote:\n')
    displayState(candidates)
    while winner == None:
        print(''.join(['\n\nround ', str(i), ':\n']))
        candidates, winner = aRound(candidates)
        voterCounts = [len(x['voters']) for x in candidates]
        if min(voterCounts) == max(voterCounts) and len(candidates) > 1:
            return "There has been a draw. Determine winner manually."
        i += 1
    return "Winner: " + winner

#define voting round
def aRound(candidates):
    #check for majority win
    sum = 0;
    for candidate in candidates:
        sum += len(candidate['voters'])
    for candidate in candidates:
        if len(candidate['voters']) > sum/2:
            return candidates, candidate['name']

    tempCandidates = deque(candidates)
    minVotes = min([len(x['voters']) for x in candidates])

    #reallocate votes
    toRemove = deque()
    for candidate in tempCandidates:
        if len(candidate['voters']) == minVotes:
            toRemove.append(candidate['name'])

    for candidate in tempCandidates:
        if minVotes == 0:
            break
        if len(candidate['voters']) == minVotes:
            for i, _ in enumerate(deque(candidate['voters'])):
                foundNewCandidate = False
                while not foundNewCandidate:
                    if len(candidate['voters'][i]) == 0:
                        break
                    newCandidate = candidate['voters'][i].popleft()
                    for candidate2 in candidates:
                        if candidate2['name'] == newCandidate not in toRemove:
                            foundNewCandidate = True
                            candidate2['voters'].append(candidate['voters'][i])

    #remove losing candidates
    for candidate in candidates:
        if candidate['name'] in toRemove:
            tempCandidates.remove(candidate)
            print(candidate['name']+' lost\n')

    candidates = deque(tempCandidates)

    displayState(candidates)

    #return resulting list
    return candidates, None

def displayState(candidates):
    aSum = 0
    for candidate in candidates:
        aSum += len(candidate['voters'])
        print(' '.join([candidate['name'], str(len(candidate['voters'])), '\n']))
    print(''.join(['Total: ', str(aSum)]))

candidates = deque()
voters = deque()

#load CSV of votes
inFile = open('votes.csv', 'rb')
reader = csv.reader(inFile)
rowNum = 0
for row in reader:
    if rowNum == 0:
        header = row
        rowNum += 1
        continue
    voter = deque()
    for rank in xrange(1,NUM_OF_CANDIDATES):
        colNum = 0
        for value in row:
            if rowNum == 1 == rank:
                candidate = {'name':header[colNum], 'voters':deque()}
                candidates.append(candidate)
            if str(value) == str(rank):
                voter.append(header[colNum])
            colNum += 1
    voters.append(voter)
    rowNum += 1

for voter in voters:
    for candidate in candidates:
        if voter[0] == candidate['name']:
            candidate['voters'].append(voter)

inFile.close()

#report winner
winner = vote(candidates)
print(''.join(['\n', winner, '\n\n']))
