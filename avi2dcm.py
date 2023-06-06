import argparse
#hacky exception handling
import numpy as np
np.float = np.float64
np.int = np.int_

import SimpleITK as sitk
import skvideo.io  
import os
##warp in main function
def main(input):
    #check if input is a folder
    if os.path.isdir(input):
        for file in os.listdir(input):
            if file.endswith(".avi"):
                convert(os.path.join(input, file))
    else:
        convert(input)
    return

def convert(fpath):
    filename = os.path.basename(fpath)
    videodata = skvideo.io.vread(fpath)
    videodata = videodata[:,:,:,0]#.transpose(2,1,0)
    transf_matrix = np.array([[0,0,-1,0],[0,-1,0,0],[1,0,0,0],[0,0,0,1]])
    #save with SimpleITK as dcm
    sitk_img = sitk.GetImageFromArray(videodata)
    sitk_img.SetSpacing((1,1,1))
    sitk_img.SetOrigin((0,0,0))
    sitk_img.SetMetaData("0010|0010", str(filename))
#    sitk_img.SetMetaData("0010|0020", str(filename))
#    sitk_img.SetMetaData("0020|000d", str(filename))
    sitk_img.SetMetaData("0008|0060", "US")
    sitk.WriteImage(sitk_img, fpath.replace(".avi",".dcm"))
    print("Converted "+fpath)
    return

##write arparse
parser = argparse.ArgumentParser(description='Converts avi to dcm. Either call it on a single file or a folder containing avi files.')
parser.add_argument('input', metavar='input', type=str, nargs='+',
                     help='input file')
args = parser.parse_args()

##call main function
main(args.input[0])


#s
#python avi2nii.py sample/Image02.avi sample/Image02.nii.gz


