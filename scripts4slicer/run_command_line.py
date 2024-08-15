import os
import sys
import subprocess
from fileutils import *
import os

def run_registration(env_var, exe_path, output_file, floating_file, reference_file, transform_path):
    os.environ["CMTK_WRITE_UNCOMPRESSED"] = env_var
    command = [exe_path, "-o", output_file, "--floating", floating_file, reference_file, transform_path]
    # Construct the command string
    command_str = f'"{exe_path}" -o "{output_file}" --floating "{floating_file}" "{reference_file}" "{transform_path}"'
    print(f'command line is {command_str}')
    subprocess.run(command, check=True)

if __name__ == "__main__":

    cmtk_path = r"C:\Users\dzha937\DEV\MRHIST_Code\PyRegPipe\Tools\CMTK-2.3.0-Windows-x86\bin\reformatx.exe"

    dest_dir = r"C:\Users\dzha937\DEV\MRHIST_DataProcessing\MRHIST"

    for i in range(5, 71):
        pid = str(i).zfill(3)
        mrhist_pid = f'mrhist{pid}'

        output_file_dir = os.path.join(dest_dir, mrhist_pid, '3d_slicer_script_output_tfm1harden_tfm2resample')
        create_directory_if_not_exists(output_file_dir)
        patient_dir = os.path.join(dest_dir, mrhist_pid)

        # process_what = 'in_adc'
        process_what = 'in_b2000'

        output_file_path = os.path.join(output_file_dir, f'({process_what})_into_(ex_3d_cropped)_deformable.nii.gz')
        # output_file_path = os.path.join(output_file_dir, f'{mrhist_pid}_(adc_refit)_into_(ex_3d)_deformable.nii')
        floating_file = os.path.join(output_file_dir, f'({process_what})_into_(ex_3d_cropped)_linear.nii')
        # floating_file = os.path.join(output_file_dir, f'{mrhist_pid}_(adc_refit)_into_(ex_3d)_linear.nii')
        reference_file = os.path.join(patient_dir, 'ex_3d_cropped.nii')
        transform_path = os.path.join(patient_dir, "warp_output_transform")

        if not os.path.exists(floating_file):
            print(f'{floating_file} not found, skipped')
            continue
        if not os.path.exists(reference_file):
            print(f'{reference_file} not found, skipped')
            continue
        if not os.path.exists(transform_path):
            print(f'{transform_path} not found, skipped')
            continue

        run_registration('1', cmtk_path, output_file_path, floating_file, reference_file, transform_path)