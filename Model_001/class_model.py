# Imports ---------------------------------------------------------------------
from sklearn.svm import SVC

# Model Class -----------------------------------------------------------------
class Model():
    # Class variables.
    training_data = None
    training_labels = None
    model_name = None
    model = None
    
    def __init__(self, data, model_name):
        # Initilzie class variables.
        self.training_data = []
        self.training_labels = []
        label_idx = 0
        if model_name == "p":
            label_idx = 0
        if model_name == "a":
            label_idx = 1
        for doc in data:
            for row in doc.get_features():
                self.training_data.append(row[1:3])
            self.training_labels.extend(doc.get_gold_labels())
        print(self.training_data)
    
    def train_model(self, parameters):
        clf = SVC(**parameters)
        clf.fit(self.training_data, self.training_labels)
        self.model = clf
    
    def predict(self, doc):
        return self.model.predict(doc)
    
    def cross_validate(self):
        pass
    
#    def test(self, doc):
#        p = self.model.predict(doc.get_
#        if p in label or label in p:
#            return True
#        return False
    
    
    
# probability = True,
#                  kernel = "linear"