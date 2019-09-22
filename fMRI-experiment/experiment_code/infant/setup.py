from psychopy import visual, gui, logging, core
from psychopy.constants import NOT_STARTED
import os

def defineInstructions(window2use):
    instr1 = visual.TextStim(win=window2use, name='TaskInstr1',  # Primary Task instructions
                                 text='You will see short videos with your baby, other babies, or non-baby images. ',
                                 font='Arial',
                                 pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                                 color='white', colorSpace='rgb', opacity=1,
                                 depth=0.0)

    instr2 = visual.TextStim(win=window2use, name='TaskInstr2',
                                 text='Just watch the videos and respond as you normally would.\n\n'
                                      'Although please try your best to keep your head still.',
                                 font='Arial',
                                 pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                                 color='white', colorSpace='rgb', opacity=1,
                                 depth=0.0)

    instr3 = visual.TextStim(win=window2use, name='TaskInstr3',
                                 text='Do you have any questions?',
                                 font='Arial',
                                 pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                                 color='white', colorSpace='rgb', opacity=1,
                                 depth=0.0)

    # Setting status attribute
    instructions = [instr1, instr2, instr3]
    for thisInstr in instructions:
        thisInstr.status = NOT_STARTED

    return instructions


def defineThankyou(window2use):
    thankyou1 = visual.TextStim(win=window2use, name='TaskThanks',
                                 text='You are done with the task! \n'
                                      'You can close your eyes and relax, '
                                      'but please try to not fall asleep.',
                                 font='Arial',
                                 pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                                 color='white', colorSpace='rgb', opacity=1,
                                 depth=0.0)

    thankyou1.status = NOT_STARTED

    return [thankyou1]


def defineStim(window2use, stimConditions, path2movies):
    # Returns a dictionary of objects containing movieStim3 objects with filenames used as keys.
    vidFileNames = [s['VideoFile'] for s in stimConditions]
    vidFileNames = list(set(vidFileNames))  # unique file names

    movies = {}
    for vid in vidFileNames:
        vidFullFile = path2movies + os.sep + vid

        thisMovie = _createMovieStim(window2use, vidFullFile)
        thisMovie = _resizeMovie(window2use, thisMovie)

        thisMovie.status = NOT_STARTED

        movies[vid] = thisMovie

    return movies


def _createMovieStim(window2use, vidFullFile):
    movieFileName = os.path.basename(vidFullFile)
    movie = visual.MovieStim3(win=window2use, name=movieFileName,
                            noAudio = False, filename = vidFullFile, units='pix',
                            color='black', colorSpace='rgb',
                            ori=0, pos=(0, 0), opacity=1)

    return movie


def _resizeMovie(window2use, movie):
    # Scale to ensure movie is entirely visible on
    # screen while maintaining aspect ratio.
    widthDiff = window2use.size[0] - movie.size[0]
    heightDiff = window2use.size[1] - movie.size[1]
    aspectRatio = movie.size[0] / movie.size[1]

    if widthDiff < heightDiff:  # resize width
        movie.size[0] += widthDiff
        movie.size[1] += (1 / aspectRatio) * widthDiff
    elif heightDiff < widthDiff:  # resize height
        movie.size[0] += aspectRatio * heightDiff
        movie.size[1] += heightDiff

    return movie


def checkBounds(thisExperiment, stimuli):
    # Verify that planned stimuli match expected run time
    TR = thisExperiment.MR_settings['TR']
    RUNLENGTH = thisExperiment.MR_settings['runlength']
    VIDLENGTH = thisExperiment.expInfo['movieDuration']

    estScanDuration = 0
    warnTruncation = False

    for trial in thisExperiment.stimConditions:
        thisVid = stimuli[trial['VideoFile']]
        movdur = thisVid.duration

        if movdur != VIDLENGTH or (movdur % TR) != 0:
            warnTruncation = True

        estScanDuration += VIDLENGTH

    if estScanDuration != RUNLENGTH:
        dlg = gui.Dlg(title='DURATION WARNING')
        dlg.addText('WARNING!\n', color='red')
        dlg.addText('The estimated scan length is ' +
                    str(estScanDuration) + ' seconds but the predefined ' +
                    'scan length has been set to ' + str(RUNLENGTH) +
                    ' seconds.\n\nAre you sure you want to continue?\n\n' +
                    'Experiment will run until there are no more trials ' +
                    'to show or the predefined scan time is reached, \n' +
                    'whichever comes first. You may end up losing stimuli ' +
                    'presentations or wasting scan time.\n\n' +
                    'Press OK to continue.')
        dlg.show()

        if not dlg.OK:
            core.quit()  # user pressed cancel

        logging.warning('Estimated time for stimuli is ' + str(estScanDuration) +
                        ', but predefined time was set to ' + str(RUNLENGTH))

    if warnTruncation:
        dlg = gui.Dlg(title='TRUNCATION WARNING')
        dlg.addText('WARNING!\n', color='red')
        dlg.addText('It was detect that some of your videos may be '
                    'automatically truncated during scanning.\n\n'
                    'This experiement is designed to align stimuli onset '
                    'to the start of volume acquisition. \nIf the planned '
                    'run time or actual movie durations are not multiples '
                    'of the TR then truncation may result.')
        dlg.show()

        if not dlg.OK:
            core.quit()  # user pressed cancel

        logging.warning('Stimuli TRUNCATION')
