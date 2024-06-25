import cv2
import os
import numpy as np

# 讀取圖片的路徑
#mask_folder = 'E:\\tool\\Pythonspace\\merge\\Riverpredict'
#image_folder = 'E:\\tool\\Pythonspace\\merge\\Riverseg'

def mask_cut_image(mask_folder, image_folder, output_folder):
    # 獲取圖片名稱列表
    mask_files = os.listdir(mask_folder)
    image_files = os.listdir(image_folder)

    # 确保输出文件夹存在，如果不存在則創建
    os.makedirs(output_folder, exist_ok=True)

    # 確保遮罩和圖片數量相同
    assert len(mask_files) == len(image_files), "Number of masks and images must be the same"

    # 遍歷每一個遮罩和圖片
    for mask_file, image_file in zip(mask_files, image_files):
        # 讀取遮罩和圖片
        mask = cv2.imread(os.path.join(mask_folder, mask_file), cv2.IMREAD_GRAYSCALE)
        image = cv2.imread(os.path.join(image_folder, image_file))
        # 若輸出圖片已經存在，則跳過
        if os.path.exists(os.path.join(output_folder, image_file)):
            print(f"File {image_file} already exists in output directory. Skipping...")
            continue
        
        # 確保遮罩和圖片的尺寸相同
        assert mask.shape == image.shape[:2], "Mask and image must have the same dimensions"

        # 創建一個全黑的圖片
        result = np.zeros_like(image)

        # 將遮罩區域的圖片保留下來
        result[mask == 255] = image[mask == 255]

        # 保存結果圖片
        cv2.imwrite(os.path.join(output_folder, image_file), result)