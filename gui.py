import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import configparser
import os
import shutil
from all_image_predict import all_predict  # 假设这些模块是你自己定义的
from mask_dilation import dilation
from mask_to_white import batch_convert
from mask_to_make_color_river import mask_cut_image
from concat_pic import Merge


def select_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)


def select_directory(entry):
    dir_path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, dir_path)


def save_config():
    config = configparser.ConfigParser()

    origin_dir = origin_dir_entry.get()
    base_dir = os.path.dirname(origin_dir)

    mask_dir = mask_dir_entry.get() or os.path.join(
        base_dir, os.path.basename(origin_dir) + "_Pre"
    )
    dilation_dir = dilation_dir_entry.get() or os.path.join(
        base_dir, os.path.basename(origin_dir) + "_Pre_Dilation"
    )
    dilation_white_dir = dilation_white_dir_entry.get() or os.path.join(
        base_dir, os.path.basename(origin_dir) + "_Pre_Dilation_White"
    )
    cut_dir = cut_dir_entry.get() or os.path.join(
        base_dir, os.path.basename(origin_dir) + "_Pre_Cut"
    )
    merger_dir = merger_dir_entry.get() or os.path.join(
        base_dir, os.path.basename(origin_dir) + "_Merge"
    )
    feature_dir = feature_dir_entry.get() or os.path.join(
        base_dir, os.path.basename(origin_dir) + "_Feature"
    )

    os.makedirs(mask_dir, exist_ok=True)
    os.makedirs(dilation_dir, exist_ok=True)
    os.makedirs(dilation_white_dir, exist_ok=True)
    os.makedirs(cut_dir, exist_ok=True)
    os.makedirs(merger_dir, exist_ok=True)
    os.makedirs(feature_dir, exist_ok=True)

    config["Paths"] = {
        "PredictPath": predict_path_entry.get(),
        "ModelPath": model_path_entry.get(),
        "OriginDir": origin_dir,
        "MaskDir": mask_dir,
        "DilationDir": dilation_dir,
        "DilationWhiteDir": dilation_white_dir,
        "CutDir": cut_dir,
        "MergerDir": merger_dir,
        "FeatureDir": feature_dir,
    }

    config["Dilation"] = {
        "kernel_size": kernel_size_entry.get(),
        "erode_iterations": erode_iterations_entry.get(),
        "dilate_iterations": dilate_iterations_entry.get(),
    }

    config["Concat"] = {
        "feature_extractor": feature_extractor_var.get(),
        "feature_matching": feature_matching_var.get(),
        "ratio": ratio_entry.get(),
    }

    with open("config.ini", "w") as configfile:
        config.write(configfile)

    print("Config file saved")


def execute_functions():
    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8-sig")

    PredictPath = config["Paths"]["PredictPath"]
    ModelPath = config["Paths"]["ModelPath"]
    OriginDir = config["Paths"]["OriginDir"]
    MaskDir = config["Paths"]["MaskDir"]
    DilationDir = config["Paths"]["DilationDir"]
    DilationWhiteDir = config["Paths"]["DilationWhiteDir"]
    CutDir = config["Paths"]["CutDir"]
    MergerDir = config["Paths"]["MergerDir"]
    FeatureDir = config["Paths"]["FeatureDir"]

    os.makedirs(MaskDir, exist_ok=True)
    os.makedirs(DilationDir, exist_ok=True)
    os.makedirs(DilationWhiteDir, exist_ok=True)
    os.makedirs(CutDir, exist_ok=True)
    os.makedirs(MergerDir, exist_ok=True)
    os.makedirs(FeatureDir, exist_ok=True)

    print("\033[31;40m Start \033[0m ")

    all_predict(PredictPath, ModelPath, OriginDir, MaskDir)
    print("\033[31;40m Predict Done \033[0m ")

    dilation(MaskDir, DilationDir)
    print("\033[31;40m Dilation Done \033[0m ")

    batch_convert(DilationDir, DilationWhiteDir)
    print("\033[31;40m Convert Done \033[0m ")

    mask_cut_image(DilationWhiteDir, OriginDir, CutDir)
    print("\033[31;40m Cut Done \033[0m ")

    Merge(CutDir, MergerDir)
    print("\033[31;40m Merge Done \033[0m ")


def update_entry(value):
    ratio_entry.delete(0, tk.END)
    ratio_entry.insert(0, format(float(value), ".2f"))


def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")

    predict_path_entry.insert(0, config["Paths"].get("PredictPath", ""))
    model_path_entry.insert(0, config["Paths"].get("ModelPath", ""))
    origin_dir_entry.insert(0, config["Paths"].get("OriginDir", ""))
    mask_dir_entry.insert(0, config["Paths"].get("MaskDir", ""))
    dilation_dir_entry.insert(0, config["Paths"].get("DilationDir", ""))
    dilation_white_dir_entry.insert(0, config["Paths"].get("DilationWhiteDir", ""))
    cut_dir_entry.insert(0, config["Paths"].get("CutDir", ""))
    merger_dir_entry.insert(0, config["Paths"].get("MergerDir", ""))
    feature_dir_entry.insert(0, config["Paths"].get("FeatureDir", ""))

    kernel_size_entry.insert(0, config["Dilation"].get("kernel_size", ""))
    erode_iterations_entry.insert(0, config["Dilation"].get("erode_iterations", ""))
    dilate_iterations_entry.insert(0, config["Dilation"].get("dilate_iterations", ""))

    feature_extractor_var.set(config["Concat"].get("feature_extractor", "sift"))
    feature_matching_var.set(config["Concat"].get("feature_matching", "bf"))
    ratio_entry.insert(0, config["Concat"].get("ratio", ""))


