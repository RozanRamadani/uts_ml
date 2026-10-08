from sklearn.tree import DecisionTreeClassifier


def create_decision_tree(random_state=42, max_depth=10):
    """Create the project's configured Decision Tree classifier."""
    return DecisionTreeClassifier(random_state=random_state, max_depth=max_depth)
