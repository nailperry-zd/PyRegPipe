# Resample the ADC and High-b maps into the
# ex 3d space
# Created by Yu Sun on 16/07/2021
# Modified by Zoe Dan Zhang on 08/08/2024

# To be run in 3D Slice
#  exec(open(r"C:\Users\dzha937\PycharmProjects\PyRegPipe\scripts4slicer\1_warp_deformable_highb.py").read())
# 
# pip_install('matplotlib')


import os
import sys
sys.path.append(r"C:\Users\dzha937\PycharmProjects\PyRegPipe")
from regFunc import *
def path(*parts):
    return os.path.realpath(os.path.join(*parts))

def exists(*filepath):
    return all([os.path.exists(f) for f in filepath])

dataDir = r'C:\Users\dzha937\DEV\MRHIST_DataProcessing\MRHIST'

pts = ['mrhist' + str(i).zfill(3) for i in range(5, 71)]

for eachP in pts:
    
    inImgL = path(dataDir, eachP, 'in_b2000.nii.gz')
    refImgL = path(dataDir, eachP, 'ex_3d_cropped.nii')
    tfmFileL_transition = path(dataDir, eachP, '(in_dwi_b50)_to_(in_3d).tfm')
    tfmFileL = path(dataDir, eachP, '(in_3d)_to_(ex_xd).tfm')
    intplMode = 'Linear'

    if not exists(inImgL, refImgL, tfmFileL):
        print(f'{inImgL} not found, skipped')
        continue

    outputDir = path(dataDir, eachP, '3d_slicer4110_script_output_tfm1harden_tfm2resample')
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
        print(f"Created directory: {outputDir}")
    outImgL_transition_harden = path(outputDir, '(in_b2000)_to_(in_3d)_harden.nii')
    outImgL_transition_brainsresample = path(outputDir, '(in_b2000)_to_(in_3d)_brainsresample.nii')
    outImgL = path(outputDir, '(in_b2000)_into_(ex_3d_cropped)_linear.nii')

    # Rigid resampling---see code regFunc.py#step1_2, not really apply it, just for comparison
    warpImg(inImg=inImgL,  # in_adc.nii
                  refImg=inImgL,  # in_adc.nii
                  outImg=outImgL_transition_brainsresample,  # (in_adc)_to_(in_3d).nii
                  pixelT='float',
                  tfmFile=tfmFileL_transition,
                  intplMode=intplMode,
                  labelMap=False)

    # Harden tfm---see code regFunc.py#step1_2
    ret = warpImg2(inImg=inImgL,
                 outImg=outImgL_transition_harden,#(in_adc)_to_(in_3d).nii
                 tfmFile=tfmFileL_transition #(in_dwi_b50)_to_(in_3d).tfm
                )

    print(ret)

    # Rigid resampling
    warpImg(inImg=outImgL_transition_harden,#(in_adc)_to_(in_3d).nii
            refImg=refImgL,
            outImg=outImgL,
            pixelT='float',
            tfmFile=tfmFileL,
            intplMode=intplMode,
            labelMap=False)