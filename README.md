# CALMstudy-fMRI
This repository contains the following:

- fMRI infant viewing task using Psychopy
- Code for creating randomized blocks of stimuli as csv files
- fMRI resting state fixation cross using Psychopy

-----------------------------------------------------------
Setting Up this Experiment:
-----------------------------------------------------------

You will need to provide videos and a csv file that specifies 
in what order to present each video.

**Store Videos Here**

	./fMRI-experiment/infant-stimuli/videos/SubjectID
Replacing _SubjectID_ with the ID you intend to use for your participant. 
For videos, it's very important that they be stored here or the code won't be able to find them.
	
**Store stimuli list here**

	./fMRI-experiment/infant-stimuli/stimuli-lists/

This is just a convenient place, but location is not as crucial as it is for videos. 

Stimuli list should consist of two columns with the headers 
_VideoFile,TrialType_

**VideoFile**
	Should be the file name (without path) and extension 
	(_e.g._ control.mp4)

**TrialType**
	This is the name of the type of condition this video represents
	(_e.g._ Control)

Videos will be displayed sequentially for max 12s each. Longer videos 
will be truncated.

-----------------------------------------------------------
Running this Experiment:
-----------------------------------------------------------

To run this task, open CALM.py in the standalone Psychopy 
IDE and hit run. You will be asked for information about your 
 experiment. Be sure that the _participant_  field is the same 
 as the video folder name (case sensitive). You will also be 
 asked to specify a stimuli list (if running a task) for this run 
 which will determine what videos and in what order they are played. 

You will also see informational windows on the assumed settings 
for this experiement. These were set for the purpose of our experiment 
and you will need to change them in the code to match your parameters.

The decision to provide this as non-editable information was intentional 
because this would only need to be changed once when setting up the 
experiment and should not be messed with after that.

-----------------------------------------------------------
Notes:
-----------------------------------------------------------

This code was developed with Psychopy 3.0.3 using Python 3.5.5 

The infant-viewing task relies on scrambled audio and video for 
a control task. The code to do this is available at 
https://github.com/heuristicwondering/movie-scrambler

An attempt has been made to document areas in need of further 
development for future versions. Please read the comments for 
this information. If you make any improvements or bug fixes to 
this paradigm, submitting a pull request to this repository would 
be greatly appreciated.

If this code or any derivation thereof is used in publication, 
please include appropriate acknowledgments. The authors would 
also be grateful if you could contact them with a citation for 
that publication.

Happy scanning!

-----------------------------------------------------------
Acknowledgments:
-----------------------------------------------------------
Paradigm originally conceived by:
    
    Laurent, H. K., Wright, D., & Finnegan, M. (2018). Mindfulness-related differences 
    in neural response to own infant negative versus positive emotion contexts. Developmental 
    Cognitive Neuroscience, 30, 70-76.