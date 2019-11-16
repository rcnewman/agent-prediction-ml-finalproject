import pickle
for doc in all_docs:
    with open("../Dataset/baseline_%s.pickle"%(doc.title), "wb") as file:
        pickle.dump(doc, file)