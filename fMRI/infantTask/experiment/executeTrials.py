import psychopy
psychopy.useVersion('latest')

from psychopy import core, event
from psychopy.hardware.emulator import launchScan
# NTS: get rid of constants not using when code is finished
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, 
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

def setupExperiment(stimuli, scantype='Practice'):
    # ------Prepare to start Experiment-------
    # Picking which stimuli to present
    #
    # Note that unlike instruction setup which returned a list taking 
    # advantage of a fixed presentation order that could be iterated over, 
    # experiment setup returns a dict to allow more flexible behavior.
    #
    # NTS: Later versions should implement a dict in both setups -- part of code integration
    if scantype == 'Practice':
        experimentComponents = {k: stimuli[k] for k in ['asterisks', 
            'cue', 'fixation', 'movies', 'ratingbar', 'Instr7']}
    elif scantype == 'Scan':
        experimentComponents = {k: stimuli[k] for k in ['asterisks', 
            'cue', 'fixation', 'movies', 'ratingbar']}
    
    # to keep track of which components have finished
    for _, thisComponent in experimentComponents.items():
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
        if hasattr(thisComponent, 'name'):
            # Since it may have been used previously
            if thisComponent.name == 'ratingbar': 
                thisComponent.responseGiven = False
                thisComponent.hideRating()
    
    return experimentComponents

def runGuidedPracticeExperiment(win, experimentComponents, globalClock,
        experimentClock, stimConditions, thisExp, frameN = 0):
    # -----Presenting Guided Practice-------
    continueRoutine = True
    stimIndx = 0 # Which stimCondition to use.
    trialPart = 0 # Which part of the trial we're on
    trialOrder = ['asterisks', 'cue', 'fixation', 'movies', 
        'fixation', 'ratingbar', 'Instr7'] # This is the order of stimuli for a single trial.
    firstFixation = True # Different behavior needed whether this is 1st or 2nd fixation in trialOrder
    
    while continueRoutine:
        thisComponent = experimentComponents[trialOrder[trialPart]]
        
        # start experiment component 
        if thisComponent.status == NOT_STARTED:
            print('Component name (start): ' + thisComponent.name) # debugging
            print('Start time: ' + str(globalClock.getTime()))
            
            # keep track of start time/frame
            thisComponent.status = STARTED
            thisExp.addData('stimType', thisComponent.name )
            thisExp.addData('start', globalClock.getTime())
            thisExp.addData('frameStart', frameN) # exact frame index
            experimentClock.reset() # keep track of how long component is active
            event.clearEvents(eventType='keyboard') # clearing any keypress from previous component
            
            # setting up component specific parameters
            if thisComponent.name == 'asterisks':
                duration = None # how long to keep this stim on screen, None means wait for response
                thisComponent.text = stimConditions[stimIndx]['Asterisk']
                thisComponent.setAutoDraw(True)
            elif thisComponent.name == 'cue':
                duration = None
                thisComponent.text = stimConditions[stimIndx]['Cue']
                thisComponent.setAutoDraw(True)
            elif thisComponent.name == 'fixation':
                if firstFixation:
                    duration = stimConditions[stimIndx]['ISI']
                    firstFixation = False
                else:
                    duration = 3
                    firstFixation = True # resetting
                thisComponent.setAutoDraw(True)
                win.flip()
            elif thisComponent.name == 'movies': # pick which movie to play
                movieName = stimConditions[stimIndx]['VideoFile']
                movie2play = thisComponent.MovieStimDict[movieName]
                duration = movie2play.duration
                thisExp.addData('VidName', movieName )
                movie2play.setAutoDraw(True)
            elif thisComponent.name == 'ratingbar':
                duration = 3
                thisComponent.setAutoDraw(True)
            elif thisComponent.name == 'Instr7':
                duration = None
                thisComponent.setAutoDraw(True)
            
        # dealing with key presses for this component.
        if thisComponent.status == STARTED:
            # Check for key press
            thiskeylist = None
            if thisComponent.name == 'asterisks' or thisComponent.name == 'cue' \
                or thisComponent.name == 'Instr7':
                thiskeylist = ['space', 'escape']
            elif thisComponent.name == 'fixation' or thisComponent.name == 'movies':
                thiskeylist = ['escape']
            elif thisComponent.name == 'ratingbar':
                ratingsAllowed = ["1", "2", "3", "4", "5"]
                thiskeylist = ratingsAllowed + ['escape']
            
            keyspressed = event.getKeys(keyList=thiskeylist)
            
            # At least one key was pressed. Do something with it.
            if len(keyspressed) >= 1: 
                firstKey = keyspressed[0] # Only taking first response
                
                if firstKey == 'escape': # check for quit (the Esc key)
                    win.close()
                    core.quit()
                if thisComponent.name == 'asterisks' or thisComponent.name == 'cue' \
                    or thisComponent.name == 'Instr7':
                    # Since already checked for esc, then space must have been pressed
                    # Advance to next component.
                    thisComponent.status = STOPPED
                    thisExp.addData('keypress', firstKey)
                    thisExp.addData('RT', experimentClock.getTime())
                elif thisComponent.name == 'ratingbar':
                    if not thisComponent.responseGiven:
                        # Only record a response if one not already given.
                        thisComponent.displayRating(int(firstKey))
                        thisComponent.responseGiven = True
                        thisExp.addData('keypress', firstKey)
                        thisExp.addData('RT', experimentClock.getTime())
        
        # only run this component for as long as duration.
        if thisComponent.status == STARTED:
            if not duration:
                # Just so time4stim to be up is always more than how long the cue has been up
                time4stim = experimentClock.getTime() + 1
            else:
                # So we don't try to draw when there isn't enough time left
                time4stim = duration - win.monitorFramePeriod * 0.75
            
            if experimentClock.getTime() > time4stim: # Not enough time, move on to next component
                thisComponent.status = STOPPED
        
        
        # reset, record and move on to next stimuli
        if thisComponent.status == STOPPED:
            print('Component name (stopped): ' + thisComponent.name) # debugging
            print('Stop time: ' + str(globalClock.getTime()))
            
            if thisComponent.name == 'movies':
                movie2play.setAutoDraw(False)
            else:
                thisComponent.setAutoDraw(False)
            
            if thisComponent.name == 'ratingbar':
                thisComponent.hideRating() # hide the rating currently given
                thisComponent.responseGiven = False
            
            thisComponent.status = NOT_STARTED
            
            thisExp.addData('duration', experimentClock.getTime())
            thisExp.addData('frameStop', frameN)
            thisExp.addData('end', globalClock.getTime())
            thisExp.nextEntry()
            
            if trialPart < ( len(trialOrder) - 1 ): # Advance to next stimuli
                trialPart = trialPart + 1
            else: # Reached the end, move on to the next trial conditions
                if stimIndx < ( len(stimConditions) - 1 ):
                    stimIndx = stimIndx + 1
                    trialPart = 0
                else: # No more stimuli to display
                    continueRoutine = False
        
        # Refresh the screen if this component has something to draw
        if continueRoutine and thisComponent.status == STARTED:
            win.flip()
            frameN = frameN + 1
    
    return frameN

