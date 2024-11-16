import pandas as pd

files_location = "Datasets/Main_Dashboard/Unmodified/DDC/cases/"
dataset_file_name_1 = "round1-2"
dataset_file_name_2 = "round3/round3_1"
dataset_file_name_3 = "round3/round3_2"
dataset_file_name_4 = "round3/round3_3"
dataset_file_name_5 = "round4"
extension = ".csv"

dataset1 = pd.read_csv(files_location + dataset_file_name_1 + extension, dtype={'age_range': "string"}, low_memory=False)
dataset2 = pd.read_csv(files_location + dataset_file_name_2 + extension, dtype={'age_range': "string"}, low_memory=False)
dataset3 = pd.read_csv(files_location + dataset_file_name_3 + extension, dtype={'age_range': "string"}, low_memory=False)
dataset4 = pd.read_csv(files_location + dataset_file_name_4 + extension, dtype={'age_range': "string"}, low_memory=False)
dataset5 = pd.read_csv(files_location + dataset_file_name_5 + extension, dtype={'age_range': "string"}, low_memory=False)

merge_dataset = pd.DataFrame()

merge_dataset = pd.concat([dataset1, dataset2], ignore_index=True)
merge_dataset = pd.concat([merge_dataset, dataset3], ignore_index=True)
merge_dataset = pd.concat([merge_dataset, dataset4], ignore_index=True)
merge_dataset = pd.concat([merge_dataset, dataset5], ignore_index=True)


print(merge_dataset.isnull().sum())

merge_dataset['age_number'] = merge_dataset['age_number'].fillna("ไม่ระบุ")
merge_dataset['job'] = merge_dataset['job'].fillna("ไม่ระบุ")

merge_dataset = merge_dataset.dropna()

print(merge_dataset.isnull().sum())


merge_dataset.to_csv("Datasets/Main_Dashboard/Modified/DDC/cases/cases_merged.csv")

merge_dataset.melt()

df = pd.read_csv("Datasets/Main_Dashboard/Modified/DDC/cases/cases_merged.csv")

print(len(df.job.unique()))
print(len(df.risk.unique()))
print(df.patient_type.unique())