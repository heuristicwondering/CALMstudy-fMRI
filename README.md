# CALMstudy-fMRI
fMRI infant viewing task using Psychopy
fMRI resting state fixation cross using Psychopy

-----------------------------------------------------------
Setting Up this Experiment:
-----------------------------------------------------------

You will need to provide videos and a csv file that specifies 
in what order to present each video.

**Store Videos Here**
	./fMRI-experiment/infant-stimuli/videos/
**Store stimuli list here**
	./fMRI-experiment/infant-stimuli/stimuli-lists/

Stimuli list should consist of two columns with the headers 
_VideoFile,TrialType_

**VideoFile**
	Should be the file name (without path) and extension 
	(_e.g._ control.mp4)
**TrialType**
	This is the name of the type of condition this video represents
	(_e.g._ Control)

Videos will be displayed sequentially for max 15s each. Longer videos 
will be truncated.

-----------------------------------------------------------
Running this Experiment:
-----------------------------------------------------------

To run this task, open CALM.py in the standalone psychopy 
IDE and hit run. You will be asked to specific a stimuli list for this run.

You will also see informational windows on the assumed settings 
for this experiement. These were set for the purpose of our experiment 
and you will need to change them in the code to match your parameters.

The decision to provide this as non-editable information was intentional 
because this would only need to be changed once when setting up the 
experiment and should not be messed with after that.

-----------------------------------------------------------
Notes:
-----------------------------------------------------------

This code was developed with Psychopy 3.0.3 
using Python 3.6.3

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