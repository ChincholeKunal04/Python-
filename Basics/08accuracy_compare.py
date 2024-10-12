from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris

data = load_iris()
X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

nb_classifier = GaussianNB()
knn_classifier = KNeighborsClassifier(n_neighbors=3)

nb_classifier.fit(X_train, y_train)
knn_classifier.fit(X_train, y_train)

nb_accuracy = cross_val_score(nb_classifier, X, y, cv=5).mean() * 100
knn_accuracy = cross_val_score(knn_classifier, X, y, cv=5).mean() * 100

if nb_accuracy > knn_accuracy:
    comparison_result = "The Bayesian classifier is more accurate."
elif knn_accuracy > nb_accuracy:
    comparison_result = "The KNN classifier is more accurate."
else:
    comparison_result = "Both classifiers have the same accuracy."

print("Results Summary:")
print(f"Bayesian Classifier Accuracy: {nb_accuracy:.2f}%")
print(f"KNN Classifier Accuracy: {knn_accuracy:.2f}%")
print(comparison_result)
