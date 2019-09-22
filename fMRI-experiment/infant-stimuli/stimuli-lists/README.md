The pilot included in this folder illustrates how video lists should be specified. There are a few things to keep in mind though when constructing your own lists.

1. Videos will be played in the order listed in these files. You will be able to specify which list you would like to use when you run the experiment.

2. The column headers **MUST** be included and **MUST** use this exact phrasing in found in the pilot file.

3. The video file **MUST** specify the file extension (*e.g.* .avi, .mp4). Multiple formats are supported however which format depends on the version of Psychopy you are using.

4. All videos are assumed to be stored in the ../infant-stimuli/videos/ directory.

5. The 'TrialType' is used to keep track of what kind of stimuli this is and is recorded in data output. This is useful when analyzing fMRI data.
