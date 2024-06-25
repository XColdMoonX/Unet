import os
import subprocess
from tqdm import tqdm

# PredictPath = # predict.py的路徑
# ModelPath =   # model.pth的路徑
# Input_folder =    # 輸入資料夾
# output_folder =   # 輸出資料夾
# OutputExt =   # 輸出檔案的副檔名
def all_predict(PredictPath, ModelPath, Input_folder, output_folder, OutputExt):
    # 獲取輸入資料夾中的所有.jpg檔案
    input_files = [f for f in os.listdir(Input_folder) if f.endswith('.jpg')]

    # 确保输出文件夹存在，如果不存在則創建
    os.makedirs(output_folder, exist_ok=True)

    # 使用tqdm產生進度條
    for file in tqdm(input_files, desc="Processing files"):
        print(f"Processing file: {file}")  # 顯示目前正在處理的檔案
        InputPath = os.path.join(Input_folder, file)  # 完整的輸入檔案路徑
        OutputFileName = os.path.splitext(file)[0] + OutputExt  # 將輸出檔案的副檔名改為.png
        OutputPath = os.path.join(output_folder, OutputFileName)  # 完整的輸出檔案路徑

        # 檢查輸出資料夾中是否已經存在相同名稱的檔案，若有，則跳過這個檔案
        if os.path.exists(OutputPath):
            print(f"File {OutputFileName} already exists in output directory. Skipping...")
            continue

        # 執行 "python predict.py -m ModelPath -i InputPath -o OutputPath" 指令
        subprocess.run(["python", PredictPath, "-m",
                        ModelPath, "-i",
                        InputPath, "-o",
                        OutputPath], check=True)
        
# def all_predict(PredictPath, ModelPath, InputDir, OutputDir):
#     # 獲取輸入資料夾中的所有.jpg檔案
#     input_files = [f for f in os.listdir(InputDir) if f.endswith('.jpg')]
#     # 确保输出文件夹存在，如果不存在則創建
#     os.makedirs(output_folder, exist_ok=True)
#     for file in input_files:
#         print(f"Processing file: {file}")  # 顯示目前正在處理的檔案
#         InputPath = os.path.join(InputDir, file)  # 完整的輸入檔案路徑
#         OutputFileName = os.path.splitext(file)[0] + '.png'  # 將輸出檔案的副檔名改為.png
#         OutputPath = os.path.join(OutputDir, OutputFileName)  # 完整的輸出檔案路徑

#         # 檢查輸出資料夾中是否已經存在相同名稱的檔案，若有，則跳過這個檔案
#         if os.path.exists(OutputPath):
#             print(f"File {OutputFileName} already exists in output directory. Skipping...")
#             continue

#         # 執行 "python predict.py -m ModelPath -i InputPath -o OutputPath" 指令
#         subprocess.run(["python", PredictPath, "-m",
#                         ModelPath, "-i",
#                         InputPath, "-o",
#                         OutputPath], check=True)