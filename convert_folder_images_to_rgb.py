from PIL import Image
import os


def convert_folder_images_to_rgb(input_folder, output_folder):
    # 確認輸出資料夾是否存在，如果不存在則創建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍歷輸入資料夾中的所有檔案
    for filename in os.listdir(input_folder):
        # 確保只處理影像檔案
        if filename.lower().endswith(
            (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif")
        ):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            with Image.open(input_path) as img:
                # 檢查影像是否為 RGBA 模式
                if img.mode == "RGBA":
                    # 轉換為 RGB 模式
                    img = img.convert("RGB")
                    # 儲存轉換後的影像
                    img.save(output_path)
                    print(f"已將 {filename} 從 RGBA 轉換為 RGB，並儲存至 {output_path}")
                else:
                    # 將非 RGBA 的影像直接儲存到輸出資料夾
                    img.save(output_path)
                    print(
                        f"{filename} 不是 RGBA 模式，不需要轉換，已儲存至 {output_path}"
                    )


# 設定輸入和輸出資料夾的路徑
input_folder_path = r""
output_folder_path = r""

# 呼叫函數進行轉換
convert_folder_images_to_rgb(input_folder_path, output_folder_path)
