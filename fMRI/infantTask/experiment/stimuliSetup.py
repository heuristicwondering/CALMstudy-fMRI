import psychopy
psychopy.useVersion('latest')

from psychopy import visual, tools
from psychopy.constants import NOT_STARTED

def defineStim(window2use, stimTimings, path2movies=''):

    Instr1 = visual.TextStim(win=window2use, name='Instr1', #Resting State instructions
        text='For this part of the scan we ask that you keep your eyes open (blinking is fine). \n',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);

    Instr2 = visual.TextStim(win=window2use, name='Instr2',
        text='You can relax and let your mind wander, but please stay awake. The screen will be blank during this time.',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);

    Instr3 = visual.TextStim(win=window2use, name='Instr3',
        text=' This part of the scan will last 10 minutes. '
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);

    Instr4 = visual.TextStim(win=window2use, name='Instr4', #Primary Task instructions
        text='We will now continue on to the next part of the scan.',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);
    
    Instr5 = visual.TextStim(win=window2use, name='Instr5',
        text='You will see 15 second clips of movies appear on the screen.',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);
    
    Instr6 = visual.TextStim(win=window2use, name='Instr6',
        text='Please remain alert and awake while these clips are playing.',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);

    Instr7 = visual.TextStim(win=window2use, name='Instr7', #This comes at the end of the RS and the main task instructions
        text='Do you have any questions?',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);

    thanks1 = visual.TextStim(win=window2use, name='thanks1', #Resting State Last Slide
        text='Good job!\n' \
            'You are done with the resting state.',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);

    thanks2 = visual.TextStim(win=window2use, name='thanks2',
        text='You are done with the task! \n'
             'You can close your eyes and relax for the rest of the scan, but please try to not fall asleep.',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);

    fixation = visual.TextStim(win=window2use, name='fixation',
        text='+',
        font='Arial',
        pos=(0, 0), height=0.4, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', 
        opacity=1, depth=0.0);

    # Returns a class containing a dictionary of movieStim3 objects with filenames used as keys.
    movies = MovieStimuli(window2use, stimConditions, path2movies, name='movies')
    
    stimuli = {'Instr1':Instr1, 'Instr2':Instr2, 'Instr3':Instr3,
        'Instr4':Instr4, 'Instr5':Instr5, 'Instr6':Instr6, 'Instr7':Instr7,
        'thanks1':thanks1, 'thanks2':thanks2, 'fixation':fixation, 'movies':movies}
    return stimuli


def getMovieNames(stimTimings):             # stimTimings will be a list of strings
    temp = set()
    uniqueStims = []
    for item in stimTimings:
        if item not in temp:
            temp.add(item)
            uniqueStims.append(item)
    return uniqueStims                      #return a list of all unique stimuli names

class MovieStimuli:
    def __init__(self, window2use, stimConditions, path2movies, name=''):
        self.status = NOT_STARTED
        self.name = name
        self.MovieStimDict = self.createMovieStim(window2use, stimConditions, path2movies)
        
    def createMovieStim(self, window2use, stimConditions, path2movies):
        movies = {}
        for thisCondition in stimConditions:
            movieFileName = thisCondition['VideoFile']
            movieFullPath = path2movies + movieFileName
            if movieFileName not in movies:
                thisMovie = visual.MovieStim3(win=window2use, name=movieFileName, 
                    noAudio = False, filename = movieFullPath, units='pix', 
                    color=[-0.569,-0.514,-0.373], colorSpace='rgb', 
                    ori=0, pos=(0, 0), opacity=1)
                # This is to ensure full screen while maintaining aspect ratio.
                #
                # Scale to fit stim along smaller side of window.
                smallerWinSide = min(window2use.size) 
                scale = max([smallerWinSide/s for s in thisMovie.size])
                newSize = thisMovie.size * scale
                # Catches when this made the stim too big: i.e. the stim is off screen along the longer side
                # Instead scales to the other side of the window.
                if any(s > w for s,w in zip(newSize, window2use.size)):
                    biggerWinSide = max(window2use.size)
                    scale = min([biggerWinSide/s for s in thisMovie.size])
                    newSize = thisMovie.size * scale
                thisMovie.size = newSize
                thisMovie = {movieFileName : thisMovie}
                movies.update(thisMovie)
        return movies