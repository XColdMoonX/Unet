import os
import subprocess


# PredictPath = "D:\\Jonas\\PythonSpace\\Pytorch-UNet\\predict.py" #predict.py的路徑
# ModelPath = "D:\\Jonas\\PythonSpace\\checkpoint\\1_checkpoint_epoch1.pth" # model.pth的路徑
# InputDir = "D:\\Jonas\\RiverData\\301"  # 輸入資料夾
# OutputDir = "D:\\Jonas\\RiverData\\301_Pre"  # 輸出資料夾

def all_predict(PredictPath,ModelPath,InputDir,OutputDir):
    # 獲取輸入資料夾中的所有.jpg檔案
    input_files = [f for f in os.listdir(InputDir) if f.endswith('.jpg')]

    # 使用tqdm來創建進度條
    for file in input_files:
        print(f"Processing file: {file}")  # 顯示目前正在處理的檔案
        InputPath = os.path.join(InputDir, file)  # 完整的輸入檔案路徑
        OutputPath = os.path.join(OutputDir, file)  # 完整的輸出檔案路徑

        # 執行 "python predict.py -m ModelPath -i InputPath -o OutputPath" 指令
        subprocess.run(["python", PredictPath, "-m",
                        ModelPath, "-i",
                        InputPath, "-o",
                        OutputPath], check=True)
