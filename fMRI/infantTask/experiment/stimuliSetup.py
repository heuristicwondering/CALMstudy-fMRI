import psychopy, math
psychopy.useVersion('latest')

from psychopy import visual, tools

# NTS: get rid of constants not using when code is finished
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, 
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

from sys import getsizeof # debugging. needed to check size of movies object
from collections import Mapping, Container # debugging.

def defineStim(window2use, stimConditions, extraStimCond=[], path2movies=''):
    # All returned objects must have a status attribute
    Instr1 = visual.TextStim(win=window2use, name='Instr1',
        text='In this task you will ...',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);

    Instr2 = visual.TextStim(win=window2use, name='Instr2',
        text='When you ...',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);

    Instr3 = visual.TextStim(win=window2use, name='Instr3',
        text='After you ...',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);

    Instr4 = visual.TextStim(win=window2use, name='Instr4',
        text='When you ... \n\n' \
        '(*** = 3)',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);

    Instr5 = visual.TextStim(win=window2use, name='Instr5',
        text='Now we will practice responses \n' \
        'on the rating sca... \n\n' \
        'Are you ready?',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);

    Instr6 = visual.TextStim(win=window2use, name='Instr6',
        text='Now you will ...\n\n' \
        'Don\'t forget to count the stars!',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);
    
    Instr7 = visual.TextStim(win=window2use, name='Instr7',
        text='Do you have any questions?',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);
    
    Instr8 = visual.TextStim(win=window2use, name='Instr8',
        text='Now, try ...',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);
    
    Instr9 = visual.TextStim(win=window2use, name='Instr9',
        text='Waiting for trigger...',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);
    
    Instr10 = visual.TextStim(win=window2use, name='Instr10',
        text='Remember your job is to ...\n',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);
    
    Instr11 = visual.TextStim(win=window2use, name='Instr11',
        text='Remember, ..',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);
    
    Instr12 = visual.TextStim(win=window2use, name='Instr12',
        text='Remember, your job is ...',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);
        
    Instr13 = visual.TextStim(win=window2use, name='Instr13',
        text='Remember, ...',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);
    
    thankyou1 = visual.TextStim(win=window2use, name='thankyou1',
        text='Good job!\n' \
            'You are done with the practice',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);
    
    thankyou2 = visual.TextStim(win=window2use, name='thankyou2',
        text='...',
        font='Arial',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);
    
    asterisks = visual.TextStim(win=window2use, name='asterisks',
        text='*****',
        font='Arial',
        pos=(0, 0), height=0.3, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);
    
    cue = visual.TextStim(win=window2use, name='cue',
        text='...',
        font='Arial',
        pos=(0, 0), height=0.2, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0);
    
    fixation = visual.TextStim(win=window2use, name='fixation',
        text='+',
        font='Arial',
        pos=(0, 0), height=0.4, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', 
        opacity=1, depth=0.0);
    
    ratingbar = RatingScale(window2use, name='ratingbar')
    
    # Returns a class containing a dictionary of movieStim objects 
    # with filenames used as keys.
    allConditions = stimConditions + extraStimCond
    movies = MovieStimuli(window2use, allConditions, path2movies, name='movies')
    
    stimuli = {'Instr1':Instr1, 'Instr2':Instr2, 'Instr3':Instr3, \
        'Instr4':Instr4, 'Instr5':Instr5, 'Instr6':Instr6, 'Instr7':Instr7, \
        'Instr8':Instr8, 'Instr9':Instr9, 'Instr10':Instr10, 'Instr11':Instr11, \
        'Instr12':Instr12, 'Instr13':Instr13, 'thankyou1':thankyou1, 'thankyou2':thankyou2, \
        'asterisks':asterisks, 'fixation':fixation, 'cue':cue, 'ratingbar':ratingbar, \
        'movies':movies}
    return stimuli

# debugging. checking size of the movies object
# not currently used, but retained to aide later development
def deep_getsizeof(o, ids):
    """Find the memory footprint of a Python object
    This is a recursive function that rills down a Python object graph
    like a dictionary holding nested dictionaries with lists of lists
    and tuples and sets.
    The sys.getsizeof function does a shallow size of only. It counts each
    object inside a container as pointer only regardless of how big it
    really is.
    :param o: the object
    :param ids:
    :return:
    """
    # Copied from https://github.com/the-gigi/deep/blob/master/deeper.py#L80
    # modified for Python 3
    d = deep_getsizeof
    if id(o) in ids:
        return 0

    r = getsizeof(o)
    ids.add(id(o))

    if isinstance(o, str):
        return r

    if isinstance(o, Mapping):
        return r + sum(d(k, ids) + d(v, ids) for k, v in o.items())

    if isinstance(o, Container):
        return r + sum(d(x, ids) for x in o)

    return r    

