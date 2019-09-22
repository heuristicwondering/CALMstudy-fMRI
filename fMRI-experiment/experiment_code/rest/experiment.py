from psychopy import event, core
from psychopy.constants import (NOT_STARTED, PLAYING, FINISHED)
from .. import generic


def runExperiment(E, stimuli):
    continueRoutine = True
    scanDuration = E.MR_settings['runlength']
    vol = 0  # number of volumes collected

    # setting up fixation cross
    thisComponent = stimuli['fixation']

    # wait for first trigger to start experiment
    generic.experiment.flipWaitScreen(E, action='start')
    vol += generic.experiment.waitForTrigger(E)
    generic.experiment.flipWaitScreen(E, action='stop')

    # for figuring out when to end
    scanStart = E.globalClock.getTime()
    scanStop = scanStart + scanDuration

    while continueRoutine:
        # start fixation cross
        if thisComponent.status == NOT_STARTED:
            E.expHandler.addData('stimName', thisComponent.name)
            E.expHandler.addData('start', E.globalClock.getTime())
            E.expHandler.addData('frameStart', E.frameN)  # exact frame index
            E.expHandler.addData('volumeStart', vol)  # start volume
            E.componentClock.reset()  # keeps track of how long component is active

            # clearing any keypresses
            event.clearEvents(eventType='keyboard')

            # draw cross to screen
            thisComponent.draw()
            thisComponent.status = PLAYING
            E.win.flip()
            E.frameN += 1

        # check if out of scan time
        if E.globalClock.getTime() >= scanStop:
            thisComponent.status = FINISHED
            continueRoutine = False

        # end this component and exit
        if thisComponent.status == FINISHED:
            # count triggers
            vol += len(event.getKeys(keyList=E.MR_settings['sync']))

            # record data
            E.expHandler.addData('duration', E.componentClock.getTime())
            E.expHandler.addData('frameStop', E.frameN)
            E.expHandler.addData('end', E.globalClock.getTime())
            E.expHandler.addData('volumeStop', vol)  # stop volume
            E.expHandler.nextEntry()

            # end routine
            continueRoutine = False

        # check for abort
        if event.getKeys(keyList='escape'):
            E.win.close()
            core.quit()