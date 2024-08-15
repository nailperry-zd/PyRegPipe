import os
from pathlib import Path
import SimpleITK as sitk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the root directory
root_dir = r"C:\Users\dzha937\DEV\MRHIST_DataProcessing\MRHIST"

# Initialize the lists to store the results
subdirs = []
max_diffs = []
min_diffs = []
med_diffs = []
mse_diffs = []

# Scan the subdirectories and process the files
for subdir in Path(root_dir).glob("mrhist[0-9][0-9][0-9]*"):
    print(f'subdir {subdir}')
    if "missing" not in str(subdir):
        in_adc_file = subdir / "3d_slicer_script_output_tfm1harden_tfm2resample" / "(in_adc)_into_(ex_3d_cropped)_linear.nii"
        check_file = subdir / "check_results" / "(in_adc)_into_(ex_3d_cropped).nii"
        # in_adc_file = subdir / "transition" / "(in_adc)_into_(ex_3d_cropped).nii"

        if in_adc_file.exists() and check_file.exists():
            in_adc_img = sitk.ReadImage(str(in_adc_file))
            check_img = sitk.ReadImage(str(check_file))

            in_adc_array = sitk.GetArrayFromImage(in_adc_img)
            check_array = sitk.GetArrayFromImage(check_img)

            diff_array = np.abs(in_adc_array - check_array)
            max_diff = np.max(diff_array)
            min_diff = np.min(diff_array)
            med_diff = np.median(diff_array)
            mse = np.mean((in_adc_array - check_array) ** 2)

            subdirs.append(str(subdir)[-2:])
            max_diffs.append(max_diff)
            min_diffs.append(min_diff)
            med_diffs.append(med_diff)
            mse_diffs.append(mse)

# Create the DataFrame and save it to an Excel file
df = pd.DataFrame({
    "Subdir": subdirs,
    "Max Diff": max_diffs,
    "Min Diff": min_diffs,
    "Medium Diff": med_diffs,
    "Mean Squared Error": mse_diffs
})

# df.to_excel("results.xlsx", index=False)
print("Results saved to 'results.xlsx'")

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(subdirs, max_diffs, label='Max Diff')
ax.plot(subdirs, min_diffs, label='Min Diff')
ax.plot(subdirs, med_diffs, label='Medium Diff')
ax.plot(subdirs, mse_diffs, label='Mean Squared Error')

# Set the labels and title
ax.set_xlabel('Subdir')
ax.set_ylabel('Value')
ax.set_title('script vs existing')
ax.legend()

# Show the plot
plt.show()