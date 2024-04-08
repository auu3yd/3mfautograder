# 3mfautograder
A python-based autograder for .3mf files produced by Bambu Studio

The current version is not finished. As such, no guarantees of functionality are made. 

If you would like to test or otherwise debug the script, there are a few things you should know. 

1. This script expects a certain (POSIX-compliant) file layout. 
I advise running the script in its own directory. 
2. You should have two directories in the same directory as the script: fileinput and csv. 
You should place validc.csv into the csv directory. That should be the only thing in that directory.
2b. fileinput should be otherwise empty apart from a single .3mf file. You will have to clear this folder before running the program again if debugging. This program was developed to be containerized, and as such I didn't really care about any file cleanup afterwards (as I'd just reset the container), but if testing in a native environment, you will need to empty this file. 

.3mf files produced by other applications in other places probably will not be reported as valid, but if you know how to navigate a .3mf file such that you know exactly what parameters to look for, then you should be able to easily modify the code as well as validc.csv in order to produce the correct functionality. 

Code in this repository is protected under the GPL V3.0 license, with all caveats and such that come with it (as outlined in the included LICENSE file.)





