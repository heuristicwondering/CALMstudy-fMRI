# CALM study for fMRI
# Version 0.02
# Written by Megan Finnegan
# Contact Megan at heuristicwondering@gmail.com
#
# Written for Psychopy 3.0.3 with Python 3.5.5

from psychopy import sound # MF - needed to work around issue #2662 and related #2230
from psychopy import core
import os

# Functions and classes for building stimuli custom to this experiment
from experiment_code import generic, infant
from experiment_code import rest


# Ensure that relative paths start from the same directory as this script
thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(thisDir)

# Creating an experiment object that keeps track of all my settings.
# These methods must be called in this order.
thisExperiment = generic.setup.ExperimentSettings(thisDir)
thisExperiment.setParameters()      # get basic settings based on user input
thisExperiment.setMRsettings()      # sets the scan parameters
thisExperiment.setMonitor()         # gets the monitor settings
thisExperiment.setWindow()          # setup the the Window
thisExperiment.createWaitScreen()   # to wait for first trigger pulse
thisExperiment.setClocks()          # initialize experiment clocks

#-------------------------------------------------------------------------------#
# Many relevant settings have been hard coded for our specific MR setup         #
# however you can simply rewrite the relevant attributes to be applicable       #
# to your experiment immediately after the function that sets them and          #
# *before* the next function is called. In a future release, parameters you     #
# would likely want to change will be moved to json files for easier editing.   #
#-------------------------------------------------------------------------------#

# ------- Initializing Stimuli ------- #
if thisExperiment.expInfo['scantype'] == 'Task':

    instructions = infant.setup.defineInstructions(thisExperiment.win)
    stimuli = infant.setup.defineStim(thisExperiment.win,
                                      thisExperiment.stimConditions,
                                      thisExperiment.vidpath)
    thankyou = infant.setup.defineThankyou(thisExperiment.win)

elif thisExperiment.expInfo['scantype'] == 'Rest':

    instructions = rest.setup.defineInstructions(thisExperiment.win)
    stimuli = rest.setup.defineStim(thisExperiment.win)
    thankyou = rest.setup.defineThankyou(thisExperiment.win)

elif thisExperiment.expInfo['scantype'] == 'Rest-Alternate':

    instructions = rest.setup.defineAlternateInstructions(thisExperiment.win)
    stimuli = rest.setup.defineStim(thisExperiment.win)
    thankyou = rest.setup.defineThankyou(thisExperiment.win)


# Bounds checking videos
if thisExperiment.expInfo['scantype'] == 'Task':
    infant.setup.checkBounds(thisExperiment, stimuli)

#-----------------------------------------------------------------------------------#
# -------------------------------- Run Experiment --------------------------------- #
#####################################################################################
#   This is the official start of the experiment. Everything above is just setup.   #
#   If you need to do something that takes some time, add it to the stimuli setup   #
#   and not here.                                                                   #
#####################################################################################

thisExperiment.globalClock.reset() # start the global clock from 0.
thisExperiment.frameN = 0 # number of frames flipped to the screen

generic.experiment.displaylist(thisExperiment, instructions)  # display instructions

if thisExperiment.expInfo['scantype'] == 'Task':
    infant.experiment.runExperiment(thisExperiment, stimuli)
elif (thisExperiment.expInfo['scantype'] == 'Rest'
    or thisExperiment.expInfo['scantype'] == 'Rest-Alternate'):
    rest.experiment.runExperiment(thisExperiment, stimuli)

generic.experiment.displaylist(thisExperiment, thankyou)  # display thank you

thisExperiment.win.close()
core.quit()

