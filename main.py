# Installs and Downloads ------------------------------------------------------
import pandas as pd
from class_document import Document
from class_model import Model_SVM, Model_NB, Model_MLP, Model_Tree
import pickle
import os
from sklearn.model_selection import train_test_split

# Get Data --------------------------------------------------------------------
#all_docs = []

#with open("data_labels_2.csv", "rb") as file:
##with open("data_labels_2.csv", "rb") as file:
#    labels = pd.read_csv(file)
#    for i, row in labels.iterrows():
#        print(i)
#        try:
#            all_docs.append(Document(row["Book"], "Files/"+row["file"], row["Protagonist"], row["Antagonist"]))
##            with open("Dataset/%s.pickle"%(row["Book"]), "wb") as file:
#            with open("Dataset/%s.pickle"%(row["Book"]), "wb") as file:
#                pickle.dump(all_docs[-1], file)
#        except Exception as e:
#            print("Error: No file found "+row["file"]+".")
#            print(e)
#            print()
#        print("File %d Complete"%(i))

#for file in os.listdir("Dataset"):
#    filename = os.fsdecode(file)
#    if filename.endswith(".pickle"):
#        print(filename)
##        print(str(os.path.getsize("Dataset/" + filename)))
#        try:
#            with open("Dataset/" + filename,"rb") as picklefile:
#                doc = pickle.load(picklefile)
#                all_docs.append(doc)
#        except Exception as e:
#            print(e)

train_data = []
test_data = []
for i, doc in enumerate(all_docs):
    if i < int(len(all_docs)*0.8)+1:
        train_data.append(doc)
    else:
        test_data.append(doc)

# Train Models ---------------------------------------------------------------
params_svm = {
            "probability": True,
            "kernel": "rbf",
            "class_weight": "balanced",
            "gamma": "auto",
            "verbose": True
            }
model_svm = Model_SVM(train_data)
model_svm.train_model(params_svm)
with open("Models/svm.pickle", "wb") as file:
    pickle.dump(model_svm, file)
#    
#params_nb = {
#            }
#model_nb = Model_NB(train_data)
#model_nb.train_model(params_nb)
#with open("Models/nb.pickle", "wb") as file:
#    pickle.dump(model_nb, file)
#    
#params_mlp = {
#            }
#model_mlp = Model_MLP(train_data)
#model_mlp.train_model(params_mlp)
#with open("Models/mlp.pickle", "wb") as file:
#    pickle.dump(model_mlp, file)
#    
#params_tree = {
#            }
#model_tree = Model_Tree(train_data)
#model_tree.train_model(params_tree)
#with open("Models/tree.pickle", "wb") as file:
#    pickle.dump(model_tree, file)
    
print("SVM:")
results_svm = model_svm.test(test_data)

predict_svm = model_svm.predict(test_data)
#print()
#print("NB:")
#print(model_nb.test(test_data))
#print()
#print("MLP:")
#print(model_mlp.test(test_data))
#print()
#print("Tree:")
#print(model_tree.test(test_data))
print()