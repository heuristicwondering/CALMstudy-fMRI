from psychopy import event, core
from psychopy.constants import (NOT_STARTED, PLAYING, FINISHED)
from .. import generic
import math


def runExperiment(E, stimuli):
    
    continueRoutine = True
    TR = E.MR_settings['TR']
    scanDuration = E.MR_settings['runlength']
    vol = 0  # number of volumes collected

    # so we don't try to draw when there isn't enough time left
    smallestTime2Draw = E.win.monitorFramePeriod * 0.75
    maxDuration = E.expInfo['movieDuration']

    # setting up first component
    trialIndx = 0
    thisComponentName = E.stimConditions[trialIndx]['VideoFile']
    thisComponentType = E.stimConditions[trialIndx]['TrialType']
    thisComponent = stimuli[thisComponentName]

    # wait for first trigger to start experiment
    generic.experiment.flipWaitScreen(E, action='start')
    vol += generic.experiment.waitForTrigger(E)
    generic.experiment.flipWaitScreen(E, action='stop')

    # for ending if we run out of time
    scanStart = E.globalClock.getTime()
    scanStop = scanStart + scanDuration
    
    while continueRoutine:
        # start movie
        if thisComponent.status == NOT_STARTED:
            E.expHandler.addData('stimName', thisComponent.name)
            E.expHandler.addData('stimType', thisComponentType)
            E.expHandler.addData('start', E.globalClock.getTime())
            E.expHandler.addData('frameStart', E.frameN)  # exact frame index
            E.expHandler.addData('volumeStart', vol) # start volume
            E.componentClock.reset()  # keeps track of how long movie is active

            # there seems to be a bug with psychopy
            # need this in order for changes in size to take effect
            thisComponent.size *= 1

            thisComponent.setAutoDraw(True)
            thisComponent.seek(0)  # rewind if needed
            thisComponent.status = PLAYING

            # clearing any keypress from previous component
            event.clearEvents(eventType='keyboard')

            # start a timer and counter to sync movie stop to trigger
            actualTriggers = 1
            if thisComponent.duration < maxDuration:
                expectedTriggers = math.floor(thisComponent.duration / TR)
            else:
                expectedTriggers = math.floor(maxDuration / TR)
            thisDuration = expectedTriggers * TR
            E.MRClock.reset(thisDuration)

        # flip movie to screen
        if thisComponent.status == PLAYING:
            E.win.flip()
            E.frameN += 1

        # check if out of scanning time
        if E.globalClock.getTime() >= scanStop:
            thisComponent.status = FINISHED
            continueRoutine = False

        # no more time left for this movie
        if E.MRClock.getTime() <= smallestTime2Draw:
            # count triggers seen during this component
            actualTriggers += len(event.getKeys(keyList=E.MR_settings['sync']))

            # check if need to wait for next trigger
            while actualTriggers < expectedTriggers:
                actualTriggers += generic.experiment.waitForTrigger(E)

            vol += actualTriggers
            thisComponent.status = FINISHED

        # end movie and get ready for next
        if thisComponent.status == FINISHED:
            # record data
            E.expHandler.addData('duration', E.componentClock.getTime())
            E.expHandler.addData('frameStop', E.frameN)
            E.expHandler.addData('end', E.globalClock.getTime())
            E.expHandler.addData('volumeStop', vol)  # stop volume
            E.expHandler.nextEntry()

            # stop video
            thisComponent.setAutoDraw(False)
            thisComponent.pause()  # this does not stop the audio stream
            thisComponent.seek(thisComponent.duration)  # but this does
            thisComponent.status = NOT_STARTED
            trialIndx += 1

            # check for no more components to display
            if trialIndx >= len(E.stimConditions):
                continueRoutine = False
            else:
                thisComponentName = E.stimConditions[trialIndx]['VideoFile']
                thisComponentType = E.stimConditions[trialIndx]['TrialType']
                thisComponent = stimuli[thisComponentName]

        # check for abort
        if event.getKeys(keyList='escape'):
            E.win.close()
            core.quit()