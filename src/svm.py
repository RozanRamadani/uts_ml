from sklearn.svm import SVC


def create_svm(kernel="rbf", c=1.0, probability=True, random_state=42):
    """Create configured Support Vector Classifier (SVM)."""
    return SVC(
        kernel=kernel,
        C=c,
        probability=probability,
        random_state=random_state,
    )
