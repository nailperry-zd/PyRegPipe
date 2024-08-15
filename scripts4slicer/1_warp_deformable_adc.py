# Resample the ADC and High-b maps into the
# ex 3d space
# Created by Yu Sun on 16/07/2021
# Modified by Zoe Dan Zhang on 08/08/2024

# To be run in 3D Slice
#  exec(open(r"C:\Users\dzha937\PycharmProjects\PyRegPipe\scripts4slicer\1_warp_deformable_adc.py").read())
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

pts = ['mrhist' + str(i).zfill(3) for i in range(33, 34)]

for eachP in pts:
    
    inImgL = path(dataDir, eachP, 'in_adc.nii')

    refImgL = path(dataDir, eachP, 'ex_3d_cropped.nii')
    
    outputDir = path(dataDir, eachP, '3d_slicer_script_output_tfm1harden_tfm2resample')
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
        print(f"Created directory: {outputDir}")
    outImgL_transition_harden = path(outputDir, '(in_adc)_to_(in_3d)_harden.nii')
    outImgL_transition_brainsresample = path(outputDir, '(in_adc)_to_(in_3d)_brainsresample.nii')
    outImgL = path(outputDir, '(in_adc)_into_(ex_3d_cropped)_linear.nii')
    
    tfmFileL_transition = path(dataDir, eachP, '(in_dwi_b50)_to_(in_3d).tfm')
    tfmFileL = path(dataDir, eachP, '(in_3d)_to_(ex_xd).tfm')
    intplMode = 'Linear'

    if not exists(inImgL, refImgL, tfmFileL):
        print(f'{inImgL} not found, skipped')
        continue
    if not os.path.exists(tfmFileL_transition):# patients 025,030,031,033
        # actually patients 025,030,031 are well aligned already according to the readme.rxt, using an identity tfm instead,
        # 033 not sure, no readme.rxt found
        # Rigid registration to in_3d: see code regFunc.py#step1_2
        # This can work because '(in_adc)_to_(in_3d).nii' is acquired by applying '(in_dwi_b50)_to_(in_3d).tfm' to 'in_adc.nii'
        rigidReg(fixedImg=os.path.join(dataDir, eachP, 'in_adc.nii'),
                 movingImg=os.path.join(dataDir, eachP, '(in_adc)_to_(in_3d).nii'),
                 outImg=None,
                 outTfm=tfmFileL_transition)
    else:
        print(f'Using existing transformation:\n\t{tfmFileL_transition}')

    # Rigid resampling---see code regFunc.py#step1_2, not really apply it, just for comparison
    ret = warpImg(inImg=inImgL,  # in_adc.nii
                  refImg=inImgL,  # in_adc.nii
                  outImg=outImgL_transition_brainsresample,  # (in_adc)_to_(in_3d).nii
                  pixelT='float',
                  tfmFile=tfmFileL_transition,
                  intplMode=intplMode,
                  labelMap=False)

    # Harden tfm---see code regFunc.py#step1_2
    ret = warpImg2(inImg=os.path.join(dataDir, eachP, 'in_adc.nii'),
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