import cv2
import numpy as np
import os

def dilation(Input_folder,output_folder):
    # 定义膨胀核
    kernel = np.ones((5, 5), np.uint8)  # 这里的(5, 5)可以根据需求调整膨胀核的大小

    # 指定输入文件夹和输出文件夹
    # Input_folder = "D:\Python practice\practice 1\Pytorch-UNet-3.0\data\BW\MASK"
    # output_folder = "D:\Python practice\practice 1\Pytorch-UNet-3.0\data\BW\FIXD_MASK"

    # 确保输出文件夹存在，如果不存在則創建
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(Input_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            # 若膨脹後的圖片已存在，則跳過
            if os.path.exists(os.path.join(output_folder, filename)):
                print(f"File {filename} already exists in output directory. Skipping...")
                continue
            # 读取图片
            filepath = os.path.join(Input_folder, filename)
            image = cv2.imread(filepath, 0)  # 以灰度模式读取

            erode_image = cv2.erode(image, kernel, iterations = 10)
            # 进行膨胀操作
            dilated_image = cv2.dilate(erode_image, kernel, iterations = 40)

            # 写入膨胀后的图片到输出文件夹
            output_filepath = os.path.join(output_folder, filename)
            cv2.imwrite(output_filepath, dilated_image)

            print(f'{filename} processed.')

    print('All images diation end.')
