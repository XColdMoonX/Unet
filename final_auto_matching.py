from all_image_predict import all_predict
from mask_dilation import dilation
from mask_to_white import batch_convert
from mask_to_make_color_river import mask_cut_image
from concat_pic import Merge
#  PredictPath、ModelPath、OriginDir必須已經存在
#  其他資料夾則可以存在or不存在
PredictPath = "D:\\Jonas\\PythonSpace\\Pytorch-UNet\\predict.py" #predict.py的路徑
ModelPath = "D:\\Jonas\\PythonSpace\\checkpoint\\2_checkpoint_epoch1_1.pth" # model.pth的路徑

OriginDir = "D:\\Jonas\\RiverData\\Test\\370"  # 初始原本圖片的資料夾
MaskDir = "D:\\Jonas\\RiverData\\Test\\370_Pre"  # 輸出遮罩的資料夾

DilationDir = "D:\\Jonas\\RiverData\\Test\\370_Pre_Dilation"  # 輸出膨脹的資料夾
DilationWihteDir = "D:\\Jonas\\RiverData\\Test\\370_Pre_Dilation_White"  # 輸出膨脹的白色遮罩的資料夾
CutDir = "D:\\Jonas\\RiverData\\Test\\370_Pre_Cut"  # 輸出切割的資料夾
MergerDir = "D:\\Jonas\\RiverData\\Test\\370_Merge"  # 輸出合併的資料夾

print("\033[31;40m Start \033[0m ")

#進行原圖預測
all_predict(PredictPath,ModelPath,OriginDir,MaskDir)    #  all_predict(PredictPath,ModelPath,InputDir,OutputDir,OutputExt = ".png")
print("\033[31;40m Predict Done \033[0m ")

#進行膨脹
dilation(MaskDir,DilationDir)                           #  dilation(input_folder,output_folder, iterations=20)
print("\033[31;40m Dilation Done \033[0m ")

#進行膨脹白色化
batch_convert(DilationDir,DilationWihteDir)             #  batch_convert(input_folder,output_folder)
print("\033[31;40m Convert Done \033[0m ")

#進行切割
mask_cut_image(DilationWihteDir,OriginDir,CutDir)       #  mask_cut_image(mask_folder, image_folder, output_folder)
print("\033[31;40m Cut Done \033[0m ")

#進行合併
Merge(CutDir,MergerDir)
print("\033[31;40m Merge Done \033[0m ")
