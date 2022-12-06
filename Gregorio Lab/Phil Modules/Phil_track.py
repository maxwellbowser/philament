from math import sqrt
import trackpy as tp
import os
import os.path

import pandas as pd
import tifffile as tif


# to automatically adjust for users with higher fps or longer video sequences (we use 5 fps and 10 sec videos)
def column_naming(df_length, file_fps):

    df_dict = {0: 'First X', 1: 'First Y', 2: 'First Frame'}
    recip_fps = 1/file_fps

    for cell in range(3, df_length):
        df_dict[cell] = (recip_fps)
        recip_fps += 1/file_fps

    return df_dict


def tracking_data_analysis(split_list, progress, root, settings_list):

    # Tracking the objects & saving to excel sheet (does i .tif videos at a time, specified by sheet_size)
    pixel_size = settings_list[0]
    object_area = settings_list[1]
    full_obj_data = settings_list[2]
    trk_memory = settings_list[4]
    search_range = settings_list[5]
    trk_algo = settings_list[6]
    fps = settings_list[7]

    for j in range(0, len(split_list)):

        # Defining Variables
        full_obj_df = pd.DataFrame()
        final_df = pd.DataFrame()

        for i in range(0, len(split_list[j])):

            displacement_df = pd.DataFrame()

            progress.set(progress.get() + 1)
            root.update()

            # Specifing which movie the data came from
            filename = os.path.basename(split_list[j][i])
            file_num = int(filename[-6:-4])

            obj_size_list = []

            frames = tif.imread(f'{split_list[j][i]}')

            # tracking the objects & collecting obj information like position, size, brightness, ect.
            f = tp.batch(frames[:], object_area, invert=True,
                         engine=trk_algo, processes='auto')

            # Linking the objects / tracking their paths
            linked_obj = tp.link_df(f, search_range, memory=trk_memory)
            linked_obj = linked_obj.sort_values(
                by=['particle', 'frame'])

            # This section is getting the speed and positional data about the objects
            # The data is formatted as follows (example data):
            #
            # 1st X | 1st Y | First Frame | {reciprocal_fps} * 1 | {reciprocal_fps} * 2 | {reciprocal_fps} * 3 | ect..
            # ---------------------------------------------------------------------------------------------------------
            #  150  |  150  |      0      | These sections are the instantaneous speed of the object at each frame
            #  200  |  200  |      0      |    1.2 (Microns/sec) |          2.3         |            0.5       |
            #  168  |  15   |      2      |         0.3          |          0.8         |            1.2       |

            # dd_values =  desired displacement values
            dd_values = linked_obj[['particle', 'frame', 'x', 'y']]
            total_objs = dd_values['particle'].iloc[-1]
            reciprocol_fps = 1/fps

            # The workflow for this loop is to separate the data for each particle into a new dataframe,
            # find the initial object coordinates & first frame (so you can go back and locate the object).
            #
            # Then for each frame, the locations and frame numbers are used to find the change in distance
            # from frame to frame. This is then converted to an instantaneous velocity by multiplying by
            # the pixel size and dividing by the reciprocol fps, and this number is then added to the list.

            for particle in range(0, total_objs):

                pythag_df = dd_values[dd_values['particle']
                                      == particle]

                if len(pythag_df) > 1:
                    first_x = pythag_df['x'].iloc[0]
                    first_y = pythag_df['y'].iloc[0]
                    first_frame = pythag_df['frame'].iloc[0]
                    output_list = [first_x, first_y, first_frame]

                    for frame in range(1, len(pythag_df)):
                        Xn = pythag_df['x'].iloc[frame-1]
                        Yn = pythag_df['y'].iloc[frame-1]
                        Frame_n = pythag_df['frame'].iloc[frame-1]

                        Xn1 = pythag_df['x'].iloc[frame]
                        Yn1 = pythag_df['y'].iloc[frame]
                        Frame_n1 = pythag_df['frame'].iloc[frame]

                        frame_diff = Frame_n1 - Frame_n

                        displacement = sqrt(((Xn-Xn1)**2)+(Yn-Yn1)**2)
                        displacement = (
                            displacement * pixel_size)/(reciprocol_fps*frame_diff)
                        output_list.append(displacement)

                    df = pd.DataFrame(output_list)
                    displacement_df = pd.concat([displacement_df, df], axis=1)

                else:
                    pass

            displacement_df = displacement_df.rename(
                index=column_naming(len(displacement_df), fps))

            displacement_df = displacement_df.transpose()

            displacement_df.insert(
                0, "File", file_num, allow_duplicates=True)

            displacement_df = displacement_df.reset_index(drop=True)

            # Full object data option where all variables are saved (object x and y for each frame & object, lots of data!)
            if full_obj_data == True:
                df2 = linked_obj
                df2.insert(0, "File", file_num, allow_duplicates=True)
                full_obj_df = pd.concat([full_obj_df, df2])

            # This section is finding the # of pixels that are in each of the object (object size)
            desired_values = linked_obj[['frame', 'particle', 'mass']]
            total_objs = desired_values['particle'].iloc[-1]

            # loop to calculate mean and std for the particle size * brightness, which is converted into pixels by x/255
            for object in range(0, int(total_objs)):

                mass_df = desired_values[desired_values['particle'] == object]

                # If just one data point is available, obj is skipped
                if len(mass_df) > 1:
                    avg_mass = (mass_df['mass'].mean())/255
                    mass_std = (mass_df['mass'].std())/255

                    # Adding the mean and stdev of the object size to list
                    size_list = [avg_mass.round(2), mass_std.round(2)]
                    obj_size_list.append(size_list)

                else:
                    pass

            # Joining dfs
            obj_size_df = pd.DataFrame(obj_size_list, columns=[
                'Average Obj Size', 'Std of Obj Size'])

            output_df = obj_size_df.join(displacement_df)
            final_df = pd.concat([final_df, output_df])

        # This won't work for some reason, I'm trying to add a header to the left-most index column
        #final_df.columns.name = 'Obj'

        # Saving as excel (The automatic naming is based on the naming convention below)
        # Naming convention: Thresh-XXXXXXXXX-01.tif

        filename = os.path.basename(split_list[j][0])
        proper_name = filename[7:-7]
        final_df.to_excel(f'{proper_name}.xlsx', sheet_name='Analyzed Data')

        # Full object data option
        if full_obj_data == True:
            full_obj_df.to_excel(
                f'{proper_name}-Full Object Data.xlsx', sheet_name='Analyzed Data')
