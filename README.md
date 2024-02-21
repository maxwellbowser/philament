# Philament  <a href="https://github.com/maxwellbowser/philament/blob/master/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue"></a>  <a href="https://www.cell.com/biophysreports/fulltext/S2667-0747(24)00006-5"><img alt= "Citation reference: DOI" src="https://img.shields.io/badge/DOI-10.1016/j.bpr.2024.100147-forestgreen"></a>  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

Philament (Phil for short) allows for automated analysis of centroid objects, specifically designed for the In-Vitro Motility assay. By implementing Phil in the workflow for data analysis, hours can be shaved off of analysis times by chaining automated, accurate, and reproducible tracking with an easy to use UI.

## Installing

1. Download the repository files (Green "<> Code" button, "Local" Tab, "Download ZIP")

2. Unzip all contents of the folder

3. Open a terminal (MacOS) or command prompt (Windows) and navigate to the unzipped folder

4. Run the following line, to install the required libraries
   
```
pip3 install -r requirements.txt
```

5. See below for running the program!

## Running

Using Philament is extremely simple and is done by running the main file with python3:
```
python3 phil_main.py
```

After a few moments, the GUI will appear, ready for analysis!

**Please note that phil_main.py, phil_thresh.py, and phil_track.py must all be in the same directory (folder) to run properly.**

## Troubleshooting
If after running the line,
```
python3 phil_main.py
```
you get an error "Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Manage App Execution Aliases." then you may need to run Philament with a slightly different line.

```
python phil_main.py
```

## Usage
Philament starting user interface:

![SuppFig1](https://github.com/maxwellbowser/philament/assets/107726558/85452f61-17de-46d2-a386-fc9aacc887aa)


### Pixel Size:
“Pixel size” is the scale factor for the camera setup used. This allows for the conversions from pixel to a real-world measurement, such as microns/sec rather than pixels/second. The value 0.139, indicates that each pixel is 0.139 units of size in width and height. If the output is desired in pixel measurements, this field should be set to 1.

### Object Diameter:
The object diameter parameter gives a minimum size for an object’s diameter to be recognized. If there is a great deal of noise in thresholded videos, despite preprocessing, this value should be set larger than the kernels of static. This value cannot be an even number, due to parameters set in place by the TrackPy package. Documentation for TrackPy advises, “When in doubt, round up”. (http://soft-matter.github.io/trackpy/dev/generated/trackpy.batch.html)

### # of Files per Condition:
To ensure that the output data is automatically grouped by each experimental condition, each condition analyzed by Philament needs to have equal numbers of samples collected. For example, if there are 10 videos taken for 50 mg myosin, and 12 videos taken for 100 mg myosin, the conditions must be analyzed separately, or the 100ug myosin dataset must be trimmed down to 10 videos. However, there is no limit to the number of conditions that can be analyzed at one time, or to the number of samples that can be included in each condition (e.g., there could be 100 conditions with 100 samples in each, the processing time would simply be longer).

### Object Tracking Memory:
The object tracking memory indicates the maximum number of frames an object can be lost before being regained, and still be labeled as the same object. If the microscope slide momentarily drops out of focus, or the object being tracked crosses paths with another object, Philament will be able to remember the placement of the objects and continue tracking the same objects where they left off. This feature allows Philament to accurately register objects present, by not counting the same objects twice, while also properly describing the paths that objects took during recordings.

### Search Radius:
The search radius limits the area in which a filament can move from frame to frame and be linked to the same path. This is necessary for keeping linked paths accurate, however, a number that is too small can set an artificially low maximum velocity for tracked objects. This value is highly recommended to be based on experimental testing, and the changes in position possible by the user’s model system. A value that is too generous will also prevent proper tracking of multiple objects as their search radii would have too much cross-over, and frame-to-frame motions between objects would not be distinguishable.

### Frames Per Second (FPS):
The FPS of an experimental setup depends on the camera and capture software used, which varies from setup to setup. Please refer to the camera manufacturer’s user guide or capture software to determine the FPS. This value is something to keep in mind when testing values for object tracking memory, as higher shutter speeds can actually decrease the time allowed for an object’s path to be retained. For example, if object memory is set to 5 frames and the camera captures 5 frames per second, objects will have 1 second to return to view before their paths are not continued. However, if the camera captures 20 frames per second, then objects will only have a quarter of the time (0.25 seconds) to return to view. In our testing, it took around 1 second for us to regain focus while operating the microscope, and we set our tracking memory accordingly.

### Naming Convention:
Philament uses a specific naming convention field to identify the file number and the condition of the experiment within the filename. Users need to follow this convention, otherwise, unexpected behaviors in the program can occur. 

Rules of thumb:
1)	Keep filenames consistent within the same condition (05ugMyosin-01, 05ugMyosin-02… 05ugMyosin-10)
2)	Put file numbers at the end of file names
3)	Add 0’s to single-digit file numbers, if including double-digit file numbers.  

