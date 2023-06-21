# Philament 
<p align=center>
   <a href="https://img.shields.io/pypi/l/localstack.svg"><img alt="PyPI License" src="https://img.shields.io/pypi/l/localstack.svg"></a>
   <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

# Overview

Phil is a Python script that allows for automated analysis of centroid objects
---
## Requirements

Numpy
TrackPy
Numba
PIMS
Pandas

## Installing

1) Download all .py files, as well as requrirements.txt
   
```powershell
pip install -r requirements.txt
```

5) Run phil_main.py in terminal ("python phil_main.py")
3)  from the terminal (make sure to be in the directory that has the requirements.txt file)
   
## Running

Running Philament is extremely simple, just run 
```powershell
python3 phil_main.py
```
in terminal and wait for the GUI to appear!

## Usage
Philament starting user interface:

![image](https://github.com/maxwellbowser/philament/assets/107726558/e7c1fe65-7006-4170-b5ed-b91cdb83aa87)



### Pixel size:
In figure 1, above, “Pixel size” is the scale factor for the camera setup used. This allows for the conversions from pixel to a real-world measurement, such as microns/sec rather than pixels/second. With the value 0.139, this indicates that each pixel is 0.139 units of size in width and height. If the output is desired in pixel measurements, this field can be set to 1. 

### Object diameter:
This parameter gives a minimum size for an object’s diameter to be recognized. If there is a great deal of noise in thresholded videos, despite Phil’s preprocessing, make sure to set this value larger than the kernels of static. This value cannot be an even number (e.g., 12, 20, 28), due to parameters set in place by the Trackpy package. The trackpy documentation author advises, “When in doubt, round up”. (http://soft-matter.github.io/trackpy/dev/generated/trackpy.batch.html)

### Files per condition:
To ensure that the output data is automatically grouped by experimental condition, each condition passed to Phil needs to have equal numbers of samples collected. For example, if there are 10 videos taken for 50ug Myosin, and 12 videos taken for 100ug Myosin, the conditions must be analyzed separately, or the 100ug Myosin dataset must be trimmed down to 10 videos. However,  there is no limit to the number of conditions that can be analyzed at one time, or to the number of samples that can be included in each condition (e.g., you could have 100 conditions with 100 samples in each, the processing time would simply be longer).

### Tracking memory:
The object tracking memory indicates the maximum number of frames an object can be lost before being regained, and still be labeled as the same object. If the microscope slide momentarily drops out of focus, Philament will be able to remember the placement of the objects and continue tracking the same objects where they left off. This feature allows Phil to accurately register objects present, by not counting the same objects twice, while also properly describing the paths that objects took during recordings. 

### Search radius:
The search radius limits the area in which a filament can move from frame to frame and be linked to the same path. This is necessary for keeping linked paths accurate, however, a number that is too small can set an artificially low maximum velocity for tracked objects. This value is highly recommended to be based on experimental testing, and the changes in position possible by the user’s model system. A value that is too generous will also prevent proper tracking of multiple objects as their search radii would have too much cross-over, and frame-to-frame motions between objects would not be distinguishable.

### Frames per second (FPS):
The FPS of an experimental setup depends on the camera and capture software used, which varies from setup to setup. Please refer to your camera manufacturer’s user guide or capture software to determine your FPS. This value is something to keep in mind when testing values for object tracking memory, as higher shutter speeds can actually decrease the time allowed for an object’s path to be retained. For example, if you set the object memory to 5 frames and have a camera that captures 5 frames per second, objects will have 1 second to return to view before their paths are not continued. However, if your camera captures 20 frames per second, then objects will only have a quarter of the time (0.25 seconds) to return to view. In our testing, it took around 1 second for us to regain focus while operating the microscope, and we set our tracking memory accordingly.

### Naming Convention:
Philament uses a specific naming convention field to identify the file number and the condition of the experiment within the filename. Users need to follow this convention, otherwise unexpected behaviors in the program can occur. 

Rules of thumb:
1)	Keep filenames consistent within the same condition (05ugMyosin-01, 05ugMyosin-02… 05ugMyosin-10)
2)	Put file numbers at the end of file names
3)	Add 0’s to single-digit file numbers, if including double-digit file numbers.  

For example, an experiment studying interactions between actin and myosin, may have the base file name “Actin05ugMyosin01, and Philament needs to differentiate that the condition is “Actin05ugMyosin”, and this is the first run, “01” (rather than mistakenly setting the condition as “ActinugMyosin01”, and the file number as “05”). By providing an example file name in the naming convention entry, “Actin05ugMyosin\*01\*”, you are providing the positional information of where run numbers are contained within the file name. Philament is able to compensate for any other changes in the filename, as long as the file number stays in the same position relative to the end of the file name. 

For example, the table below shows how Philament handles files in a given run when provided the naming convention: Actin05ugMyosin\*01\*
| Input file names | Condition | File Number |
|------------------|-----------|-------------|
| Actin10ugMyosin02	| Actin10ugMyosin |	02 |
|Actin20ugMyosin01 | Actin20ugMyosin | 01 |
| Actin1000ugMyosin10 | Actin1000ugMyosin | 10 |


### Full object data:
Moving to the right side of  figure 1, the option for including full object data (described more in depth in the results section), includes the full output dataframe from trackpy, as well as the comma separated value (CSV) file that we designed. The full object data contains the information for each frame of each object tracked, meaning the file could be 50x larger than the default output CSV (or if the videos contain 100 frames, they could be 100x larger). 

### Folder naming:
The desired folder name allows the user to change the name of the folder that is created to store all of the thresholded videos and output CSV files. The only non-adjustable attribute is that the output folder name will always include the suffix “-Analyzed Files”. This was done for convenience’s sake so that folders of the analyzed and regular files are easily distinguishable. If desired, this behavior can be changed in the source code by adjusting line 290 in phil_main.py (line number may change before publication)

### Filtering Options:
To remove bias from data output, Philament returns object data unfiltered, leaving the data trimming up to individual users’ preferences. We have provided an Excel spreadsheet that uses 3 filters to separate stalled filaments, exclude objects tracked for short periods, and remove objects with unusual motion patterns. The values we used to filter out data were determined experimentally, by testing a range of values and cross-checking original movies by eye to see if properly moving filaments were excluded or not. We recommend users make modifications and adjustments to this Excel spreadsheet based on their own findings, as the filter values used for our experimental setup may improperly filter objects/filaments of another. 

Our reasoning for excluding filters internally with Phil was to avoid bias as much as possible, so that users have full access to their raw data, and can then choose to exclude objects at their own discretion. 