class MovieStimuli:
    def __init__(self, window2use, stimConditions, path2movies, name=''):
        self.status = NOT_STARTED
        self.name = name
        self.MovieStimDict = self.createMovieStim(window2use, stimConditions, path2movies)
        
    def createMovieStim(self, window2use, stimConditions, path2movies):
        # NTS: Future versions should check for duplicate movie entries and create 
        # a new class for this as well. This will prevent loading slow downs for 
        # large movies (as opposed to replaying which under the psychopy hood calls a 
        # load command) during experiment run. Experiment execution code will need to 
        # be modified to accommodate this.
        movies = {}
        for thisCondition in stimConditions:
            movieFileName = thisCondition['VideoFile']
            movieFullPath = path2movies + movieFileName
            if movieFileName not in movies:
                thisMovie = visual.MovieStim3(win=window2use, name=movieFileName, 
                    noAudio = False, filename = movieFullPath, units='pix', 
                    color=[-0.569,-0.514,-0.373], colorSpace='rgb', 
                    ori=0, pos=(0, 0), opacity=1)
                
                # This is to make full screen while maintaining aspect ratio.
                # NTS: Think of a more elegant way to do this.
                #
                # Scale to fit stim along smaller side of window.
                smallerWinSide = min(window2use.size) 
                scale = max([smallerWinSide/s for s in thisMovie.size])
                newSize = thisMovie.size * scale
                # Catches when this made the stim too big.
                # i.e. the stim is off screen along the longer side
                # Instead scale to the other side of the window.
                if any(s > w for s,w in zip(newSize, window2use.size)):
                    biggerWinSide = max(window2use.size)
                    scale = min([biggerWinSide/s for s in thisMovie.size])
                    newSize = thisMovie.size * scale
                    
                thisMovie.size = newSize
                
                thisMovie = {movieFileName : thisMovie}
                movies.update(thisMovie)
                
                # debugging. printing current size of movies object.
                # NTS: remove this only after I implement on-the-fly movie loading
                # print( 'Current size of movies object: ' 
                    # + str( deep_getsizeof(movies, ids=set()) )
                    # + ' bytes.')
        
        return movies

