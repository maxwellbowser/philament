from statistics import mean
import random
from tkinter import ttk


from tkinter.messagebox import showinfo
import os
import os.path
import sys
import cv2
import tifffile as tif
import tkinter as tk
from numpy import array
from pims import PyAVVideoReader

# this generates the sample size for showing the user images to
# threshold, as well as picking the videos to be used for said sample
def sample_generation(filepaths):
    multiples_of_50 = len(filepaths) // 50

    if multiples_of_50 == 1:
        num_files_for_threshold = 2

    elif multiples_of_50 == 2:
        num_files_for_threshold = 3

    elif multiples_of_50 == 3:
        num_files_for_threshold = 4

    elif multiples_of_50 >= 4:
        num_files_for_threshold = 5

    else:
        num_files_for_threshold = 1

    try:
        rand_file_num = random.sample(range(0, len(filepaths)), num_files_for_threshold)

    except:
        print("Please re-run program, and make sure to select files!")
        sys.exit()

    return rand_file_num, num_files_for_threshold


# Gui to help user find best thresholding value for videos (Picks a randomly chosen video to use)
# For larger sample sizes more videos will be tested
# Always at least 1 video, and capped at 5 if n > 200 (n is number of selected files)
def threshold_value_testing(List_of_Filepaths):

    # not super neccesary, but its easier to bundle these two commands together this way...
    # sorry Tim Peters
    def close():
        window.destroy()
        cv2.destroyAllWindows()

    # This function allows for the changing of thresholding values to also
    # change the image shown to the user. So if threshold changes from 50->60,
    # this function is called to reshow the image with the updated threshold.
    def double_check(value):

        blur = cv2.medianBlur(checking_images[0], 5)

        ret, thresholded_checked = cv2.threshold(
            blur, threshold_value.get(), 255, cv2.THRESH_BINARY_INV
        )

        cv2.imshow("Thresholded Image", thresholded_checked)
        cv2.imshow("Original Image", checking_images[0])
        cv2.waitKey(5)

    thresh_values = []
    rand_file_num, num_files_for_threshold = sample_generation(List_of_Filepaths)

    is_avi = False
    if "avi" in List_of_Filepaths[rand_file_num[0]][-3:]:
        is_avi = True

    # running the thresholding picker gui
    for i in range(0, len(rand_file_num)):

        window = tk.Tk()
        window.title("Checking Thresholding Value")
        window.geometry("425x250")
        window.resizable(False, False)
        window.eval("tk::PlaceWindow . center")

        thresh_check_frame = ttk.Frame(window, padding="5 5 10 10")
        thresh_check_frame.grid(column=0, row=0)
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)

        checking_images = []
        current_num = i + 1
        if is_avi == True:

            checking_images = PyAVVideoReader(List_of_Filepaths[rand_file_num[i]])

        else:
            loaded, checking_images = cv2.imreadmulti(
                mats=checking_images,
                filename=List_of_Filepaths[rand_file_num[i]],
                flags=cv2.IMREAD_GRAYSCALE,
            )

        # Here 100 is just a default starting point for the thresholding value
        threshold_value = tk.IntVar(thresh_check_frame, 100)

        # Widgets! I chose not to show threshold value to eliminate human bias & simplicity
        slider = ttk.Scale(
            thresh_check_frame,
            from_=255,
            to=0,
            orient="horizontal",
            variable=threshold_value,
            command=double_check,
            length=200,
        ).grid(column=0, row=1)

        cont_but = ttk.Button(thresh_check_frame, text="Continue", command=close).grid(
            column=1, row=1, padx=10, pady=5
        )

        ttk.Label(
            thresh_check_frame, text="Select best thresholding value:", font=12
        ).grid(column=0, row=0, padx=20, pady=10)
        ttk.Label(
            thresh_check_frame,
            text=f"Image {current_num} out of {num_files_for_threshold}",
        ).grid(column=1, row=0, padx=20, pady=10)

        double_check(0)
        thresh_check_frame.mainloop()
        thresh_values.append(threshold_value.get())

    # setting the thresholding value to be used when thresholding
    threshold_value = int(mean(thresh_values))
    return threshold_value, is_avi


def thresholding_files(filepath, threshold_value, progress, root, is_avi, fps):
    # Start of the data analysis, the thresholding and saving of files
    try:
        for i in range(0, len(filepath)):
            # incase someone selects non-files
            assert os.path.isfile(filepath[i])
            try:
                threshold_images = []
                original_images = []
                filename = os.path.basename(filepath[i])

                if is_avi == True:

                    original_images = PyAVVideoReader(filepath[i])

                    avi_size = original_images.frame_shape

                    fourcc = cv2.VideoWriter_fourcc(*"XVID")
                    avi_image = cv2.VideoWriter(
                        "Thresh-" + filename, fourcc, fps, (avi_size[1], avi_size[0])
                    )

                else:
                    loaded, original_images = cv2.imreadmulti(
                        mats=original_images,
                        filename=f"{filepath[i]}",
                        flags=cv2.IMREAD_GRAYSCALE,
                    )

                for x in range(0, len(original_images)):

                    # Image processing (blur & thresholding)
                    blur = cv2.medianBlur(original_images[x], 5)

                    ret, image = cv2.threshold(
                        blur, threshold_value, 255, cv2.THRESH_BINARY_INV
                    )

                    if is_avi == True:
                        avi_image.write(image)

                    else:
                        threshold_images.append(image)

                if is_avi == True:
                    avi_image.release()

                else:
                    threshold_array = array(threshold_images)
                    tif.imwrite("Thresh-" + filename, threshold_array)

                progress.set(i + 1)
                root.update()

            except AssertionError:
                showinfo(
                    title="Assertion Error",
                    message=f"Sorry, there was an error with: {filename[i]}\nPhil couldn't determine if it is a file or not.\nPlease try again.",
                )

    # There were a few times I got a random NameError, so added this
    except NameError:
        showinfo(
            title="Error",
            message=f"Phil encountered a NameError. Try rerunning the program, and ensure all files selected are .tif image sequences",
        )
        sys.exit()
