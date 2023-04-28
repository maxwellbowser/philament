from math import sqrt
import trackpy as tp
import os
import os.path
import cv2

import pandas as pd
import tifffile as tif
from pims import PyAVVideoReader


# to automatically adjust for users with higher fps or longer video sequences (we use 5 fps and 10 sec videos)
def column_naming(df_length, file_fps):
    df_dict = {
        0: "Particle",
        1: "First X",
        2: "First Y",
        3: "First Frame",
        4: "Distance",
    }
    recip_fps = 1 / file_fps

    # This loop writes the intervals between frames in seconds.
    # For a 5fps movie, 10 sec long, the intervals will be in 1/5fps (0.2) seconds
    # and will contain 50 cells (the calculation on line 28 is just
    # getting the time passed, starting with 0.2 + 0.2 = 0.4)
    for cell in range(5, df_length):
        df_dict[cell] = recip_fps
        recip_fps += 1 / file_fps

    return df_dict


# Apologies if this is overdocumentation
"""
tracking_data_analysis
Inputs:
split_list -> nested lists containing the pathnames for preprocessed .tif image sequences
progress -> int used for progress window
root -> tk root of progress window
settings_list -> list containing the user defined parameters, such as search radius and tracking memory
name_indices -> tuple containing the negative indices of the file number, to keep track of which video the analyzed data came from

            Workflow
--------------------------------
1. for (loop) number of conditions

    a. create/clear dataframes which will contain all the positional data

    b. for (loop) files in condition
        * increase progress bar by 1 (since it starts at 0)
        * separate filename and filenumber
        * read .avi/.tif files (is_avi = True/False) 

        * trackpy batch track and link objects
        * sort datapoints by particle and frame
        * separate out unwanted data (only frame, x, y, and particle #)

        * for (loop) objects in tracked file
            - find first/last x & y values (.iloc) 
            - calculate total distance travelled (pythagorean equation)
            - save first frame, first x/y, and particle number with distance

            - for (loop) # of frames object is tracked
                > calculate distances travelled and speed from frame to frame (pythag. eq.)
                > append value to list & repeat
            
            - combine speed df and positional info df
            - add to condition file
        
        * save condition file with all movies data 

        * for (loop) objects in tracked file
            - calculate mean and std of object size

        * join object size and condition file together
        * add to output dataframe with all the other data in that condition
    
    c. save .CSV file with data from all files in the condition 
    

"""


