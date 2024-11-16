import pandas as pd
import regions

files_location = "Datasets/Main_Dashboard/Unmodified/DDC/deaths/"
dataset_file_name_1 = "death-round-1to2-line-list"
dataset_file_name_2 = "death-round-3-lists"
dataset_file_name_3 = "death-round-4-lists"
extension = ".csv"

dataset1 = pd.read_csv(files_location + dataset_file_name_1 + extension)
dataset2 = pd.read_csv(files_location + dataset_file_name_2 + extension)
dataset3 = pd.read_csv(files_location + dataset_file_name_3 + extension)

merge_dataset = pd.DataFrame()

merge_dataset = pd.concat([dataset1, dataset2], ignore_index=True)
merge_dataset = pd.concat([merge_dataset, dataset3], ignore_index=True)

merge_dataset.to_csv("Datasets/Main_Dashboard/Modified/deaths/deaths_merged.csv")

merge_dataset.melt()
