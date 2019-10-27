# Stimuli List Creation Tool
Creates randomized block design stimuli lists.

Trials within blocks are fully randomized, each block represents 
a unique order of trials and blocks are chosen so that no stimuli 
will be presented twice in a row.

This is implemented by creating all possible permutations of 
stimuli types within a block and randomly sampling (without replacement) 
subject to the restriction that the trial type at the start of the 
next block is not the same as the last trial of the preceding block. 
This is repeated until there are no more blocks that can be chosen, 
with the remaining blocks writing to a "leftovers.csv" file.

This script can simply be run as is, or you can change the 
parameters indicated at the top of the file to create different 
variants of this design.