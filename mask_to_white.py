import os
from PIL import Image
import concurrent.futures

def Convert2white(input_image_path, output_image_path):
    try:
        with Image.open(input_image_path) as image:
            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            data = image.getdata()
            new_data = []
            for pixel in data:
                # 将红色值为 1 的像素转换为全透明的白色
                if pixel[0] == 1:
                    new_data.append((255, 255, 255, 0))
                else:
                    # 确保所有非黑色像素都转换为白色
                    if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
                        new_data.append((0, 0, 0, 255))  # 黑色
                    else:
                        new_data.append((255, 255, 255, 255))  # 白色

            image.putdata(new_data)
            image.save(output_image_path)
        print(f"Processed: {input_image_path}")
    except Exception as e:
        print(f"Error processing {input_image_path}: {e}")


def batch_convert(input_folder, output_folder):
    if not os.path.isdir(input_folder) or not os.path.isdir(output_folder):
        print("請輸入正確的資料夾路徑")
        return

    file_list = [file_name for file_name in os.listdir(input_folder) if file_name.endswith(".png")]
    if not file_list:
        print("No PNG files found in the input directory.")
        return

    print(f"Found {len(file_list)} PNG files to process.")
    # 限制线程池的大小
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(Convert2white, os.path.join(input_folder, file_name),
                                   os.path.join(output_folder, file_name)) for file_name in file_list]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error in thread: {e}")

    print("Batch conversion completed.")