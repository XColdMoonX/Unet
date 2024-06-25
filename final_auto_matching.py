from all_image_predict import all_predict
from mask_dilation import dilation
from mask_to_make_color_river import mask_cut_image

PredictPath = "D:\\Jonas\\PythonSpace\\Pytorch-UNet\\predict.py" #predict.py的路徑
ModelPath = "D:\\Jonas\\PythonSpace\\checkpoint\\1_checkpoint_epoch1.pth" # model.pth的路徑

OriginDir = "D:\\Jonas\\RiverData\\301"  # 初始原本圖片的資料夾
MaskDir = "D:\\Jonas\\RiverData\\301_Pre"  # 輸出遮罩的資料夾

DilationDir = "D:\\Jonas\\RiverData\\301_Pre_Dilation"  # 輸出膨脹的資料夾
CutDir = "D:\\Jonas\\RiverData\\301_Pre_Cut"  # 輸出切割的資料夾

all_predict(PredictPath,ModelPath,OriginDir,MaskDir)    #  all_predict(PredictPath,ModelPath,InputDir,OutputDir)
dilation(MaskDir,DilationDir)                           #  dilation(input_folder,output_folder)
mask_cut_image(DilationDir,OriginDir,MaskDir)           #  mask_cut_image(mask_folder, image_folder, output_folder)