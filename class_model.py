# Imports ---------------------------------------------------------------------
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn import tree, metrics
from sklearn.model_selection import GridSearchCV

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
        self.grid_results = [];

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
        svm_log_range = [10**x for x in range(-2, 2+1)]
        grid_params = {'gamma': svm_log_range, 'C': svm_log_range}
        self.sv_grid = GridSearchCV(clf, grid_params,cv=3, verbose=3, n_jobs=4)
        print("Training SVM...2")
        self.sv_grid.fit(self.training_data, self.training_labels)
#        clf.fit(self.training_data, self.training_labels)
        
        self.grid_results = {"best_score": self.sv_grid.best_score_,
                                 "best_params": self.sv_grid.best_params_,
                                 "best_estimator": self.sv_grid.best_estimator_,
                                 "final_test_accuracy": 0}
        self.model = self.sv_grid.best_estimator_
    
    def predict(self, doc):
        best_p = [None, 0]
        best_a = [None, 0]
        a = []
        test_data = []
        test_labels = []
        for row in doc:
            for b in row.get_features():
                test_data.append(b[1:])
            test_labels.extend(row.get_gold_labels())
            
#            p = self.model.predict_proba([row[1:]])[0]
#            if best_p[1] < p[2]:
#                best_p = [row[0], p[2]]
#            if best_a[1] < p[0]:
#                best_a = [row[0], p[0]]
#                
#            a.append([p,row[0]])
        y_pred = self.model.predict(test_data)
        print("SVM Confusion Matrix")
        print(metrics.confusion_matrix(y_true=test_labels, y_pred=y_pred))
        print()
        print("SVM Classification Report")
        print(metrics.classification_report(test_labels, y_pred))
#        sorted_list_a = sorted(a,key= lambda x: x[0][0])
#        sorted_list_p = sorted(a,key=lambda x: x[0][2])
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
        self.grid_results = []
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
        grid_params = {'alpha': 10.0 ** -np.arange(1, 10), 'hidden_layer_sizes':np.arange(10, 15)}
        mlp_grid = GridSearchCV(clf, grid_params,cv=3)
        print("Training MLP...")
        mlp_grid.fit(self.training_data, self.training_labels)
#        clf.fit(self.training_data, self.training_labels)
        
        self.grid_results = {"best_score": mlp_grid.best_score_,
                                 "best_params": mlp_grid.best_params_,
                                 "best_estimator": mlp_grid.best_estimator_,
                                 "final_test_accuracy": 0}
        self.model = mlp_grid.best_estimator_
    
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