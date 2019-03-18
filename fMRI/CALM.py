# CALM study for fMRI
# Version 0.01 -- Alpha.
# Written by Megan Finnegan and Chris Perriello 2/14/2019
# Contact Megan at heuristicwondering@gmail.com
#
# Written for Psychopy 3.0.3 with Python 3.6.3
#   - This may run in other versions, but will likely not behave nicely.
#
# Windows 10 does not alway track the active window properly. To be sure that
# the proper window is in focus for this experiment, don't bring other programs 
# or the desktop into focus during code execution.


from __future__ import absolute_import, division

import psychopy
psychopy.useVersion('latest')

from psychopy import locale_setup, visual, monitors, core, data, event, logging, sound, gui, info
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding
import math

# Functions and classes for building stimuli custom to this experiment
from experiment import stimuliSetup, executeInstructions, executeTrials

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

#-------------------------------------------------------------------------------------#
# -----Setting up Experiment Parameters-------
RUNLENGTH = 1000 # Time in seconds of planned run.

# Store info about the experiment session
expName = u'socevalPilot'
dlg = gui.Dlg(title=expName)
dlg.addField('participant','Jayne Doe')
dlg.addField('Scan Type', choices=['Practice', 'Scan'])
dlg.addText('Only relevant for scan type \'Scan\'')
dlg.addField('session','##')
dlg.addField('Instuction Length', choices=['long', 'short'])
dlg.addText('Planned Scan Time: ' + str(RUNLENGTH) + ' seconds')
expValues = dlg.show()

if dlg.OK == False:
    core.quit()  # user pressed cancel

expKeys = ['participant', 'scantype', 'session',  'instrlen']
expInfo = dict( zip( expKeys, expValues ) )
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# settings for launchScan:
MR_settings = {
    'TR': 1.000,     # duration (sec) per whole-brain volume
    'volumes': RUNLENGTH,  # number of whole-brain 3D volumes per scanning run
    'sync': 'equal', # character to use as the sync timing event; assumed to come at start of a volume
    'skip': 0,       # number of volumes lacking a sync pulse at start of scan (for T1 stabilization)
    'sound': True    # in test mode: play a tone as a reminder of scanner noise
    }

# Loading the list of stimuli to present and updating expInfo
if expInfo['scantype'] == 'Practice':
    
    stimFileGuided = _thisDir + os.sep + u'stimuliLists' + os.sep + u'guided_vids.csv'
    stimConditionsGuided = data.importConditions(stimFileGuided)
    
    stimFile = _thisDir + os.sep + u'stimuliLists' + os.sep + u'se_run00.csv'
    expInfo['session'] = 'practice'
    
elif expInfo['scantype'] == 'Scan':
    
    thisrun = expInfo['session']
    stimConditionsGuided = []
    
    # Truncate string to last two digits
    # NTS: Notify user and let them change their mind in future versions
    thisrun = thisrun[-2:] if len(thisrun) > 2 else thisrun
    stimFile = _thisDir + os.sep + u'stimuliLists' + os.sep + u'se_run' + thisrun + u'.csv'
    
    expInfo['session'] = thisrun

stimConditions = data.importConditions(stimFile)

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s_%s' % (expInfo['participant'], expInfo['session'], expName, expInfo['date'])
vidpath = _thisDir + os.sep + u'videos' + os.sep # Assuming all movies are here

# An ExperimentHandler isn't essential but helps with data saving
# Since this will only ever handle 1 run and stimuli will
# be presented sequentially, not bothering with a TrialHandler.
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=(filename))

logFile = logging.LogFile(filename+'.log', level=logging.EXP) # save a log file for detail verbose info
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

#-------------------------------------------------------------------------------------#
# -----Setting up Window-------

# Setup the Window <-- subjectMonitor NEEDS TO BE ADJUSTED FOR MONITOR USING! 
expMonitor = monitors.Monitor('subjectMonitor')
SCREEN_SIZE = (1920,1080)   # screen res

# Using secondary monitor NEEDS TO BE ADJUSTED FOR MONITOR USING! 
win = visual.Window(
    SCREEN_SIZE, fullscr=True, screen=1,
    allowGUI=False, allowStencil=False,
    monitor=expMonitor, 
    color=[-0.569,-0.514,-0.373], colorSpace='rgb',
    blendMode='avg', useFBO=True)

# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

#-------------------------------------------------------------------------------------#
# Initializing Stimuli and Clocks
stimuli = stimuliSetup.defineStim(win, stimConditions, 
    extraStimCond = stimConditionsGuided, path2movies = vidpath)

globalClock = core.Clock() # Keep track of beginning of time
MRClock = core.Clock() # Keep track of the start of a scan session
instructionsClock = core.Clock() # Keep track of start of instruction components
experimentClock = core.Clock() # Keep track of start of experiment components

