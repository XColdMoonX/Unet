from all_image_predict import all_predict
from mask_dilation import dilation
from mask_to_white import batch_convert
from mask_to_make_color_river import mask_cut_image
from concat_pic import Merge
#  PredictPath、ModelPath、OriginDir必須已經存在
#  其他資料夾則可以存在or不存在
PredictPath = "D:\\Jonas\\PythonSpace\\Pytorch-UNet\\predict.py" #predict.py的路徑
ModelPath = "D:\\Jonas\\PythonSpace\\checkpoint\\River_model_0702.pth" # model.pth的路徑

OriginDir = "D:\\Jonas\\RiverData\\Test\\361"  # 初始原本圖片的資料夾
MaskDir = OriginDir + "_Pre"  # 輸出遮罩的資料夾

DilationDir = OriginDir + "_Pre_Dilation"  # 輸出膨脹的資料夾
DilationWihteDir = OriginDir + "_Pre_Dilation_White"  # 輸出膨脹的白色遮罩的資料夾
CutDir = OriginDir + "_Pre_Cut"  # 輸出切割的資料夾
MergerDir = OriginDir + "_Merge"  # 輸出合併的資料夾

print("\033[31;40m Start \033[0m ")

#進行原圖預測
all_predict(PredictPath,ModelPath,OriginDir,MaskDir)    #  all_predict(PredictPath,ModelPath,InputDir,OutputDir,OutputExt = ".png")
print("\033[31;40m Predict Done \033[0m ")

#進行腐蝕與膨脹
dilation(MaskDir,DilationDir)                           #  dilation(input_folder,output_folder, kernelsize = 5, iterations=20)
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

# import shutil

# # 刪除指定的資料夾
# shutil.rmtree(MaskDir, ignore_errors=True)
# shutil.rmtree(DilationDir, ignore_errors=True)
# shutil.rmtree(DilationWihteDir, ignore_errors=True)
# shutil.rmtree(CutDir, ignore_errors=True)