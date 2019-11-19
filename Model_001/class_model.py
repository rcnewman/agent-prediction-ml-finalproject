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
    
    def train_model(self, parameters):
        clf = SVC(**parameters)
        clf.fit(self.training_data, self.training_labels)
        self.model = clf
    
    def predict(self, doc):
        best = None
        for row in doc:
            p = self.model.predict([row[1:3]])
            if best is None:
                best = [row[0], p]
            elif best[1] < p:
                best = [row[0], p]
        return best[0]
    
    def cross_validate(self):
        pass
    
    def test(self, test_data, char_type):
        acc = 0.0
        preds = []
        for doc in test_data:
            p = []
            test_doc = []
            test_char = None
            if char_type == "p":
                test_char = doc.protagonist_g
            else:
                test_char = doc.antagonist_g
            p.append([self.predict(doc.get_features()), test_char])
            if self.predict(doc.get_features()) in test_char or test_char in self.predict(doc.get_features()):
                acc += 1
            preds.append(p)
        print(preds)
        acc /= len(test_data)
        return acc
    
    
# probability = True,
#                  kernel = "linear"