For example, an experiment studying interactions between actin and differing concentrations of myosin may have the base file name “Actin05ugMyosin01. The program needs to differentiate that the condition is “Actin05ugMyosin”, and that this is the first run, “01” (rather than mistakenly setting the condition as “ActinugMyosin01”, and the file number as “05”). By providing an example file name in the naming convention entry, “Actin05ugMyosin*01*”, the user is providing the positional information of where run numbers are contained within the file name. Philament can compensate for any other changes in the filename, as long as the file number stays in the same position relative to the end of the file name.

As an example, the table below shows how Philament handles files in a given run when provided the naming convention: Actin05ugMyosin*01*
| Input file names | Condition | File Number |
|------------------|-----------|-------------|
| Actin10ugMyosin02	| Actin10ugMyosin |	02 |
|Actin20ugMyosin01 | Actin20ugMyosin | 01 |
| Actin1000ugMyosin10 | Actin1000ugMyosin | 10 |

 
### Full Object Data:
Moving to the right side of Figure 1, the option for including full object data (described more in-depth in the results section), includes the full output data frame from TrackPy, as well as the comma-separated value (CSV) file that was designed. The full object data contains the information for each frame of each object tracked, meaning the file could be 50x larger than the default output CSV (or if the videos contain 100 frames, they could be 100x larger).

### Folder Naming:
The desired folder name allows the user to change the name of the folder that is created to store all of the thresholded videos and output CSV files, which by default, contains the current date (in the operating system’s format). The only non-adjustable attribute is that the output folder name will always include the suffix “-Analyzed Files”. This was done for convenience so that folders of analyzed and regular files are easily distinguishable.

### Filtering Options:
To remove bias from data output, Philament returns object data unfiltered, leaving the selection of data to be used (i.e., “trimming up”) to individual users’ preferences. An Excel template has been provided that uses 3 filters to separate stalled filaments, exclude objects tracked for short periods, and remove objects with unusual motion patterns. The values used to filter out data were determined experimentally, by testing a range of values and cross-checking original videos by eye to see if properly moving filaments were excluded or not. It is recommended that users make modifications and adjustments to this Excel spreadsheet based on their own findings, as the filter values used for our experimental setup may improperly filter objects/filaments of another experimental design.
The rationale for excluding filters internally with Philament is to avoid bias as much as possible, so that users have full access to their raw data, and can then choose to exclude objects at their own discretion.

Information on Output File and Full Data Output can be found at (https://github.com/maxwellbowser/philament).

To allow for fast comparisons of many conditions, we have also implemented an output summary file, which displays for each condition, the total average speed, SEM, and number of tracks per condition. These statistics, however, do not include filtering, as our goal is to return raw data to the user which may be filtered according to their preferences.

## Notes:

To strike a balance between user-friendly and customization, we chose to make some parameters of the tracking non-GUI adjustable. These variables are marked within the code and can be adjusted there. 

### Search Kernel:
- This can be adjusted in phil_threshold.py, and there are two places this must be changed to have the desired effect. They are both saved as “kernel_size” which can be found with ctrl + f. Otherwise, the first instance is in the double_check function (which blurs the temp test thresholding images for the user) and the second is in the thresholding_files function, which does all of the blurring for the saved images. This did not seem important enough to include in the settings JSON file, so it was hard-coded in.

### Paths Image DPI (Dots-Per-Inch):
- The Paths image DPI refers to the resolution at which the path files are saved, if that option is selected in the main GUI. If one would like to use these path images in a presentation or publication, this is a very helpful variable to change. The default DPI is 150, and may be increased or decreased to any amount, (a rule of thumb is 400 is plenty clear enough for a publication, if enlarging, then higher is better). This is found in phil_track.py, again ctrl + f for “dpi”. Very simple to change, however we recommend that this is reduced for regular usage, to save on storage space.

### Thresholding Sample Size:
- By default, for every 50 files that are selected, one more image is added to the pool for thresholding (Max of 5). This can be adjusted in phil_threshold.py, in the sample_generation function. Documentation is written to guide the user through this, and if the user would like to change the max # of images shown, this can also be changed in the sample_generation function. Our low max # of samples (set at 5) was intentional, with our reasoning being that this is meant to be an automated process, so giving 20 sample images just turns it back into ImageJ, therefore we recommend keeping the max number low.

### GUI Scaling:
- To account for loaded images with extremely high resolutions, which need to be scaled for viewing, we designed Phil to have ratiometric GUIs. This means that the thresholding sample images will always be ½ of the width of the screen (so both regular and thresholded images can fit), no matter what the size of the captured image is. To adjust this is, it is a bit more involved, however not overwhelming. The code to do this is in both phil_main.py and phil_threshold.py, and we have added comments “SCALING” above all of the places needed to change it. We recommend adjusting small amounts before running to see the effect, but ultimately up to the user’s best judgment.	


