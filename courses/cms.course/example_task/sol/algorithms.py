#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier

#-----------------------------------------------------#
#                 Logistic Regression                 #
#-----------------------------------------------------#
class Logistic_Regression:
    def __init__(self):
        self.model = LogisticRegression(random_state=0, solver="lbfgs",
                                        multi_class="ovr")

    def train(self, train_x, train_y):
        self.model.fit(train_x, train_y)

    def predict(self, data):
        return self.model.predict(data)

#-----------------------------------------------------#
#                     Naive Bayes                     #
#-----------------------------------------------------#
class Naive_Bayes:
    def __init__(self):
        self.model = MultinomialNB()

    def train(self, train_x, train_y):
        self.model.fit(train_x, train_y)

    def predict(self, data):
        return self.model.predict(data)

#-----------------------------------------------------#
#                 k-Nearest Neighbors                 #
#-----------------------------------------------------#
class k_Nearest_Neighbors:
    def __init__(self, k=5):
        self.model = KNeighborsClassifier(n_neighbors=k)

    def train(self, train_x, train_y):
        self.model.fit(train_x, train_y)

    def predict(self, data):
        return self.model.predict(data)

#-----------------------------------------------------#
#               Support Vector Machine                #
#-----------------------------------------------------#
class Support_Vector_Machine:
    def __init__(self):
        self.model = svm.SVC(gamma="scale")

    def train(self, train_x, train_y):
        self.model.fit(train_x, train_y)

    def predict(self, data):
        return self.model.predict(data)

#-----------------------------------------------------#
#                    Random Forest                    #
#-----------------------------------------------------#
class Random_Forest:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)

    def train(self, train_x, train_y):
        self.model.fit(train_x, train_y)

    def predict(self, data):
        return self.model.predict(data)
