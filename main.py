# Installs and Downloads ------------------------------------------------------
import pandas as pd
from class_document import Document

all_docs = []
accs = []
with open("data_labels.csv", "rb") as file:
    labels = pd.read_csv(file)
    for i, row in labels.iterrows():
        try:
            all_docs.append(Document("files/"+row["file"], row["Protagonist"], row["Antagonist"]))
            accs.append(all_docs[-1].preds())
        except:
            print("Error: No file found "+row["file"]+".")
        break

pa = 0
aa = 0
for row in accs:
    if row[0]:
        pa += 1
    if row[1]:
        aa += 1
pa = pa/len(accs)
aa = aa/len(accs)
print("protagonist accuracy: "+str(pa))
print("antagonist accuracy: "+str(aa))
with open("baseline.txt", "wb") as file:
    file.writelines(accs)
    file.write("protagonist accuracy: "+str(pa))
    file.write("antagonist accuracy: "+str(aa))