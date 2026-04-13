import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
from typing import List, Dict, Tuple, Union
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc
from sklearn.preprocessing import label_binarize


class ViralSequenceClassifier:
    def __init__(self, classifiers: List[str] = ['svm', 'rf', 'lr', 'dt', 'knn', 'nb', 'mlp', 'gbm']):
        """
        初始化分类器

        Args:
            classifiers: 要使用的分类器列表
        """
        self.classifiers = classifiers
        self.models = {}
        self.vectorizer = CountVectorizer(token_pattern=r'\b\w+\b')
        self.label_encoder = LabelEncoder()
        self.vectorizer_fit = False

    def load_sequence_data(self, virus_data: Dict[str, List[str]]) -> pd.DataFrame:
        """加载并处理病毒序列数据"""
        sequences, labels = [], []
        for virus, seq_list in virus_data.items():
            sequences.extend(seq_list)
            labels.extend([virus] * len(seq_list))

        return pd.DataFrame({'sequence': sequences, 'label': labels})

    def preprocess_sequences(self, sequences: List[str]) -> np.ndarray:
        """将带有 -1 分隔符的序列转换为特征向量"""
        processed_sequences = []
        for seq in sequences:
            elements = [e.strip() for e in seq.split('-1') if e.strip()]
            processed_sequences.append(' '.join(elements))

        if not self.vectorizer_fit:
            X = self.vectorizer.fit_transform(processed_sequences)
            self.vectorizer_fit = True
        else:
            X = self.vectorizer.transform(processed_sequences)
        return X

    def train(self, data: pd.DataFrame, test_size: float = 0.2, random_state: int = 42) -> Dict[str, Dict[str, float]]:
        """训练并评估多个分类器"""
        from sklearn.metrics import average_precision_score

        # 准备特征和标签
        X = self.preprocess_sequences(data['sequence'].tolist())
        y = self.label_encoder.fit_transform(data['label'])
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        results = {}
        for clf_name in tqdm(self.classifiers, desc="Training classifiers"):
            if clf_name == 'svm':
                clf = SVC(probability=True, kernel='rbf', C=1.0, gamma='scale', random_state=random_state)
            elif clf_name == 'rf':
                clf = RandomForestClassifier(
                    n_estimators=200, max_depth=None, criterion='gini',
                    min_samples_split=2, min_samples_leaf=1, n_jobs=-1, random_state=random_state
                )
            elif clf_name == 'lr':
                clf = LogisticRegression(
                    solver='lbfgs', C=1.0, max_iter=1000, random_state=random_state
                )
            elif clf_name == 'dt':
                clf = DecisionTreeClassifier(
                    criterion='gini', max_depth=None, min_samples_split=2,
                    min_samples_leaf=1, random_state=random_state
                )
            elif clf_name == 'knn':
                clf = KNeighborsClassifier(
                    n_neighbors=5, weights='distance', metric='minkowski', p=2
                )
            elif clf_name == 'nb':
                clf = GaussianNB()
                # ✅ GaussianNB 需要 dense 输入
                X_train_dense = X_train.toarray()
                X_test_dense = X_test.toarray()
            elif clf_name == 'mlp':
                clf = MLPClassifier(
                    hidden_layer_sizes=(100,), activation='relu', solver='adam',
                    learning_rate_init=0.001, max_iter=300, random_state=random_state
                )
            elif clf_name == 'gbm':
                clf = GradientBoostingClassifier(
                    n_estimators=100, learning_rate=0.1, max_depth=3, random_state=random_state
                )
            else:
                raise ValueError(f"不支持的分类器: {clf_name}")

            # === 拟合模型 ===
            if clf_name == 'nb':
                clf.fit(X_train_dense, y_train)
                y_pred = clf.predict(X_test_dense)
                y_prob = clf.predict_proba(X_test_dense)
            else:
                clf.fit(X_train, y_train)
                y_pred = clf.predict(X_test)
                y_prob = clf.predict_proba(X_test) if hasattr(clf, 'predict_proba') else None

            self.models[clf_name] = clf

            # === 指标计算 ===
            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
                'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
                'f1': f1_score(y_test, y_pred, average='weighted', zero_division=0),
            }

            if y_prob is not None:
                metrics['auc'] = roc_auc_score(y_test, y_prob, multi_class='ovr', average='weighted')
                y_test_bin = label_binarize(y_test, classes=range(len(self.label_encoder.classes_)))
                metrics['auprc'] = average_precision_score(y_test_bin, y_prob, average='weighted')
            else:
                metrics['auc'] = None
                metrics['auprc'] = None

            results[clf_name] = metrics

        return results

    def predict(self, sequences: List[str], clf_name: str = 'svm') -> List[Dict[str, Union[str, float]]]:
        """对新序列进行预测"""
        if clf_name not in self.models:
            raise ValueError(f"未训练的分类器: {clf_name}")

        X = self.preprocess_sequences(sequences)
        clf = self.models[clf_name]
        y_pred = clf.predict(X)
        y_prob = clf.predict_proba(X)
        class_names = self.label_encoder.inverse_transform(range(len(self.label_encoder.classes_)))

        predictions = []
        for i, pred in enumerate(y_pred):
            predictions.append({
                'sequence': sequences[i],
                'predicted_class': class_names[pred],
                'confidence': y_prob[i][pred]
            })
        return predictions

    def save_model(self, path: str = 'viral_classifier.pkl'):
        joblib.dump({'models': self.models, 'vectorizer': self.vectorizer, 'label_encoder': self.label_encoder}, path)

    @classmethod
    def load_model(cls, path: str = 'viral_classifier.pkl'):
        model_data = joblib.load(path)
        classifier = cls()
        classifier.models = model_data['models']
        classifier.vectorizer = model_data['vectorizer']
        classifier.label_encoder = model_data['label_encoder']
        return classifier


