import psychopy
psychopy.useVersion('latest') #Sets up latest version of psychopy

from psychopy import core, event
from psychopy.constants import (NOT_STARTED, STARTED, STOPPED, FINISHED)

# ------Prepare to start Instructions-------
def setupInstructions(stimuli, instrType='Practice'): # Picks which stimuli to present
    if instrType == 'Resting':
        instructionComponents = [stimuli.get(key) for key in ['Instr1', 'Instr2', 'Instr3', 'Instr7']]
    elif instrType == 'RestingEnd':
        instructionComponents = [stimuli.get(key) for key in ['thanks1']]
    elif instrType == 'Primary':
        instructionComponents = [stimuli.get(key) for key in ['Instr4', 'Instr5', 'Instr6', 'Instr7']]
    elif instrType == 'PrimaryEnd':
        instructionComponents = [stimuli.get(key) for key in ['thanks2']]
    elif instrType == 'Fixation':
        instructionComponents = [stimuli.get(key) for key in ['fixation']]
    
    # Keeps track of which components have finished
    for thisComponent in instructionComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    return instructionComponents

# Reaction time analysis should be done with duration as this most closely reflects 
# the time between when a stimuli was presented and the user's first response.
def displayInstructions(win, instructionComponents, globalClock, 
    instructionsClock, thisExp, frameN = 0):
    # This is designed to display a list of text stim, advancing on 'space'.
    #
    # -----Presenting Instructions-------
    t = 0
    continueRoutine = True
    instrIndx = 0
    thisComponent = instructionComponents[instrIndx]
    
    while continueRoutine:
        # start instructions    
        if thisComponent.status == NOT_STARTED:
            # keep track of start time/frame
            thisExp.addData('stimType', thisComponent.name )
            thisExp.addData('start', globalClock.getTime())
            thisExp.addData('frameStart', frameN) # exact frame index
            instructionsClock.reset() # keeps track of how long instruction set active
            thisComponent.setAutoDraw(True)
            thisComponent.status = STARTED
            event.clearEvents(eventType='keyboard') # clearing any keypress from previous component
        
        # Check for key response
        if thisComponent.status == STARTED:
            thiskeylist = ['space', 'escape']
            keyspressed = event.getKeys(keyList=thiskeylist)
            
            if len(keyspressed) >= 1: # At least one key was pressed
                firstKey = keyspressed[0] # Only taking first response
                if firstKey == 'escape': # check for quit (the Esc key) - otherwise, it is a space and advance instr
                    win.close()
                    core.quit()
                else
                    thisComponent.status = STOPPED
                
                # If component stopped due to key press, record data
                if thisComponent.status == STOPPED:
                    thisExp.addData('keypress', firstKey)
                    thisExp.addData('RT', instructionsClock.getTime())
                    thisExp.addData('duration', instructionsClock.getTime())
                    thisExp.addData('frameStop', frameN)
                    thisExp.addData('end', globalClock.getTime())
        
        # This component is ready to finish
        if thisComponent.status == STOPPED:
            instrIndx = instrIndx + 1
            thisComponent.status = FINISHED
            thisComponent.setAutoDraw(False)
            thisExp.nextEntry()
        
        # check for quit (the Esc key)
        if event.getKeys(keyList=['escape']):
            win.close()
            core.quit()
        
        # Refresh the screen if this component has something to draw
        if continueRoutine and thisComponent.status == STARTED:
            win.flip()
            frameN = frameN + 1 # number of completed frames (0 is the first frame)
        
        # Check for no more components to display
        if instrIndx >= len(instructionComponents):
            continueRoutine = False
        else:
            thisComponent = instructionComponents[instrIndx]
        
    return frameN
