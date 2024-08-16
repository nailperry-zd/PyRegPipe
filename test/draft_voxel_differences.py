import numpy as np
import plotly.graph_objects as go

import numpy as np
import SimpleITK as sitk
import plotly.graph_objects as go

# 读取两个图像
pid = '019'
threshold = 0.5
# image1 = sitk.ReadImage(rf"C:\Users\dzha937\DEV\MRHIST_DataProcessing\MRHIST\mrhist{pid}\3d_slicer_script_output_tfm1harden_tfm2resample\(in_adc)_into_(ex_3d_cropped)_linear.nii")
image1 = sitk.ReadImage(rf"C:\Users\dzha937\DEV\MRHIST_DataProcessing\MRHIST\mrhist{pid}\3d_slicer4110_script_output_tfm1harden_tfm2resample\(in_adc)_into_(ex_3d_cropped)_linear.nii")
# image1 = sitk.ReadImage(rf"C:\Users\dzha937\DEV\MRHIST_DataProcessing\MRHIST\mrhist{pid}\manual_registration_output_tfm1harden_tfm2resample\(in_adc)_into_(ex_3d_cropped).nii")
image2 = sitk.ReadImage(rf"C:\Users\dzha937\DEV\MRHIST_DataProcessing\MRHIST\mrhist{pid}\check_results\(in_adc)_into_(ex_3d_cropped).nii")

# 将 SimpleITK 图像转换为 NumPy 数组
array1 = sitk.GetArrayFromImage(image1)
array2 = sitk.GetArrayFromImage(image2)

# 计算差异
difference = np.transpose(np.abs(array1 - array2))

# 创建 3D 网格
x, y, z = np.indices(difference.shape)

# 设置阈值以可视化显著差异

mask = difference > threshold

# Create meshgrid for coordinates
x, y, z = np.indices(difference.shape)

# 找出所有超过阈值的值
values_above_threshold = difference[mask]

print(f'{pid} shape is {difference.shape}')
print(f'{pid} values_above_threshold{-threshold} are {values_above_threshold.size} in total: {values_above_threshold}')

# Gather voxel positions where differences occur
x_diff = x[mask].flatten()
y_diff = y[mask].flatten()
z_diff = z[mask].flatten()

# Create a Plotly figure
fig = go.Figure()

# Check if there's any data to plot
if values_above_threshold.size > 0:
    # Plot the difference voxels
    fig.add_trace(go.Scatter3d(
        x=x_diff,
        y=y_diff,
        z=z_diff,
        mode='markers',
        marker=dict(size=10, color='cyan', opacity=0.8),
    ))

    # Set titles and labels
    fig.update_layout(
        title='Voxel Differences',
        scene=dict(
            xaxis_title='X Axis',
            yaxis_title='Y Axis',
            zaxis_title='Z Axis',
            xaxis=dict(nticks=difference.shape[0]),
            yaxis=dict(nticks=difference.shape[1]),
            zaxis=dict(nticks=difference.shape[2]),
        )
    )
    # Show the plot
    fig.show()
else:
    print("No differences detected.")