if __name__ == "__main__":
    def read_sequences_from_file(file_path):
        with open(file_path, 'r') as file:
            return file.read().splitlines()

    file1_path = r'E:\Coding Region Form(worked)\DabieCR(inverse200)GONPM2,0,3,30000(0.9,0.85,0.75,0.65)(sameform)(cut10).txt'
    file2_path = r'E:\Coding Region Form(worked)\DengueCR(inverse200)GONPM2,0,3,85000(0.9,0.85,0.75,0.65)(sameform)(cut10).txt'
    file3_path = r'E:\Coding Region Form(worked)\HantaCR(inverse200)GONPM2,0,3,40000(0.9,0.85,0.75,0.65)(sameform)(cut10).txt'
    file4_path = r'E:\Coding Region Form(worked)\EbolaCR(inverse200)GONPM2,0,3,130000(0.9,0.85,0.75,0.65)(sameform)(cut10).txt'
    file5_path = r'E:\Coding Region Form(worked)\HepaciCR(inverse200)GONPM2,0,3,65000(0.9,0.85,0.75,0.65)(sameform)(cut10).txt'
    file6_path = r'E:\Coding Region Form(worked)\HIVCR(inverse100)GONPM2,0,3,46000(0.9,0.85,0.75,0.65)(sameform)(cut10).txt'
    file7_path = r'E:\Coding Region Form(worked)\MERSCR(inverse50)GONPM2,0,3,95000(0.9,0.85,0.75,0.65)(sameform)(cut10).txt'
    file8_path = r'E:\Coding Region Form(worked)\RotaCR(inverse200)GONPM2,0,3,17500(0.9,0.85,0.75,0.65)(sameform)(cut10).txt'
    #file7_path = r'E:\Coding Region Form(worked)\InfluenzaCR(inverse200)GONP,0,3,16000,(3,1.3)(sameform)(cut8).txt'
    #file8_path = r'E:\Coding Region Form(worked)\MeaslesCR(inverse200)GONP,0,3,135000,(3,1.3)(sameform)(cut8).txt'
    # file9_path = r'E:\Coding Region Form(worked)\RabiesCR(inverse200)GONP,0,3,90000,(3,1.3)(sameform)(cut8).txt'
    # file10_path = r'E:\Coding Region Form(worked)\NoroCR(inverse200)GONP,0,3,60000,(3,1.3)(sameform)(cut8).txt'
    # file11_path = r'E:\Coding Region Form(worked)\MERSCR(inverse50)GONP,0,3,90000,(3,1.3)(sameform)(cut8).txt'
    # file12_path = r'E:\Coding Region Form(worked)\EbolaCR(inverse200)ONP,0,3,140000(sameform)(cut8).txt'
    # file13_path = r'E:\Coding Region Form(worked)\EbolaCR(inverse200)ONP,0,3,140000(sameform)(cut8).txt'
    sequences_file1 = read_sequences_from_file(file1_path)
    sequences_file2 = read_sequences_from_file(file2_path)
    sequences_file3 = read_sequences_from_file(file3_path)
    sequences_file4 = read_sequences_from_file(file4_path)
    sequences_file5 = read_sequences_from_file(file5_path)
    sequences_file6 = read_sequences_from_file(file6_path)
    sequences_file7 = read_sequences_from_file(file7_path)
    sequences_file8 = read_sequences_from_file(file8_path)
    # sequences_file9 = read_sequences_from_file(file9_path)
    # sequences_file10 = read_sequences_from_file(file10_path)
    # sequences_file11 = read_sequences_from_file(file11_path)
    # sequences_file12 = read_sequences_from_file(file11_path)
    # sequences_file13 = read_sequences_from_file(file12_path)
    # 假设将file1的序列作为目标病毒（例如Dabie）的序列，file2的序列作为其他病毒的序列
    viral_sequences = {
        "DabieCR": sequences_file1,
        "DengueCR": sequences_file2,
        'HantaCR': sequences_file3,
        'EbolaCR': sequences_file4,
        'HepaciCR': sequences_file5,
        'HIVCR': sequences_file6,
        'MERSCR': sequences_file7,
        'RotaCR': sequences_file8,
        # 'RabiesCR': sequences_file9,
        # 'NoroCR': sequences_file10,
        # 'MERSCR': sequences_file11,
        # 'InfluenzaCR': sequences_file11,
        # 'MERSCR': sequences_file12
    }
    classifier = ViralSequenceClassifier()
    data2 = classifier.load_sequence_data(viral_sequences)
    results = classifier.train(data2)

    # === 打印所有分类器结果 ===
    print("\n模型评估结果：")
    for clf_name, metrics in results.items():
        print(f"\n{clf_name.upper()} 分类器:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value:.4f}" if value is not None else f"  {metric}: None")

    classifier.save_model("multi_viral_classifier.pkl")
    loaded_classifier = ViralSequenceClassifier.load_model("multi_viral_classifier.pkl")
    print("\n✅ 模型已保存并重新加载成功。")

    # === 可视化部分（仅 SVM） ===
    plt.rcParams["font.family"] = ["SimSun", "Microsoft YaHei", "SimHei"]
    plt.rcParams["axes.unicode_minus"] = False

    clf_name = 'rf'
    clf = classifier.models[clf_name]
    X_all = classifier.preprocess_sequences(data2['sequence'].tolist())
    y_true = classifier.label_encoder.transform(data2['label'])
    y_pred = clf.predict(X_all)
    y_score = clf.predict_proba(X_all)

    # 混淆矩阵
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classifier.label_encoder.classes_)
    plt.figure(figsize=(8, 6))
    disp.plot(cmap='Blues', colorbar=False, xticks_rotation=45)
    plt.title('Confusion Matrix of SVM Classifier', fontsize=14)
    plt.tight_layout()
    plt.show()

    # ROC 曲线
    y_true_bin = label_binarize(y_true, classes=range(len(classifier.label_encoder.classes_)))
    plt.figure(figsize=(7, 6))
    for i, label in enumerate(classifier.label_encoder.classes_):
        fpr, tpr, _ = roc_curve(y_true_bin[:, i], y_score[:, i])
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, lw=1.5, label=f"{label} (AUC = {roc_auc:.3f})")
    plt.plot([0, 1], [0, 1], 'k--', lw=1)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Multi-class ROC Curves (SVM)', fontsize=13)
    plt.legend(fontsize=8, loc='lower right')
    plt.tight_layout()
    plt.show()
