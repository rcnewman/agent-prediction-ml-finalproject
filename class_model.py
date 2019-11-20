# Imports ---------------------------------------------------------------------
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn import tree

# Model Class -----------------------------------------------------------------
class Model_SVM():
    # Class variables.
    training_data = None
    training_labels = None
    model_name = None
    model = None
    for_csv = []
    
    def __init__(self, data):
        # Initilzie class variables.
        self.training_data = []
        self.training_labels = []
        x = []
        y = []
        for doc in data:
            for row in doc.get_features():
                self.training_data.append(row[1:])
                x.append(row[1])
                y.append(row[2])
            self.training_labels.extend(doc.get_gold_labels())
    
    def train_model(self, parameters):
        clf = SVC(**parameters)
        clf.fit(self.training_data, self.training_labels)
        self.model = clf
    
    def predict(self, doc):
        best_p = [None, 0]
        best_a = [None, 0]
        a = []
        for row in doc:
            p = self.model.predict_proba([row[1:]])[0]
            if best_p[1] < p[2]:
                best_p = [row[0], p[2]]
            if best_a[1] < p[0]:
                best_a = [row[0], p[0]]
                
            a.append([p,row[0]])
        sorted_list_a = sorted(a,key= lambda x: x[0][0])
        sorted_list_p = sorted(a,key=lambda x: x[0][2])
        return [best_p, best_a]
    
    def test(self, test_data):
        acc = 0.0
        data = []
        labels = []
        for doc in test_data:
            for row in doc.get_features():
                data.append(row[1:])
            labels.extend(doc.get_gold_labels())
        return self.model.score(data, labels)

class Model_NB():
    # Class variables.
    training_data = None
    training_labels = None
    model_name = None
    model = None
    for_csv = []
    
    def __init__(self, data):
        # Initilzie class variables.
        self.training_data = []
        self.training_labels = []
        x = []
        y = []
        for doc in data:
            for row in doc.get_features():
                self.training_data.append(row[1:])
                x.append(row[1])
                y.append(row[2])
            self.training_labels.extend(doc.get_gold_labels())
    
    def train_model(self, parameters):
        clf = GaussianNB(**parameters)
        clf.fit(self.training_data, self.training_labels)
        self.model = clf
    
    def predict(self, doc):
        best_p = [None, 0]
        best_a = [None, 0]
        a = []
        for row in doc:
            p = self.model.predict_proba([row[1:]])[0]
            if best_p[1] < p[2]:
                best_p = [row[0], p[2]]
            if best_a[1] < p[0]:
                best_a = [row[0], p[0]]
                
            a.append([p,row[0]])
        sorted_list_a = sorted(a,key= lambda x: x[0][0])
        sorted_list_p = sorted(a,key=lambda x: x[0][2])
        return [best_p, best_a]
    
    def test(self, test_data):
        acc = 0.0
        data = []
        labels = []
        for doc in test_data:
            for row in doc.get_features():
                data.append(row[1:])
            labels.extend(doc.get_gold_labels())
        return self.model.score(data, labels)

class Model_MLP():
    # Class variables.
    training_data = None
    training_labels = None
    model_name = None
    model = None
    for_csv = []
    
    def __init__(self, data):
        # Initilzie class variables.
        self.training_data = []
        self.training_labels = []
        x = []
        y = []
        for doc in data:
            for row in doc.get_features():
                self.training_data.append(row[1:])
                x.append(row[1])
                y.append(row[2])
            self.training_labels.extend(doc.get_gold_labels())
    
    def train_model(self, parameters):
        clf = MLPClassifier(**parameters)
        clf.fit(self.training_data, self.training_labels)
        self.model = clf
    
    def predict(self, doc):
        best_p = [None, 0]
        best_a = [None, 0]
        a = []
        for row in doc:
            p = self.model.predict_proba([row[1:]])[0]
            if best_p[1] < p[2]:
                best_p = [row[0], p[2]]
            if best_a[1] < p[0]:
                best_a = [row[0], p[0]]
                
            a.append([p,row[0]])
        sorted_list_a = sorted(a,key= lambda x: x[0][0])
        sorted_list_p = sorted(a,key=lambda x: x[0][2])
        return [best_p, best_a]
    
    def test(self, test_data):
        acc = 0.0
        data = []
        labels = []
        for doc in test_data:
            for row in doc.get_features():
                data.append(row[1:])
            labels.extend(doc.get_gold_labels())
        return self.model.score(data, labels)

class Model_Tree():
    # Class variables.
    training_data = None
    training_labels = None
    model_name = None
    model = None
    for_csv = []
    
    def __init__(self, data):
        # Initilzie class variables.
        self.training_data = []
        self.training_labels = []
        x = []
        y = []
        for doc in data:
            for row in doc.get_features():
                self.training_data.append(row[1:])
                x.append(row[1])
                y.append(row[2])
            self.training_labels.extend(doc.get_gold_labels())
    
    def train_model(self, parameters):
        clf = tree.DecisionTreeClassifier(**parameters)
        clf.fit(self.training_data, self.training_labels)
        self.model = clf
    
    def predict(self, doc):
        best_p = [None, 0]
        best_a = [None, 0]
        a = []
        for row in doc:
            p = self.model.predict_proba([row[1:]])[0]
            if best_p[1] < p[2]:
                best_p = [row[0], p[2]]
            if best_a[1] < p[0]:
                best_a = [row[0], p[0]]
                
            a.append([p,row[0]])
        sorted_list_a = sorted(a,key= lambda x: x[0][0])
        sorted_list_p = sorted(a,key=lambda x: x[0][2])
        return [best_p, best_a]
    
    def test(self, test_data):
        acc = 0.0
        data = []
        labels = []
        for doc in test_data:
            for row in doc.get_features():
                data.append(row[1:])
            labels.extend(doc.get_gold_labels())
        return self.model.score(data, labels)