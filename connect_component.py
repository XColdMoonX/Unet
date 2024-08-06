import os
import numpy as np
import cv2
import concurrent.futures


def select_max_region(mask):
    nums, labels, stats, centroids = cv2.connectedComponentsWithStats(
        mask, connectivity=8
    )
    background = 0
    for row in range(stats.shape[0]):
        if stats[row, :][0] == 0 and stats[row, :][1] == 0:
            background = row
    stats_no_bg = np.delete(stats, background, axis=0)
    max_idx = stats_no_bg[:, 4].argmax()
    max_region = np.where(labels == max_idx + 1, 1, 0)
    return max_region


def imageSelect(input_image_path, output_image_path):
    try:
        # Skip if the output image already exists
        if os.path.exists(output_image_path):
            print(f"File {output_image_path} already exists. Skipping...")
            return

        # Read the image in grayscale
        img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
        # if img is None:
        #     raise FileNotFoundError(
        #         f"The image file '{input_image_path}' could not be opened."
        #     )

        # # Threshold the image to create a binary mask
        # _, mask = cv2.threshold(img, 20, 255, cv2.THRESH_BINARY)

        if img is None:
            raise FileNotFoundError(
                f"The image file '{input_image_path}' could not be opened."
            )

        # Check if the image is already in grayscale
        if len(img.shape) == 2:
            gray = img
        else:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        mask = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)[1]

        # Select the largest connected region
        mask = select_max_region(mask)

        # Save the result
        cv2.imwrite(output_image_path, mask * 255)
        print(f"Processed: {input_image_path}")
    except Exception as e:
        print(f"Error processing {input_image_path}: {e}")


def component(input_folder, output_folder):
    if not os.path.isdir(input_folder):
        print("請輸入正確的資料夾路徑")
        return

    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    file_list = [
        file_name
        for file_name in os.listdir(input_folder)
        if file_name.endswith(".png") or file_name.endswith(".jpg")
    ]
    if not file_list:
        print("No JPG files found in the input directory.")
        return

    print(f"Found {len(file_list)} JPG files to process.")
    # Limit the size of the thread pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(
                imageSelect,
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


# def main():
#     input_folder = r""
#     output_folder = r""
#     component(input_folder, output_folder)


# if __name__ == "__main__":
#     main()
