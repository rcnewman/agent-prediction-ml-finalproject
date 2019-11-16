# Installs and Downloads ------------------------------------------------------
import pandas as pd
from class_document import Document
from class_model import Model
import pickle

# Get Data --------------------------------------------------------------------
all_docs = []
with open("../data_labels.csv", "rb") as file:
    labels = pd.read_csv(file)
    for i, row in labels.iterrows():
        try:
            all_docs.append(Document(row["Book"], "../Files/"+row["file"], row["Protagonist"], row["Antagonist"]))
#            with open("../Dataset/%s.pickle"%(row["Book"]), "wb") as file:
#                pickle.dump(all_docs[-1], file)
        except Exception as e:
            print("Error: No file found "+row["file"]+".")
            print(e)
            print()
        if len(all_docs) > 1:
            break

# Train Models ----------------------------------------------------------------
params = {
            "probability": True,
            "kernel": "linear"
            }
print("models")
p_model = Model(all_docs, "p")
print("built model")
p_model.train_model(params)
print("Trained p model")
a_model = Model(all_docs, "a")
a_model.train_model(params)
print("Trained pa model")

# Get Test Accuracy -----------------------------------------------------------
            