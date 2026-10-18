from sklearn.naive_bayes import GaussianNB


def create_naive_bayes(var_smoothing=1e-9):
    """Create configured Gaussian Naive Bayes classifier."""
    return GaussianNB(var_smoothing=var_smoothing)
