import psychopy
psychopy.useVersion('latest')

from psychopy import core, event
# NTS: get rid of constants not using when code is finished
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, 
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)


def setupInstructions(stimuli, instrType='Practice'):
    # ------Prepare to start Instructions-------
    # Picking which stimuli to present
    if instrType == 'Practice':
        instructionComponents = [stimuli.get(key) for key in ['Instr1', 
            'Instr2', 'Instr3', 'Instr4', 'Instr5', 
            'ratingbar', 'Instr6']]
    elif instrType == 'Transition':
        instructionComponents = [stimuli.get(key) for key in ['Instr8', 
            'Instr9']]
    elif instrType == 'practiceThankyou':
        instructionComponents = [stimuli.get(key) for key in ['thankyou1']]
    elif instrType == 'long':
        instructionComponents = [stimuli.get(key) for key in ['Instr1', 
            'Instr2', 'Instr3', 'Instr4', 'Instr5', 'ratingbar', 
            'Instr10', 'Instr11', 'Instr9']]
    elif instrType == 'short':
        instructionComponents = [stimuli.get(key) for key in ['Instr12', 
            'Instr13', 'Instr9']]
    elif instrType == 'Thankyou':
        instructionComponents = [stimuli.get(key) for key in ['thankyou2']]
    
    # to keep track of which components have finished
    for thisComponent in instructionComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    return instructionComponents

# Reaction time analysis should be done with duration as this most closely reflects 
# the time between when a stimuli was presented and the user's first response.
def displayInstructions(win, instructionComponents, globalClock, 
    instructionsClock, thisExp, frameN = 0):
    # This is designed to display a list of text stim, advancing on 'space', if there
    # is a ratingbar object, then it will be shown 3 times, advancing on 'space'.
    #
    # -----Presenting Instructions-------
    t = 0
    continueRoutine = True
    instrIndx = 0
    ratingbarIndx = 1 # Ratingbar will be presented 3 times
    thisComponent = instructionComponents[instrIndx]
    
    while continueRoutine:
        # start instructions    
        if thisComponent.status == NOT_STARTED:
            # keep track of start time/frame
            thisExp.addData('stimType', thisComponent.name )
            thisExp.addData('start', globalClock.getTime())
            thisExp.addData('frameStart', frameN) # exact frame index
            instructionsClock.reset() # keep track of how long instruction set active
            thisComponent.setAutoDraw(True)
            thisComponent.status = STARTED
            event.clearEvents(eventType='keyboard') # clearing any keypress from previous component
        
        # Check for key response
        if thisComponent.status == STARTED:
            if thisComponent.name == 'ratingbar':
                ratingsAllowed = ["1", "2", "3", "4", "5"]
                thiskeylist = ratingsAllowed + ['space', 'escape']
            else: # only listen for 'space' on all other components
                thiskeylist = ['space', 'escape']
            
            keyspressed = event.getKeys(keyList=thiskeylist)
            
            if len(keyspressed) >= 1: # At least one key was pressed
                firstKey = keyspressed[0] # Only taking first response
                if firstKey == 'escape': # check for quit (the Esc key)
                    win.close()
                    core.quit()
                
                if thisComponent.name == 'ratingbar':
                    if firstKey == 'space':
                        # only advance ratingbar component if a rating has been given
                        if thisComponent.responseGiven == True:
                            thisComponent.status = STOPPED
                            
                    else: # display the rating -- already checked for esc and space
                        thisComponent.displayRating(int(firstKey))
                        thisComponent.responseGiven = True
                        thisComponent.RT = instructionsClock.getTime()
                        
                else: # All other components are instruction screens and a keypress means advance
                    thisComponent.status = STOPPED
                
                # If component stopped due to key press, record data
                if thisComponent.status == STOPPED:
                    if thisComponent.name == 'ratingbar':
                        thisExp.addData('keypress', thisComponent.currentResponse)
                        thisExp.addData('RT', thisComponent.RT)
                    else:
                        thisExp.addData('keypress', firstKey)
                        thisExp.addData('RT', instructionsClock.getTime())
                    thisExp.addData('duration', instructionsClock.getTime())
                    thisExp.addData('frameStop', frameN)
                    thisExp.addData('end', globalClock.getTime())
        
        # This component is ready to finish
        if thisComponent.status == STOPPED:
            if thisComponent.name == 'ratingbar':
                if ratingbarIndx < 3: # If the rating hasn't been presented x3, keep going
                    thisComponent.status = NOT_STARTED
                    thisComponent.responseGiven = False
                    thisComponent.hideRating()
                    ratingbarIndx = ratingbarIndx + 1
                else:
                    instrIndx = instrIndx + 1
                    thisComponent.status = FINISHED
                    thisComponent.setAutoDraw(False)
            else:
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
