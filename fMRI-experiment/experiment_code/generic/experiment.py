from psychopy import visual, core, event
from psychopy.constants import (NOT_STARTED, STARTED, PAUSED, STOPPED, FINISHED)

# Reaction time analysis should be done with duration as this most closely reflects
# the time between when a stimuli was presented and the user's first response.
def displaylist(E, stimuli):
    # This is designed to display a list of text stim, advancing on 'space'.
    continueRoutine = True
    instrIndx = 0
    thisComponent = stimuli[instrIndx]

    while continueRoutine:
        # start instructions
        if thisComponent.status == NOT_STARTED:
            # keep track of start time/frame
            E.expHandler.addData('stimName', thisComponent.name)
            E.expHandler.addData('start', E.globalClock.getTime())
            E.expHandler.addData('frameStart', E.frameN)  # exact frame index
            E.componentClock.reset()  # keeps track of how long instruction/text is active

            # draw and flip to screen
            thisComponent.draw()
            E.win.flip()
            E.frameN += 1
            thisComponent.status = STARTED
            event.clearEvents(eventType='keyboard')  # clearing any keypress from previous component

        # Check for key response
        thiskeylist = ['space', 'escape']
        keyspressed = event.getKeys(keyList=thiskeylist)
        if any(item in keyspressed for item in thiskeylist):
            if 'escape' in keyspressed: # user pressed escape
                E.win.close()
                core.quit()
            else: # space was pressed, advance instr
                thisComponent.status = STOPPED
                # record data
                E.expHandler.addData('keypress', 'space')
                E.expHandler.addData('duration', E.componentClock.getTime())
                E.expHandler.addData('frameStop', E.frameN)
                E.expHandler.addData('end', E.globalClock.getTime())

        # see if this component is ready to finish
        if thisComponent.status == STOPPED:
            instrIndx += 1
            thisComponent.status = FINISHED
            E.expHandler.nextEntry()

            # check for no more components to display
            if instrIndx >= len(stimuli):
                continueRoutine = False
            else:
                thisComponent = stimuli[instrIndx]


# Note that launchscan is currently not working due to a bug in
# how sound is handled (https://github.com/psychopy/psychopy/issues/2007)
# using the following as part of a work around until next release
def flipWaitScreen(E, action='start'):
    if action is 'start':
        E.expHandler.addData('stimName', E.waitScreen.name)
        E.expHandler.addData('start', E.globalClock.getTime())
        E.expHandler.addData('frameStart', E.frameN)
        E.componentClock.reset()

        E.waitScreen.draw()
        E.win.flip()
        E.frameN += 1
        E.waitScreen.status = STARTED
    elif action is 'stop':
        E.expHandler.addData('keypress', '')
        E.expHandler.addData('duration', E.componentClock.getTime())
        E.expHandler.addData('frameStop', E.frameN)
        E.expHandler.addData('end', E.globalClock.getTime())
        E.waitScreen.status = STOPPED
        E.expHandler.nextEntry()


def waitForTrigger(expSettings):
    # pause execution until a trigger character is detected
    # clears the character from buffer
    thiskeylist = [expSettings.MR_settings['sync'], 'escape']
    triggerSeen = False

    while not triggerSeen:
        keyspressed = event.waitKeys(keyList=thiskeylist)
        if 'escape' in keyspressed:  # user pressed escape
            expSettings.win.close()
            core.quit()
        else:
            triggerSeen = True

    return keyspressed.count(expSettings.MR_settings['sync'])