def runExperiment(win, experimentComponents, globalClock,
        experimentClock, stimConditions, thisExp, MR_settings, 
        MRClock, scantype='Practice', frameN=0):
    
    continueRoutine = True
    stimIndx = 0 # Which stimCondition to use.
    trialPart = 0 # Which part of the trial we're on
    trialOrder = ['asterisks', 'cue', 'fixation', 'movies', 
        'fixation', 'ratingbar'] # This is the order of stimuli for a single trial.
    firstFixation = True # Different behavior needed whether this is 1st or 2nd fixation in trialOrder
    stopOnTrigger = False # Flag to stop on next trigger
    waiting4trigger = False # Flag to wait until a trigger happens
    asterRespGiven = False # Flag to only allow one response to the asterisks
    
    if scantype == 'Practice':
        vol = launchScan(win, MR_settings, globalClock=MRClock, wait_msg='', mode='Test')
    if scantype == 'Scan':
        # This will halt code execution until a trigger is sent
        vol = launchScan(win, MR_settings, globalClock=MRClock, wait_msg='', 
            wait_timeout=300, mode='Scan')
    
    scanDuration = MR_settings['volumes'] * MR_settings['TR']
    
    while continueRoutine:
        thisComponent = experimentComponents[trialOrder[trialPart]]
        
        # start experiment component 
        if thisComponent.status == NOT_STARTED:
            # syncing the start of this component to the next trigger pulse
            while waiting4trigger:
                allKeys = event.getKeys()
                for key in allKeys:
                    if key == MR_settings['sync']:
                        waiting4trigger = False
                        vol += 1
                    elif key == 'escape':
                        win.close()
                        core.quit()
            
            print('Component name (start): ' + thisComponent.name) # debugging
            print('Start time: ' + str(MRClock.getTime()))
            
            # keep track of start time/frame
            thisComponent.status = STARTED
            thisExp.addData('stimType', thisComponent.name )
            thisExp.addData('start', globalClock.getTime())
            thisExp.addData('frameStart', frameN) # exact frame index
            experimentClock.reset() # keep track of how long component is active
            event.clearEvents(eventType='keyboard') # clearing any keypress from previous component
            
            # setting up component specific parameters
            if thisComponent.name == 'asterisks':
                duration = stimConditions[stimIndx]['ITI'] # how long to keep this stim on screen
                thisComponent.text = stimConditions[stimIndx]['Asterisk']
                thisComponent.setAutoDraw(True)
            elif thisComponent.name == 'cue':
                duration = 2 
                thisComponent.text = stimConditions[stimIndx]['Cue']
                thisComponent.setAutoDraw(True)
            elif thisComponent.name == 'fixation':
                if firstFixation:
                    duration = stimConditions[stimIndx]['ISI']
                    firstFixation = False
                else:
                    duration = 3
                    firstFixation = True # resetting
                thisComponent.setAutoDraw(True)
                win.flip()
            elif thisComponent.name == 'movies': # pick which movie to play
                movieName = stimConditions[stimIndx]['VideoFile']
                movie2play = thisComponent.MovieStimDict[movieName]
                duration = movie2play.duration
                thisExp.addData('VidName', movieName )
                movie2play.setAutoDraw(True)
            elif thisComponent.name == 'ratingbar':
                duration = 3
                thisComponent.setAutoDraw(True)
            
        # dealing with key presses for this component.
        if thisComponent.status == STARTED:
            # Check for key press
            thiskeylist = ['escape', MR_settings['sync']]
            if thisComponent.name == 'asterisks':
                ratingsAllowed = ["1", "2", "3", "4", "5"]
                thiskeylist = thiskeylist + ratingsAllowed
            elif thisComponent.name == 'ratingbar':
                ratingsAllowed = ["1", "2", "3", "4", "5"]
                thiskeylist = thiskeylist + ratingsAllowed
            
            keyspressed = event.getKeys(keyList=thiskeylist)
            
            for key in keyspressed:
                if key == MR_settings['sync']:
                    vol += 1
                    if stopOnTrigger: # Checking if this component has been marked to stop on trigger
                        # if the trigger just happened, run the next component as soon
                        # as possible, don't wait for another trigger
                        #
                        # Note that this is to deal with the possibility that there are stimuli with 
                        # durations that are not a multiple of the TR. Hopefully this doesn't happen, 
                        # but if it does, then the timing of the next component will be very close, 
                        # but not exactly time locked with the trigger as the others that waited for 
                        # for the trigger will be. This should only be a difference of a few fractions 
                        # of a millisecond, but obviously not ideal. Avoid this simply by making sure 
                        # your stimuli are multiples of the TR in duration.
                        waiting4trigger = False 
                        stopOnTrigger = False
                        thisComponent.status = STOPPED
                if key == 'escape': # check for quit (the Esc key):
                    win.close()
                    core.quit()
            
            # Filtering out any trigger characters which should already be accounted for.
            keyspressed = list( filter(lambda item: item != MR_settings['sync'] , keyspressed) )
            
            # At least one key was pressed. Do something with it.
            if len(keyspressed) >= 1:
                firstKey = keyspressed[0] # Only taking first response
                print(keyspressed)
                if thisComponent.name == 'asterisks':
                    if not asterRespGiven:
                        # Only record a response if one not already given.
                        asterRespGiven = True
                        thisExp.addData('keypress', firstKey)
                        thisExp.addData('RT', experimentClock.getTime())
                elif thisComponent.name == 'ratingbar':
                    if not thisComponent.responseGiven:
                        # Only record a response if one not already given.
                        thisComponent.displayRating(int(firstKey))
                        thisComponent.responseGiven = True
                        thisExp.addData('keypress', firstKey)
                        thisExp.addData('RT', experimentClock.getTime())
        
        # only run this component for as long as its specified duration.
        if thisComponent.status == STARTED:
            # So we don't try to draw when there isn't enough time left
            time4stim = duration - win.monitorFramePeriod * 0.75
            if experimentClock.getTime() > time4stim: # Not enough time, move on to next component
                thisComponent.status = STOPPED
                waiting4trigger = True # Sync the next component to the next trigger
            
            timeLeft = time4stim - experimentClock.getTime()
            if timeLeft < MR_settings['TR']:
                # Not enough time to finish, start listening for trigger to start next component,
                # but keep running till then.
                stopOnTrigger = True
        
        # If we've run out of time for the experiment, stop this component gracefully.
        if (MRClock.getTime() >= scanDuration):
            thisComponent.status = STOPPED
            continueRoutine = False
        
        # reset, record and move on to next stimuli
        if thisComponent.status == STOPPED:
            print('Component name (stopped): ' + thisComponent.name) # debugging
            print('Stop time: ' + str(MRClock.getTime()))
            
            if thisComponent.name == 'movies':
                movie2play.setAutoDraw(False)
            else:
                thisComponent.setAutoDraw(False)
            
            if thisComponent.name == 'ratingbar':
                if not thisComponent.responseGiven:
                    thisExp.addData('keypress', 'no response')
                thisComponent.hideRating() # hide the rating currently given
                thisComponent.responseGiven = False
            elif thisComponent.name == 'asterisks':
                if not asterRespGiven:
                    thisExp.addData('keypress', 'no response')
                asterRespGiven = False
            
            thisComponent.status = NOT_STARTED
            stopOnTrigger = False
            
            thisExp.addData('duration', experimentClock.getTime())
            thisExp.addData('frameStop', frameN)
            thisExp.addData('end', globalClock.getTime())
            thisExp.nextEntry()
            
            if trialPart < ( len(trialOrder) - 1 ): # Advance to next stimuli
                trialPart = trialPart + 1
            else: # Reached the end, move on to the next trial conditions
                if stimIndx < ( len(stimConditions) - 1 ):
                    stimIndx = stimIndx + 1
                    trialPart = 0
                else: # No more stimuli to display
                    continueRoutine = False
        
        # Refresh the screen if this component has something to draw
        # NTS: Make this a little less CPU intensive by only flipping if 
        # something has changed.
        if continueRoutine and thisComponent.status == STARTED:
            win.flip()
            frameN = frameN + 1
        
    
    return frameN