def tracking_data_analysis(split_list, progress, root, settings, name_indices, is_avi):
    # Tracking the objects & saving to excel sheet (does i .tif videos at a time, specified by sheet_size)
    for j in range(0, len(split_list)):
        # Defining Variables / Clearing Dataframes
        full_obj_df = pd.DataFrame()
        final_df = pd.DataFrame()

        for i in range(0, len(split_list[j])):
            displacement_df = pd.DataFrame()

            progress.set(progress.get() + 1)
            root.update()

            # Specifing which movie the data came from
            filename = os.path.basename(split_list[j][i])
            file_num = int(filename[name_indices[0] : name_indices[1]])

            obj_size_list = []

            if is_avi == True:
                frames = PyAVVideoReader(split_list[j][i])

                avi_array = []
                for x in range(0, len(frames)):
                    avi_array.append(cv2.cvtColor(frames[x], cv2.COLOR_BGR2GRAY))
                frames = avi_array

            else:
                frames = tif.imread(split_list[j][i])

            # tracking the objects & collecting obj information like position, size, brightness, ect.
            f = tp.batch(
                frames[:],
                settings["object_area"],
                invert=True,
                engine="numba",
                processes="auto",
            )

            # Linking the objects / tracking their paths
            linked_obj = tp.link_df(
                f, settings["search_range"], memory=settings["trk_memory"]
            )
            linked_obj = linked_obj.sort_values(by=["particle", "frame"])

            # Uncomment the line below to get plots of object paths (ruins automation workflow)
            # tp.plot_traj(linked_obj)

            # This next section is getting the speed and positional data about the objects
            # The data is formatted as follows (example data):
            #
            # 1st X | 1st Y | First Frame | Distance |{reciprocal_fps} * 1 | {reciprocal_fps} * 2 | {reciprocal_fps} * 3 | ect..
            # ---------------------------------------------------------------------------------------------------------
            #  150  |  150  |      0      |   18.6   |These sections are the instantaneous speed of the object at each frame
            #  200  |  200  |      0      |   8.2    |  1.2 (Microns/sec)  |          2.3         |            0.5       |
            #  168  |  15   |      2      |   1.55   |         0.3         |          0.8         |            1.2       |

            # dd_values stands for desired_displacement values
            dd_values = linked_obj[["particle", "frame", "x", "y"]]
            total_objs = dd_values["particle"].iloc[-1]
            reciprocol_fps = 1 / settings["fps"]

            # The workflow for this loop is to separate the data for each particle into a new dataframe, then
            # find the initial object coordinates & first frame (so you can go back and locate the object).
            #
            # Then for each frame, the object positions and frame numbers are used to find the change in distance
            # from frame to frame. This is converted to an instantaneous velocity by multiplying by
            # the pixel size and dividing by the reciprocol fps, and this number is appended to the list.

            for particle in range(0, total_objs):
                pythag_df = dd_values[dd_values["particle"] == particle]

                if len(pythag_df) > 1:
                    first_x = pythag_df["x"].iloc[0]
                    first_y = pythag_df["y"].iloc[0]
                    first_frame = pythag_df["frame"].iloc[0]
                    particle_num = pythag_df["particle"].iloc[0]
                    last_x = pythag_df["x"].iloc[-1]
                    last_y = pythag_df["y"].iloc[-1]

                    # In plain english, this is pythagorean theorem, (a^2 + b^2) = c^2,
                    # where a and b are the x and y distances travelled between frame n and frame n+1

                    distance = (
                        sqrt(((first_x - last_x) ** 2) + (first_y - last_y) ** 2)
                        * settings["pixel_size"]
                    )
                    output_list = [
                        particle_num,
                        first_x,
                        first_y,
                        first_frame,
                        distance,
                    ]

                    for frame in range(1, len(pythag_df)):
                        Xn = pythag_df["x"].iloc[frame - 1]
                        Yn = pythag_df["y"].iloc[frame - 1]
                        Frame_n = pythag_df["frame"].iloc[frame - 1]

                        Xn1 = pythag_df["x"].iloc[frame]
                        Yn1 = pythag_df["y"].iloc[frame]
                        Frame_n1 = pythag_df["frame"].iloc[frame]

                        frame_diff = Frame_n1 - Frame_n

                        displacement = sqrt(((Xn - Xn1) ** 2) + (Yn - Yn1) ** 2)
                        displacement = (displacement * settings["pixel_size"]) / (
                            reciprocol_fps * frame_diff
                        )

                        output_list.append(displacement)

                    output_list_df = pd.DataFrame(output_list)
                    displacement_df = pd.concat(
                        [displacement_df, output_list_df], axis=1
                    )

                # This removes particles only detected for a single frame
                else:
                    pass

            # By using the dictionary retuned in column_naming() this line renames the rows of the data frame
            # which is then transposed and set as the column names
            displacement_df = displacement_df.rename(
                index=column_naming(len(displacement_df), settings["fps"])
            )

            displacement_df = displacement_df.transpose()

            displacement_df.insert(0, "File", file_num, allow_duplicates=True)

            displacement_df = displacement_df.reset_index(drop=True)

            # Full object data option where all variables are saved (object x and y for each frame & object, lots of data!)
            if settings["full_obj_data"] == True:
                df2 = linked_obj
                df2.insert(0, "File", file_num, allow_duplicates=True)
                full_obj_df = pd.concat([full_obj_df, df2])

            # This section is finding the # of pixels that are in each of the object (object size)
            desired_values = linked_obj[["frame", "particle", "mass"]]
            total_objs = desired_values["particle"].iloc[-1]

            # This is how the obj_size DataFrame is formatted for the size of objects and file information
            # Average Obj Size | Std of Obj Size | File | Particle |
            # ----------------------------------------------------------
            #       14.86      |       7.38      |   1  |     0    |
            #       33.33      |       9.24      |   1  |     1    |
            #       55.06      |       5.18      |   1  |     2    |
            #       ect...     |       ect...    |ect...|   ect... |

            # Loop to calculate mean and std for the particle size * brightness,
            # which is converted into pixels by particle size/255
            for object in range(0, int(total_objs)):
                mass_df = desired_values[desired_values["particle"] == object]

                # If just one data point is available, obj is skipped, since you cant take a std from one data point
                if len(mass_df) > 1:
                    avg_mass = (mass_df["mass"].mean()) / 255
                    mass_std = (mass_df["mass"].std()) / 255

                    # Adding the mean and stdev of the object size to list
                    size_list = [avg_mass.round(2), mass_std.round(2)]
                    obj_size_list.append(size_list)

                else:
                    pass

            obj_size_df = pd.DataFrame(
                obj_size_list, columns=["Average Obj Size", "Std of Obj Size"]
            )

            # This is joining the two dataframes together, for the final/ output DataFrame
            output_df = obj_size_df.join(displacement_df)

            # output_df now looks like this:
            # Average Obj Size | Std of Obj Size | File | Particle | 1st X | 1st Y | First Frame | Distance |{reciprocal_fps} * 1 | {reciprocal_fps} * 2 | {reciprocal_fps} * 3 |
            # -----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------
            #       14.86      |       7.38      |   1  |     0    |  150  |  150  |      0      |   18.6   |These sections are the instantaneous speed of the object at each frame
            #       33.33      |       9.24      |   1  |     1    |  200  |  200  |      0      |   8.2    |  1.2 (Microns/sec)  |          2.3         |            0.5       |
            #       55.06      |       5.18      |   1  |     2    |  168  |  15   |      2      |   1.55   |         0.3         |          0.8         |            1.2       |
            #       ect...     |       ect...    |ect...|   ect... | ect...| ect...|    ect...   |  ect...  |       ect...        |         ect...       |           ect...     |

            final_df = pd.concat([final_df, output_df])

        filename = os.path.basename(split_list[j][0])
        proper_name = filename[7 : name_indices[0]]
        final_df.to_csv(f"{proper_name}.csv", index=0)

        # Full object data option
        if settings["full_obj_data"] == True:
            full_obj_df.to_csv(f"{proper_name}-Full Object Data.csv")
