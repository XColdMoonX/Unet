import cv2
import numpy as np
import os
import concurrent.futures


def imageFill(input_image_path, output_image_path):
    try:
        # 若輸出圖片已經存在，則跳過
        if os.path.exists(output_image_path):
            print(f"File {output_image_path} already exists. Skipping...")
            return

        # 讀取灰度圖像
        image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

        # 二值化處理
        _, binary_image = cv2.threshold(image, 220, 255, cv2.THRESH_BINARY)

        # 使用 floodFill 填充
        flood_filled_image = binary_image.copy()
        height, width = binary_image.shape[:2]
        mask = np.zeros((height + 2, width + 2), np.uint8)
        cv2.floodFill(flood_filled_image, mask, (0, 0), 255)

        # 反轉填充的圖像
        flood_filled_image_inv = cv2.bitwise_not(flood_filled_image)

        # 組合二值化圖像和反轉的填充圖像
        final_image = binary_image | flood_filled_image_inv

        # 保存結果
        cv2.imwrite(output_image_path, final_image)
        print(f"Processed: {input_image_path}")
    except Exception as e:
        print(f"Error processing {input_image_path}: {e}")


def fill(input_folder, output_folder):
    if not os.path.isdir(input_folder):
        print("請輸入正確的資料夾路徑")
        return

    # 確保輸出文件夾存在，如果不存在則創建
    os.makedirs(output_folder, exist_ok=True)

    file_list = [
        file_name
        for file_name in os.listdir(input_folder)
        if file_name.endswith(".png")
    ]
    if not file_list:
        print("No PNG files found in the input directory.")
        return

    print(f"Found {len(file_list)} PNG files to process.")
    # 限制線程池的大小
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(
                imageFill,
                os.path.join(input_folder, file_name),
                os.path.join(output_folder, file_name),
            )
            for file_name in file_list
        ]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error in thread: {e}")


# 示例使用：
# input_folder = "path_to_input_folder"
# output_folder = "path_to_output_folder"
# batch_convert(input_folder, output_folder)
