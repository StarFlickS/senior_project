owid_translation = {
    "new_cases": "new_cases (ผู้ป่วยรายใหม่)",
    "new_deaths": "new_deaths (ผู้เสียชีวิตรายใหม่)",
    "new_vaccinations": "new_vaccinations (การฉีดวัคซีนใหม่)",
    "total_cases": "total_cases (ผู้ป่วยสะสมทั้งหมด)",
    "total_deaths": "total_deaths (ผู้เสียชีวิตสะสมทั้งหมด)",
    "total_vaccinations": "total_vaccinations (การฉีดวัคซีนทั้งหมด)"
}

labels = {
    "date": "ปีที่ระบาด",
    "value": "จำนวน" # X-axis label for date
}

labels["value"] = "จำนวน" + owid_translation["new_cases"].split(" ")[1].strip("()")

print(labels['value'])