def clear_paths():
    config = configparser.ConfigParser()
    config.read("config.ini")

    config["Paths"]["PredictPath"] = ""
    config["Paths"]["ModelPath"] = ""
    config["Paths"]["OriginDir"] = ""
    config["Paths"]["MaskDir"] = ""
    config["Paths"]["DilationDir"] = ""
    config["Paths"]["DilationWhiteDir"] = ""
    config["Paths"]["CutDir"] = ""
    config["Paths"]["MergerDir"] = ""
    config["Paths"]["FeatureDir"] = ""

    with open("config.ini", "w") as configfile:
        config.write(configfile)

    predict_path_entry.delete(0, tk.END)
    model_path_entry.delete(0, tk.END)
    origin_dir_entry.delete(0, tk.END)
    mask_dir_entry.delete(0, tk.END)
    dilation_dir_entry.delete(0, tk.END)
    dilation_white_dir_entry.delete(0, tk.END)
    cut_dir_entry.delete(0, tk.END)
    merger_dir_entry.delete(0, tk.END)
    feature_dir_entry.delete(0, tk.END)

    messagebox.showinfo("Success", "Paths cleared successfully!")


def clear_related_paths(*args):
    mask_dir_entry.delete(0, tk.END)
    dilation_dir_entry.delete(0, tk.END)
    dilation_white_dir_entry.delete(0, tk.END)
    cut_dir_entry.delete(0, tk.END)
    merger_dir_entry.delete(0, tk.END)
    feature_dir_entry.delete(0, tk.END)


root = tk.Tk()
root.title("Parameter Selector")

tk.Label(root, text="Predict Path:").grid(row=0, column=0, padx=10, pady=5)
predict_path_entry = tk.Entry(root, width=50)
predict_path_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: select_file(predict_path_entry)).grid(
    row=0, column=2, padx=10, pady=5
)

tk.Label(root, text="Model Path:").grid(row=1, column=0, padx=10, pady=5)
model_path_entry = tk.Entry(root, width=50)
model_path_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: select_file(model_path_entry)).grid(
    row=1, column=2, padx=10, pady=5
)

tk.Label(root, text="Origin Directory:").grid(row=2, column=0, padx=10, pady=5)
origin_dir_entry = tk.Entry(root, width=50)
origin_dir_entry.grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: select_directory(origin_dir_entry)).grid(
    row=2, column=2, padx=10, pady=5
)
origin_dir_entry_var = tk.StringVar()
origin_dir_entry["textvariable"] = origin_dir_entry_var
origin_dir_entry_var.trace_add("write", clear_related_paths)

tk.Label(root, text="Mask Directory:").grid(row=3, column=0, padx=10, pady=5)
mask_dir_entry = tk.Entry(root, width=50)
mask_dir_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Dilation Directory:").grid(row=4, column=0, padx=10, pady=5)
dilation_dir_entry = tk.Entry(root, width=50)
dilation_dir_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Dilation White Directory:").grid(row=5, column=0, padx=10, pady=5)
dilation_white_dir_entry = tk.Entry(root, width=50)
dilation_white_dir_entry.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Cut Directory:").grid(row=6, column=0, padx=10, pady=5)
cut_dir_entry = tk.Entry(root, width=50)
cut_dir_entry.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Merger Directory:").grid(row=7, column=0, padx=10, pady=5)
merger_dir_entry = tk.Entry(root, width=50)
merger_dir_entry.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="Feature Directory:").grid(row=7, column=0, padx=10, pady=5)
feature_dir_entry = tk.Entry(root, width=50)
feature_dir_entry.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="Kernel Size:").grid(row=8, column=0, padx=10, pady=5)
kernel_size_entry = tk.Entry(root, width=50)
kernel_size_entry.grid(row=8, column=1, padx=10, pady=5)

tk.Label(root, text="Erode Iterations:").grid(row=9, column=0, padx=10, pady=5)
erode_iterations_entry = tk.Entry(root, width=50)
erode_iterations_entry.grid(row=9, column=1, padx=10, pady=5)

tk.Label(root, text="Dilate Iterations:").grid(row=10, column=0, padx=10, pady=5)
dilate_iterations_entry = tk.Entry(root, width=50)
dilate_iterations_entry.grid(row=10, column=1, padx=10, pady=5)

tk.Label(root, text="Feature Extractor:").grid(row=11, column=0, padx=10, pady=5)
feature_extractor_var = tk.StringVar()
feature_extractor_options = ["sift", "surf", "brisk", "orb"]
feature_extractor_var.set(feature_extractor_options[0])
tk.OptionMenu(root, feature_extractor_var, *feature_extractor_options).grid(
    row=11, column=1, padx=10, pady=5
)

tk.Label(root, text="Feature Matching:").grid(row=12, column=0, padx=10, pady=5)
feature_matching_var = tk.StringVar()
feature_matching_options = ["bf", "knn"]
feature_matching_var.set(feature_matching_options[0])
tk.OptionMenu(root, feature_matching_var, *feature_matching_options).grid(
    row=12, column=1, padx=10, pady=5
)

tk.Label(root, text="ratio:").grid(row=13, column=0, padx=10, pady=5)
ratio_entry = tk.Entry(root, width=50)
ratio_entry.grid(row=13, column=1, padx=10, pady=5)

ratio_scale = ttk.Scale(root, from_=0, to=1, orient="horizontal", command=update_entry)
ratio_scale.grid(row=13, column=2, padx=10, pady=5)

tk.Button(root, text="Save Config", command=save_config).grid(
    row=14, column=0, padx=10, pady=20
)

tk.Button(root, text="Execute", command=execute_functions).grid(
    row=14, column=1, padx=10, pady=20
)

tk.Button(root, text="Clear Paths", command=clear_paths).grid(
    row=14, column=2, padx=10, pady=20
)

load_config()

root.mainloop()
