import pandas as pd


files_location = "datasets/mainDashboard/"
dataset_file_name_1 = "mainDashboard_Dataset_1"
dataset_file_name_2 = "mainDashboard_Dataset_2"
dataset_file_name_3 = "mainDashboard_Dataset_3"
extension = ".csv"

dataset1 = pd.read_csv(files_location + dataset_file_name_1 + extension)
dataset2 = pd.read_csv(files_location + dataset_file_name_2 + extension)
dataset3 = pd.read_csv(files_location + dataset_file_name_3 + extension)

merge_dataset = pd.DataFrame()

merge_dataset = pd.concat([dataset1, dataset2], ignore_index=True)
merge_dataset = pd.concat([merge_dataset, dataset3], ignore_index=True)

merge_dataset.to_csv("datasets/mainDashboard/report.csv")

merge_dataset.melt()