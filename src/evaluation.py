import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

def evaluate_model(model_name, y_true, y_pred):
    print(f"\n--- Evaluasi {model_name} ---")
    cm = confusion_matrix(y_true, y_pred, labels=[False, True])
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, pos_label=True, zero_division=0)
    rec = recall_score(y_true, y_pred, pos_label=True, zero_division=0)
    f1 = f1_score(y_true, y_pred, pos_label=True, zero_division=0)
    
    print("Confusion Matrix (actual: rows, predicted: columns; [False, True]):")
    print(cm)
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall: {rec:.4f}")
    print(f"F1-score: {f1:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred))
    
    return {
        'Model': model_name,
        'Accuracy': acc,
        'Precision': prec,
        'Recall': rec,
        'F1-Score': f1,
    }

def plot_confusion_matrix(y_true, y_pred, model_name, filepath):
    cm = confusion_matrix(y_true, y_pred, labels=[False, True])
    plt.figure(figsize=(6,4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title(f'Confusion Matrix - {model_name}')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.xticks([0.5, 1.5], ['False', 'True'])
    plt.yticks([0.5, 1.5], ['False', 'True'], rotation=0)
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()
    return cm

def plot_class_distribution(y, title, filepath):
    plt.figure(figsize=(6,4))
    ax = sns.countplot(x=y)
    plt.title(title)
    
    # Add counts above bars
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', xytext = (0, 5), textcoords = 'offset points')

    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()

def plot_metrics_comparison(metrics_df, filepath):
    df_melt = metrics_df.melt(id_vars='Model', var_name='Metric', value_name='Score')
    plt.figure(figsize=(10,6))
    sns.barplot(x='Metric', y='Score', hue='Model', data=df_melt)
    plt.title('Perbandingan Metrik Evaluasi')
    plt.ylim(0, 1.0)
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()