class RatingScale:
# Note that not all functions have been thoroughly tested <-- No guarantees!
    def __init__(self, window2use, name='', totTickNum=5):
        self.status = NOT_STARTED
        self.drawToggle = False
        self.name = name
        self.responseGiven = False
        self.currentResponse = ''
        self.showingResponse = False
        self.RT = None
        
        self._winWidth = window2use.size[0]
        self._winHeight = window2use.size[1]
        
        self._centerLine = visual.Rect(win=window2use, units='norm', 
            width=1, height=0.025, fillColor='white', pos=(0,-0.25))
        self.totTickNum = totTickNum
        
        self._CLvert = tools.monitorunittools.convertToPix(self._centerLine.vertices,
            self._centerLine.pos, 'norm', window2use)
        
        self._ticklines = []
        self._ticknums = []
        # setting tick and their labels
        for t in range(self.totTickNum):
            tick = t + 1
            tickParam = self.setTick(tick)
            thisTick = visual.Rect(win=window2use, units='pix', 
                width=tickParam['width'], height=tickParam['height'], 
                fillColor='white', pos=tickParam['pos'])
            self._ticklines = self._ticklines + [thisTick]
            
            tickLabelParam = self.setTickLabel(tickParam)
            thisTickNum = visual.TextStim(win=window2use, units='pix',
                text=str(tick), font='Arial', pos=tickLabelParam['pos'], 
                height=tickLabelParam['height'], wrapWidth=None, 
                color='white', colorSpace='rgb', opacity=1, depth=0.0)
            self._ticknums = self._ticknums + [thisTickNum]
        
        anchorParam = self.setAnchor(tickParam, 'left')
        self._anchorL = visual.TextStim(win=window2use, units='pix',
            text='Very\ngood', font='Arial', alignHoriz='right', 
            pos=anchorParam['pos'], height=anchorParam['height'], 
            wrapWidth=None, color='white', colorSpace='rgb', opacity=1, depth=0.0)
        
        anchorParam = self.setAnchor(tickParam, 'right')
        self._anchorR = visual.TextStim(win=window2use, units='pix',
            text='Very\nbad', font='Arial', alignHoriz='left', 
            pos=anchorParam['pos'], height=anchorParam['height'], 
            wrapWidth=None, color='white', colorSpace='rgb', opacity=1, depth=0.0)
        
        self._instr = visual.TextStim(win=window2use, units='norm',
            text='How do you feel?', font='Arial', pos=(0, 0.4), 
            alignHoriz='center', height=0.125, 
            wrapWidth=2, color='white', colorSpace='rgb', opacity=1, depth=0.0)
        
        self._bar = ([self._centerLine] + self._ticklines + self._ticknums 
                        + [self._anchorL, self._anchorR, self._instr])
        
        circParam = self.setCircle(tickParam)
        self._circle = visual.Circle(window2use, units='pix', radius=circParam['radius'], 
            pos=circParam['pos'], lineWidth=3, lineColor=[1, 0, .5], lineColorSpace='rgb', 
            fillColor=[1, 0, 0], fillColorSpace='rgb')
    
    def setTick(self, tickNum):
        # Uses pixel vertices of the center line to set the width, height, 
        # and position of tick marks so that they stay lined up with the 
        # center bar and maintain aspect ratio even if it's moved.
        luCornerW = self._CLvert[0][0] # left lower corner width position
        ruCornerW = self._CLvert[1][0]
        ruCornerH = self._CLvert[1][1]
        rlCornerW = self._CLvert[2][0]
        rlCornerH = self._CLvert[2][1]
        CLwidth = abs(ruCornerW - luCornerW)
        CLheight = abs(ruCornerH - rlCornerH)
        
        width = CLheight
        height = math.floor( (CLwidth / self.totTickNum) / 2 ) # Kinda arbitrary
        
        CLtickWidth = CLwidth - width # width in which to place tick centers
        tickDist = CLtickWidth / (self.totTickNum - 1) # dist between tick centers
        
        if tickNum == 1: # width pos of far left tick
            tickCentWidth = luCornerW + math.floor(width/2)
        elif tickNum == self.totTickNum: # width pos of far right tick
            # Rounding errors in calculating width pos as an offset may cause 
            # last tick to not line up with the end of the center line. Setting 
            # manually to avoid this.
            tickCentWidth = rlCornerW - math.ceil(width/2)
        else: # all other ticks set as offset from width pos of far left tick
            tickCentWidth = luCornerW + math.floor( width/2 + tickDist*(tickNum-1) )
        
        tickCentHght = rlCornerH + math.floor( CLheight / 2 ) # If CLheight odd, will be down by 1px
        
        pos = (tickCentWidth, tickCentHght)
        
        param = {'width':width, 'height':height, 'pos':pos}
        return param
    
    def setTickLabel(self, tickParam):
        # Setting tick labels relative to the ticks themselves
        height = math.floor(tickParam['height']*0.75) # Keeping proportional to tick length
        tickLblCentWidth = tickParam['pos'][0] # center along width in line with tick
        tickLblCentHght = tickParam['pos'][1] - math.ceil( tickParam['height']/2 
            + height ) # Need text height center moved down from tick center
        pos = (tickLblCentWidth, tickLblCentHght)
        
        param = {'height':height, 'pos':pos}
        return param
    
    def setAnchor(self, tickParam, toside):
        height = math.floor( tickParam['height']/2 )
        
        luCornerW = self._CLvert[0][0] # left upper corner width
        luCornerH = self._CLvert[0][1] # left upper corner height
        ruCornerW = self._CLvert[1][0] # right upper corner width
        llCornerH = self._CLvert[3][1] # left lower corner height
        CLheight = abs(luCornerH - llCornerH)
        
        sideShift = {'left':-1,'right':1}
        CLside = {'left':luCornerW, 'right':ruCornerW}
        
        anchrCentWidth = ( CLside[toside] + sideShift[toside]*height)
        anchrCentHght = llCornerH + math.ceil(CLheight/2)
        
        pos = (anchrCentWidth, anchrCentHght)
        
        param = {'height':height, 'pos':pos}
        return param
    
    def setCircle(self, tickParam):
        radius = math.floor( tickParam['height']/4 )
        pos = [ 0, tickParam['pos'][1] ]
        param = {'radius':radius, 'pos':pos}
        return param
    
    def setAutoDraw(self, drawToggle):
        for component in self._bar:
            component.setAutoDraw(drawToggle)
        
        if self.showingResponse == True:
            self._circle.setAutoDraw(drawToggle)
        # just in case circle was drawn then show response was 
        # turned off before autoDraw set false
        else:
            self._circle.setAutoDraw(False)
        
        self.drawToggle = drawToggle
        
    def draw(self):
        for component in self._bar:
            component.draw()
        
        if self.showingResponse == True:
            self._circle.draw()
        
    def displayRating(self, rating):
        # code to allow rating circle to draw
        self.showingResponse = True
        self.currentResponse = rating
        crclTick = self.setTick(rating) # Tick parameters to determine where to draw
        self._circle.pos = crclTick['pos']
        
        # If autoDraw is turned on, reset it so the response will also autoDraw
        # if not, will need to call draw() to display
        if self.drawToggle:
            self.setAutoDraw(self.drawToggle)
        
        print('Show rating: ' + str(self.currentResponse))
    
    def hideRating(self):
        # code to hide rating circle goes here
        self.showingResponse = False
        
        if self.drawToggle:
            self.setAutoDraw(self.drawToggle)
            
        print('Hide rating: ' + str(self.currentResponse))
        
