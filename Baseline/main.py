# Installs and Downloads ------------------------------------------------------
import pandas as pd
from class_document import Document
import os
all_docs = []
accs = []
print(os.getcwd())
with open("../data_labels.csv", "rb") as file:
    labels = pd.read_csv(file)
    for i, row in labels.iterrows():
        try:
            all_docs.append(Document(row["Book"], "../Files/"+row["file"], row["Protagonist"], row["Antagonist"]))
            x = [all_docs[-1].title]
            x.extend(all_docs[-1].preds())
            accs.append(x)
        except Exception as e:
            print("Error: No file found "+row["file"]+".")
            print(e)
            print()

pa = 0
aa = 0
for row in accs:
    if row[1]:
        pa += 1
    if row[2]:
        aa += 1
pa = pa/len(accs)
aa = aa/len(accs)
print("protagonist accuracy: "+str(pa))
print("antagonist accuracy: "+str(aa))
with open("../Results/baseline.txt", "w") as file:
#    file.writelines(accs)
    for row in accs:
        file.write("%s, %s, %s\n"%(row[0], row[1], row[2]))
    file.write("protagonist accuracy: %s\n"%(str(pa)))
    file.write("antagonist accuracy: %s\n"%(str(aa)))