#-------------------------------------------------------------------------------------#
# -----Bounds Checking - Verify that planned stimuli do not exceed expected run time---
if expInfo['scantype'] == 'Scan': 
    # This is the presumed trial order
    TR = MR_settings['TR']
    estScanDuration = 0
    for trial in stimConditions:
        astr = trial['ITI'] - trial['ITI'] % TR
        cue = 2 - 2 % TR
        fix1 = trial['ISI'] - trial['ISI'] % TR
        movdur = stimuli['movies'].MovieStimDict[trial['VideoFile']].duration
        mov = movdur - movdur % TR
        fix2 = 3 - 3 % TR
        rating = 3 - 3 % TR
        
        estScanDuration += astr + cue + fix1 + mov + fix2 + rating
    
    if estScanDuration != RUNLENGTH:
        dlg = gui.Dlg(title='DURATION WARNING')
        dlg.addText('Warning!\n\nThe estimated scan length is ' + 
            str(estScanDuration) + ' seconds but the predefined ' + 
            'scan length has been set to ' + str(RUNLENGTH) + 
            ' seconds.\n\nAre you sure you want to continue?\n\n' + 
            'Experiment will run until there are no more trials ' +
            'to show or the predefined scan time is reached, \n' + 
            'whichever comes first. You may end up losing stimuli ' + 
            'presentations or wasting scan time.\n\n' + 
            'Press OK to continue.')
        dlg.show()
        
        if dlg.OK == False:
            core.quit()  # user pressed cancel
        
        logging.warning('Estimated time for stimuli is ' + str(estScanDuration) + 
            ', but predefined time was set to ' + str(RUNLENGTH))

#-------------------------------------------------------------------------------------#
# These are encapsulated into functions because while practice 
# and experiment runs are very similar, they are different 
# enough to make code reuse not so straight forward. This is 
# done to help keep the code readable during alpha development, 
# but future versions should integrate these into single functions.
#
#
if expInfo['scantype'] == 'Practice':
    #########################################################################################
    # This is the official start of the experiment. Everything above is just setup.         #
    # Note that the call to setup functions should be done right before the call to execute #
    # It is mostly just resetting code that is shared across functions and should be        #
    # very fast. If you need to do something that takes some time, add it to the stimuli    #
    # setup and not here.                                                                   #
    #########################################################################################
    
    instructionComponents = executeInstructions.setupInstructions(stimuli, instrType='Practice')
    globalClock.reset() # start the global clock from 0.
    numFlips = executeInstructions.displayInstructions(win, instructionComponents, globalClock, 
       instructionsClock, thisExp)
    
    experimentComponents = executeTrials.setupExperiment(stimuli, scantype='Practice')
    numFlips = executeTrials.runGuidedPracticeExperiment(win, experimentComponents, globalClock,
       experimentClock, stimConditionsGuided, thisExp, frameN = numFlips)
    
    instructionComponents = executeInstructions.setupInstructions(stimuli, instrType='Transition')
    numFlips = executeInstructions.displayInstructions(win, instructionComponents, globalClock, 
        instructionsClock, thisExp, frameN = numFlips)
    
    experimentComponents = executeTrials.setupExperiment(stimuli, scantype='Scan')
    numFlips = executeTrials.runExperiment(win, experimentComponents, globalClock,
       experimentClock, stimConditions, thisExp, MR_settings, MRClock, scantype='Practice', 
       frameN = numFlips)
       
    instructionComponents = executeInstructions.setupInstructions(stimuli, instrType='practiceThankyou')
    numFlips = executeInstructions.displayInstructions(win, instructionComponents, globalClock, 
        instructionsClock, thisExp, frameN = numFlips)
    
elif expInfo['scantype'] == 'Scan':
    # Current behavior is that instructions need to be advanced through with 'space' 
    # and task will not start listening for trigger pulses (i.e. it won't start) until 
    # these have all been cycled through. A blank screen will appear when the code begins 
    # listening for the first trigger.
    #
    instructionComponents = executeInstructions.setupInstructions(stimuli, instrType=expInfo['instrlen'])
    globalClock.reset() # start the global clock from 0.
    numFlips = executeInstructions.displayInstructions(win, instructionComponents, globalClock, 
       instructionsClock, thisExp)
    
    experimentComponents = executeTrials.setupExperiment(stimuli, scantype='Scan')
    numFlips = executeTrials.runExperiment(win, experimentComponents, globalClock,
       experimentClock, stimConditions, thisExp, MR_settings, MRClock, scantype='Scan', 
       frameN = numFlips)
    
    instructionComponents = executeInstructions.setupInstructions(stimuli, instrType='Thankyou')
    numFlips = executeInstructions.displayInstructions(win, instructionComponents, globalClock, 
        instructionsClock, thisExp, frameN = numFlips)
    

win.close()
core.quit()

