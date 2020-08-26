import pandas as pd
import shutil

src = "train/images/"
desct = "test/images/"
test = pd.read_csv("test_vc2kHdQ.csv")
final_list = test["image_names"]
# print(final_list)
for file in final_list:
    shutil.move(src + file, desct)
