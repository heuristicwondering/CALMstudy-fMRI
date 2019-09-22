from psychopy import visual, event, monitors, gui, core, data, logging
from psychopy.constants import (NOT_STARTED, STARTED, STOPPED)
import os

class ExperimentSettings:
    def __init__(self, expDir):
        self.experimentDir = expDir

        # these are set with setParameters
        self.expInfo = None
        self.stimConditions = None
        self.expHandler = None

        # this is set with setMRsettings
        self.MR_settings = None

        # these are set with setMonitor
        self.monitor = None
        self.screensize = None

        # this is set with setWindow
        self.win = None

        # this is set with createScanLauncher
        self.launchscan = None

        # this is set with setClocks
        self.globalClock = None
        self.componentClock = None
        self.MRClock = None

        # this is not set with a method
        self.frameN = 0

    def _getStimList(self):
        # Asking user what list of videos to play
        dlg = gui.Dlg(title='Error')
        dlg.addText('Please only select one file!')

        while True:
            stimFile = gui.fileOpenDlg(tryFilePath='./infant-stimuli/stimuli-lists/',
                                       prompt='Select which video list to use', allowed='*.csv')

            if stimFile is None:
                core.quit()  # user pressed cancel

            if len(stimFile) == 1:
                break
            else:
                dlg.show()  # ask user to only pick one file
                if not dlg.OK:
                    core.quit()  # user pressed cancel

        # Loading the list of stimuli to present
        self.stimConditions = data.importConditions(stimFile[0])

        self.vidpath = (self.experimentDir + os.sep + 'infant-stimuli' + os.sep + 'videos')  # Assuming all movies are here
        assert os.path.isdir(self.vidpath), self.vidpath + ' which should contain stimuli does not exist'

    def setParameters(self):
        # Store info about the experiment session
        expName = 'CALMstudy'
        dlg = gui.Dlg(title=expName)
        dlg.addField('participant', 'Jayne Doe')
        dlg.addField('Scan Type', choices=['Task', 'Rest', 'Rest-Alternate'])
        dlg.addField('Session', choices=['Pre-Intervention', 'Post-Intervention'])
        dlg.addText(('Note: The Rest-Alternate scan is a resting state scan \n'
                     'using a different set of instructions.'), color='green')
        expValues = dlg.show()

        if not dlg.OK:
            core.quit()  # user pressed cancel

        # Creating a dictionary of information about experiment
        expKeys = ['participant', 'scantype', 'session']
        self.expInfo = dict(zip(expKeys, expValues))
        self.expInfo['date'] = data.getDateStr()  # add a simple timestamp
        self.expInfo['expName'] = expName

        # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
        if self.expInfo['scantype'] == 'Task':
            dataFolder = self.experimentDir + os.sep + 'data-infant'
        elif self.expInfo['scantype'] == 'Rest':
            dataFolder = self.experimentDir + os.sep + 'data-rest'
        elif self.expInfo['scantype'] == 'Rest-Alternate':
            dataFolder = self.experimentDir + os.sep + 'data-rest-alternate'
        if not os.path.exists(dataFolder):
            os.makedirs(dataFolder)

        filename = (dataFolder + os.sep
                    + '%s_%s_%s_%s_%s' % (
                    self.expInfo['participant'],
                    self.expInfo['scantype'], self.expInfo['session'],
                    self.expInfo['expName'], self.expInfo['date']))

        # get video play list
        if self.expInfo['scantype'] == 'Task':
            self._getStimList()

        # An ExperimentHandler isn't essential but helps with data saving
        self.expHandler = data.ExperimentHandler(name=expName, version='',
                                                     extraInfo=self.expInfo, runtimeInfo=None,
                                                     originPath=None,
                                                     savePickle=True, saveWideText=True,
                                                     dataFileName=filename)

        logging.LogFile(filename + '.log', level=logging.EXP)  # save a log file for detail verbose info
        logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    def _displayMRSetting(self):
        # Tell experimenter what the scan settings are.
        dlg = gui.Dlg(title=self.expInfo['expName'])
        dlg.addText('These are the current scan parameters.\n'
                    'This is for informational purposes only.\n'
                    'If these settings are correct, just click \'OK\'\n')
        dlg.addText('Run length (in seconds) = ' + str(self.MR_settings['runlength']))
        dlg.addText('TR = ' + str(self.MR_settings['TR']))
        dlg.addText('Volumes = ' + str(self.MR_settings['volumes']))

        if self.expInfo['scantype'] == 'Task':
            dlg.addText('Planned stimuli duration = ' + str(self.expInfo['movieDuration']) + ' seconds')

        dlg.show()

        if not dlg.OK:
            core.quit()  # user pressed cancel

    def setMRsettings(self):
        # Setting the scan parameter and adding additional experiment info
        # depending on scan type specified by user.
        if self.expInfo['scantype'] == 'Task':
            self.MR_settings = {
                'runlength': 480,  # duration (sec) of this scan
                'TR': 1.000,  # duration (sec) per whole-brain volume
                'volumes': 480,  # number of whole-brain 3D volumes per scanning run
                'sync': 'equal',  # character to use as the sync timing event; assumed to come at start of a volume
                'skip': 0,  # number of volumes lacking a sync pulse at start of scan (for T1 stabilization)
                'sound': True  # in test mode: play a tone as a reminder of scanner noise
            }

            # note that movies will play to the nearest second that is both a multiple of the TR
            # and less than or equal to this duration
            self.expInfo.update({'movieDuration': 12})

        elif (self.expInfo['scantype'] == 'Rest'
              or self.expInfo['scantype'] == 'Rest-Alternate'):
            self.MR_settings = {
                'runlength': 360,  # duration (sec) of this scan
                'TR': 1.000,  # duration (sec) per whole-brain volume
                'volumes': 360,  # number of whole-brain 3D volumes per scanning run
                'sync': 'equal',  # character to use as the sync timing event; assumed to come at start of a volume
                'skip': 0,  # number of volumes to ignore at start of scan (for T1 stabilization)
                'sound': True  # in test mode: play a tone as a reminder of scanner noise
            }

        self._displayMRSetting()

    def setMonitor(self):
        # subjectMonitor NEEDS TO BE ADJUSTED FOR MONITOR USING!
        # this is done in the Monitor Center of the psychopy IDE
        self.monitor = monitors.Monitor('subjectMonitor')
        self.screensize = (1280, 1024)  # screen resolution

    def setWindow(self):
        # Using secondary monitor NEEDS TO BE ADJUSTED FOR MONITOR USING!
        self.win = visual.Window(self.screensize, fullscr=True, screen=1,
                                allowGUI=False, allowStencil=False,
                                monitor=self.monitor,
                                color=[0, 0, 0], colorSpace='rgb',
                                blendMode='avg', useFBO=True)

        # store frame rate of monitor if we can measure it
        self.expInfo['frameRate'] = self.win.getActualFrameRate()
        if self.expInfo['frameRate'] is not None:
            frameDur = 1.0 / round(self.expInfo['frameRate'])
        else:
            frameDur = 1.0 / 60.0  # could not measure, so guess

        # Tell experimenter what the monitor settings are.
        dlg = gui.Dlg(title=self.expInfo['expName'])
        dlg.addText('These are the current monitor settings.\n'
                    'This is for informational purposes only.\n'
                    'If these settings are correct, just click \'OK\'\n')
        dlg.addText('Screen Resolution = ' + str(self.screensize))
        dlg.addText('Screen Number (0 is primary) = ' + str(self.win.screen))
        dlg.addText('Estimated Monitor Frame Rate = ' + str(round(frameDur, 8)))
        dlg.show()

        if not dlg.OK:
            core.quit()  # user pressed cancel

    def createWaitScreen(self):
        # Note that launchscan is currently not working due to a bug in
        # how sound is handled (https://github.com/psychopy/psychopy/issues/2007)
        # using the following as part of a work around until next release
        self.waitScreen = visual.TextStim(win=self.win, name='Wait4TriggerScreen',
                                             text='Waiting for Scan Start',
                                             font='Arial',
                                             pos=(0, 0), height=0.05, wrapWidth=None, ori=0,
                                             color='white', colorSpace='rgb', opacity=1,
                                             depth=0.0)

        self.waitScreen.status = NOT_STARTED

    def setClocks(self):
        self.globalClock = core.Clock()  # Keep track of beginning of time
        self.MRClock = core.CountdownTimer()  # Keep help sync stimuli to trigger
        self.componentClock = core.Clock()  # Keep track of start of stimuli

