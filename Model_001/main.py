# Installs and Downloads ------------------------------------------------------
import pandas as pd
from class_document import Document
from class_model import Model
import pickle
import os
from sklearn.model_selection import train_test_split

# Get Data --------------------------------------------------------------------
all_docs = []
with open("../data_labels.csv", "rb") as file:
    labels = pd.read_csv(file)
    for i, row in labels.iterrows():
        try:
            all_docs.append(Document(row["Book"], "../Files/"+row["file"], row["Protagonist"], row["Antagonist"]))
            with open("../Dataset/%s.pickle"%(row["Book"]), "wb") as file:
                pickle.dump(all_docs[-1], file)
        except Exception as e:
            print("Error: No file found "+row["file"]+".")
            print(e)
            print()
        print(i)
train_data = None
test_data = None
for i, doc in enumerate(all_docs):
    if i < int(len(all_docs)*0.8)+1:
        train_data.append(doc)
    else:
        test_data.append(doc)

# Train Models ----------------------------------------------------------------
params = {
            "probability": True,
            "kernel": "linear"
            }
p_model = Model(train_data, "p")
p_model.train_model(params)
a_model = Model(train_data, "a")
a_model.train_model(params)
with open("model_001_p.pickle", "wb") as file:
    pickle.dump(p_model, file)
with open("model_001_a.pickle", "wb") as file:
    pickle.dump(a_model, file)
# Get Test Accuracy -----------------------------------------------------------
t_p = p_model.test(test_data)
t_a = a_model.test(test_data)

print(t_p)
print(t_a)