"""
    Create template csv files of randomized trial blocks.
    1. Each block contains one and only one of every trial type
    2. Trials are fully randomized within blocks
    3. Blocks are partially randomized to prevent presenting the same trial twice in a row.
    4. Each block represent a unique trial randomization (i.e. randomly sampled trial permutations without replacement).
    5. Block are drawn from remaining permutations,
        excluding those that would present the same trial twice in a row across blocks.
    6. If multiple file names map onto the same trial type,
        then one of these files will be picked at random in the final run list.
    7. Be aware that this code does not do much error checking and assumes that you've picked reasonable values
        Some attempts to add bounds checking has been added, but is not fully tested.
"""
import os
import itertools
import csv
from random import randint, sample

###------------- THINGS YOU MIGHT WANT TO CHANGE -------------###
numRuns = 2  # number of runs to create
numBlocks = 6  # number of blocks in a run

# For creating csv files -- this maps each file name onto a stimuli type
# it is possible to have multiple files map to the same type. Case sensitive.
vidFileNames = ['###_pos.mp4', '###_neg.mp4',
                'other_pos.mp4', 'other_neg.mp4', 'scrambled-###_pos.mp4', 'scrambled-###_neg.mp4']
trialTypes = ['InfOwnPos', 'InfOwnNeg', 'InfOtherPos', 'InfOtherNeg', 'Control', 'Control']
###--------------------------- END ---------------------------###


###--------------- THINGS YOU SHOULDN'T CHANGE ---------------###


class NoUniqueBlocks( Exception ):
    pass


class NoMoreBlocks( Exception ):
    pass

def setifyDuplicates(stimTypes, stimNames):
    # creates type to filenames dictionary so that
    # if multiple vidFileNames map to the same trial type,
    # can randomly choose which file it will resolve to for each trial
    mapping = dict()
    for tp, nm in zip(stimTypes, stimNames):
        if mapping.get(tp) is None:  # create entry
            mapping.update({tp: {nm}})
        else:  # update existing entry
            mapping[tp].add(nm)

    return mapping


def reformatRun4File(thisRun, stimTypes, trialMapping):
    reformatedRun = []

    for thisblock in thisRun:
        for thistrial in thisblock:
            thistype = stimTypes[thistrial]
            thisname = ''.join(sample(trialMapping[thistype], 1))
            reformatedRun.append([thisname, thistype])

    return reformatedRun


def writeRun2File(csvFile, csvHeader, thisRun):
    with open(csvFile, 'w') as stimFile:
        stimWriter = csv.writer(stimFile, delimiter=',')
        stimWriter.writerow(csvHeader)
        for row in thisRun:
            stimWriter.writerow(row)


numTrials = len(set(trialTypes))  # number of stimuli types in a block
trialMapping = setifyDuplicates(trialTypes, vidFileNames)

# For creating csv files
csvHeader = ['VideoFile', 'TrialType']

# Ensure that relative paths start from the same directory as this script
thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(thisDir)

csvDir = thisDir + os.sep + 'stimuli-templates' + os.sep
if not os.path.exists(csvDir):
    os.makedirs(csvDir)
if len(os.listdir(csvDir)) != 0:
    print('\nThere are files in the stimuli-template folder already.\n'
          'I do not want to overwrite them, so please move them out of \n'
          'this directory. I will not co-operate until you do this.\n\n'
          'BBBYYYYEEEEE!!!!!\n')
    quit()

# all possible unique blocks
allBlocks = list(itertools.permutations(range(0, numTrials)))

try:
    for run in range(0,numRuns):
        runList = list()
        if len(allBlocks) == 0:  # no blocks to choose from end now
            raise NoMoreBlocks

        # pick a random block to start
        runList.append(allBlocks.pop(randint(0, len(allBlocks)-1)))

        # adding the rest of the blocks to this run list.
        for block in range(1, numBlocks):
            if len(allBlocks) == 0:  # no blocks to choose from end now
                allBlocks.append(runList)  # returning unfinished run list to pool. Will print leftovers before exit.
                raise NoMoreBlocks

            # only picking next block from blocks that don't start with the same trial the previous ended with
            availableBlockIndices = [i for i, b in enumerate(allBlocks) if b[0] != runList[-1][-1]]

            if len(availableBlockIndices) == 0:
                raise NoUniqueBlocks

            nextBlockIndx = availableBlockIndices[randint(0, len(availableBlockIndices)-1)]
            nextBlock = allBlocks.pop(nextBlockIndx)
            runList.append(nextBlock)

        # write this run to file
        csvFile = csvDir + 'CALM###_run{0:02d}.csv'.format(run)
        refrmtdRunList = reformatRun4File(runList, trialTypes, trialMapping) # translate indices to a names/type list
        writeRun2File(csvFile, csvHeader, refrmtdRunList)

except (NoUniqueBlocks, NoMoreBlocks) as e:
    print('\nRan out of blocks to create runs with. Ending early.\n')


if len(allBlocks) > 0: # unused blocks. printing to file
    print(('\nPrinting remaining {0:d} unique blocks (of {1:d} trials each) ' +
          'that were not used to file for your reference.\n').format(len(allBlocks), numTrials))
    print('\nThey can be found in the file \'leftovers.csv\'\n')
    csvFile = csvDir + 'leftovers.csv'
    refrmtdRunList = reformatRun4File(allBlocks, trialTypes, trialMapping)  # translate indices to a names/type list
    # just to make the file a little more readable, put in blank rows between blocks
    indx = list(range(0, len(refrmtdRunList)-1, numTrials))
    for i in reversed(indx):
        refrmtdRunList.insert(i, ['',''])

    writeRun2File(csvFile, csvHeader, refrmtdRunList)
