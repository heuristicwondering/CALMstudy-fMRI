from psychopy import visual, gui, logging, core
from psychopy.constants import NOT_STARTED


def defineInstructions(window2use):
    instr1 = visual.TextStim(win=window2use, name='TaskInstr1',  # Primary Task instructions
                                 text='We will start the first scan now.',
                                 font='Arial',
                                 pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                                 color='white', colorSpace='rgb', opacity=1,
                                 depth=0.0)

    instr2 = visual.TextStim(win=window2use, name='TaskInstr2',
                                 text='You will see a white cross appear on the screen.',
                                 font='Arial',
                                 pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                                 color='white', colorSpace='rgb', opacity=1,
                                 depth=0.0)

    instr3 = visual.TextStim(win=window2use, name='TaskInstr3',
                                 text='Please remain alert and awake while you look and this cross.',
                                 font='Arial',
                                 pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                                 color='white', colorSpace='rgb', opacity=1,
                                 depth=0.0)

    instr4 = visual.TextStim(win=window2use, name='TaskInstr4',
                                    text='Do you have any questions?',
                                    font='Arial',
                                    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                                    color='white', colorSpace='rgb', opacity=1,
                                    depth=0.0)

    # Setting status attribute
    instructions = [instr1, instr2, instr3, instr4]
    for thisInstr in instructions:
        thisInstr.status = NOT_STARTED

    return instructions


def defineAlternateInstructions(window2use):
    instr1 = visual.TextStim(win=window2use, name='TaskInstr1',  # Primary Task instructions
                             text='We will now continue on to the next part of the scan.',
                             font='Arial',
                             pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                             color='white', colorSpace='rgb', opacity=1,
                             depth=0.0)

    instr2 = visual.TextStim(win=window2use, name='TaskInstr2',
                             text='This will be a different set of instructions.',
                             font='Arial',
                             pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                             color='white', colorSpace='rgb', opacity=1,
                             depth=0.0)

    instr3 = visual.TextStim(win=window2use, name='TaskInstr3',
                             text='Please follow this other instruction.',
                             font='Arial',
                             pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                             color='white', colorSpace='rgb', opacity=1,
                             depth=0.0)

    instr4 = visual.TextStim(win=window2use, name='TaskInstr4',
                             text='Do you have any questions?',
                             font='Arial',
                             pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                             color='white', colorSpace='rgb', opacity=1,
                             depth=0.0)

    # Setting status attribute
    instructions = [instr1, instr2, instr3, instr4]
    for thisInstr in instructions:
        thisInstr.status = NOT_STARTED

    return instructions


def defineThankyou(window2use):
    thankyou1 = visual.TextStim(win=window2use, name='TaskThanks',
                                 text='You\'re all done! \n\n'
                                      'You can close your eyes and relax, '
                                      'but please try to not fall asleep.',
                                 font='Arial',
                                 pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                                 color='white', colorSpace='rgb', opacity=1,
                                 depth=0.0)

    thankyou1.status = NOT_STARTED

    return [thankyou1]


def defineStim(window2use):
    fixation = visual.TextStim(win=window2use, name='fixation',
                                text='+',
                                font='Arial',
                                pos=(0, 0), height=0.4, wrapWidth=None, ori=0,
                                color='white', colorSpace='rgb', opacity=1,
                                depth=0.0)

    fixation.status = NOT_STARTED

    return {'fixation': fixation}
