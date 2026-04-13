import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
from typing import List, Dict, Tuple, Union
from imblearn.over_sampling import SMOTE
from tqdm import tqdm
import matplotlib.pyplot as plt
from imblearn.under_sampling import RandomUnderSampler
from sklearn.manifold import TSNE
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc
from sklearn.preprocessing import label_binarize



class ViralSequenceClassifier:


    def __init__(self, classifiers: List[str] = ['svm', 'rf']):

        self.classifiers = classifiers
        self.models = {}
        self.vectorizer = CountVectorizer(token_pattern=r'\b\w+\b')  # 用于将序列转换为特征向量
        self.label_encoder = LabelEncoder()
        self.vectorizer_fit = False

    def load_sequence_data(self, virus_data: Dict[str, List[str]]) -> pd.DataFrame:

        sequences = []
        labels = []
        for virus, seq_list in virus_data.items():
            sequences.extend(seq_list)
            labels.extend([virus] * len(seq_list))

        data = pd.DataFrame({
            'sequence': sequences,
            'label': labels
        })

        return data

    def preprocess_sequences(self, sequences: List[str]) -> np.ndarray:

        processed_sequences = []
        for seq in sequences:
            elements = []
            for e in seq.split('-1'):
                if e.strip():
                    elements.append(e.strip())
            processed_seq = ' '.join(elements)
            processed_sequences.append(processed_seq)
        if not self.vectorizer_fit:
            X = self.vectorizer.fit_transform(processed_sequences)
            self.vectorizer_fit = True
        else:
            X = self.vectorizer.transform(processed_sequences)
        return X

    def train(self, data: pd.DataFrame, test_size: float = 0.2, random_state: int = 42) -> Dict[str, Dict[str, float]]:
        X = self.preprocess_sequences(data['sequence'].tolist())
        y = self.label_encoder.fit_transform(data['label'])
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        results = {}
        for clf_name in tqdm(self.classifiers, desc="Training classifiers"):  # 此处tqdm已正确导入
            
            if clf_name == 'svm':
                clf = SVC(
                    probability=True,
                    random_state=random_state,
                    kernel='rbf', 
                    C=1,  
                    gamma='scale',  
                    degree=3
                )
            elif clf_name == 'rf':
                clf = RandomForestClassifier(
                    random_state=random_state,
                    n_estimators=100,  
                    max_depth=None,  
                    criterion='gini',  
                    min_samples_leaf=1,  
                    min_samples_split=2,  
                    n_jobs=1 
                )
            else:
                raise ValueError(f"unsupport: {clf_name}")

           
            clf.fit(X_train, y_train)
            self.models[clf_name] = clf  

           
            y_pred = clf.predict(X_test)
            y_prob = clf.predict_proba(X_test) if hasattr(clf, 'predict_proba') else None

            
            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, average='weighted'),#weighted,marco
                'recall': recall_score(y_test, y_pred, average='weighted'),
                'f1': f1_score(y_test, y_pred, average='weighted'),
                'auc': roc_auc_score(y_test, y_prob, multi_class='ovr',
                                     average='weighted') if y_prob is not None else None
            }

            results[clf_name] = metrics

        return results


    def predict(self, sequences: List[str], clf_name: str = 'svm') -> List[Dict[str, Union[str, float]]]:

        if clf_name not in self.models:
            raise ValueError(f"untrain_classifier: {clf_name}")

        X = self.preprocess_sequences(sequences)
        clf = self.models[clf_name]
        y_pred = clf.predict(X)
        y_prob = clf.predict_proba(X)

        class_names = self.label_encoder.inverse_transform(range(len(self.label_encoder.classes_)))
        predictions = []

        for i, pred in enumerate(y_pred):
            result = {
                'sequence': sequences[i],
                'predicted_class': class_names[pred],
                'confidence': y_prob[i][pred]
            }
            predictions.append(result)

        return predictions

    def save_model(self, path: str = 'viral_classifier.pkl'):
        
        joblib.dump({
            'models': self.models,
            'vectorizer': self.vectorizer,
            'label_encoder': self.label_encoder
        }, path)

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

    file1_path = r"E:\Coding Region Form(CM)\HantaCR,CM,0.4,7,10,1(sameform).txt"
    file2_path = r"E:\Coding Region Form(CM)\RhinoCR,CM,0.75,7,10,1(sameform).txt"
    file3_path = r"E:\Coding Region Form(CM)\NoroCR,CM,0.85,7,10,1(sameform).txt"
    #file4_path = r'E:\Coding Region Form(worked)\EbolaCR(inverse200)GONP,0,3,130000,(3,1.3)(sameform)(cut8).txt'
    #file5_path = r'E:\Coding Region Form(worked)\HepaciCR(inverse200)GONP,0,3,75000,(3,1.3)(sameform)(cut8).txt'
    #file6_path = r'E:\Coding Region Form(worked)\HIVCR(inverse200)GONP,0,3,85000,(3,1.3)(sameform)(cut8).txt'
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
    #sequences_file4 = read_sequences_from_file(file4_path)
    #sequences_file5 = read_sequences_from_file(file5_path)
    #sequences_file6 = read_sequences_from_file(file6_path)
    #sequences_file7 = read_sequences_from_file(file7_path)
    #sequences_file8 = read_sequences_from_file(file8_path)
    # sequences_file9 = read_sequences_from_file(file9_path)
    # sequences_file10 = read_sequences_from_file(file10_path)
    # sequences_file11 = read_sequences_from_file(file11_path)
    # sequences_file12 = read_sequences_from_file(file11_path)
    # sequences_file13 = read_sequences_from_file(file12_path)

    viral_sequences = {
        "HantaCR": sequences_file1,
        "RhinoCR": sequences_file2,
        'NoroCR': sequences_file3,
        #'EbolaCR': sequences_file4,
        #'HepaciCR': sequences_file5,
        #'HIVCR': sequences_file6,
        #'InfluenzaCR': sequences_file7,
        #'MeaslesCR': sequences_file8,
        # 'RabiesCR': sequences_file9,
        # 'NoroCR': sequences_file10,
        # 'MERSCR': sequences_file11,
        # 'InfluenzaCR': sequences_file11,
        # 'MERSCR': sequences_file12
    }
    classifier = ViralSequenceClassifier(classifiers=['svm', 'rf'])
    data2 = classifier.load_sequence_data(viral_sequences)
    results = classifier.train(data2)
    data2.to_csv(r'D:\CM-SPAM_data\Coding Region Form\data2(neigative_data2)\five.csv', index=False)

    print("Result:")
    for clf_name, metrics in results.items():
        print(f"{clf_name.upper()}classifier(ONP):")
        for metric, value in metrics.items():
            print(f"  {metric}: {value:.4f}")

    classifier.save_model("multi_viral_classifier.pkl")
    loaded_classifier = ViralSequenceClassifier.load_model("multi_viral_classifier.pkl")



    
    # t-SNE 
    #classifier.visualize_tsne(data2, sample_size=3000, random_state=42, perplexity=30.0, n_iter=1000)

    # print(len(sequences_file1)+len(sequences_file2)+len(sequences_file3)+len(sequences_file4)+len(sequences_file5)+len(sequences_file6)+len(sequences_file7)+len(sequences_file8)+len(sequences_file9)+len(sequences_file10)+len(sequences_file11)+len(sequences_file12))

    plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]

    counts = [len(seq) for seq in viral_sequences.values()]

    virus_names = list(viral_sequences.keys())


    plt.figure(figsize=(14, 7)) 
    bars = plt.bar(virus_names, counts, color='skyblue')

    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height,
                 f'{height}', ha='center', va='bottom', fontsize=10)

    
    plt.title('compare')
    plt.xlabel('type')
    plt.ylabel('number')

    
    plt.xticks(rotation=45, ha='right')  

    
    plt.tight_layout()

    
    plt.show()

    clf_name = 'svm'
    clf = classifier.models[clf_name]

    # feature and label
    X_all = classifier.preprocess_sequences(data2['sequence'].tolist())
    y_true = classifier.label_encoder.transform(data2['label'])
    y_pred = clf.predict(X_all)
    y_score = clf.predict_proba(X_all)

    # ========== comfusion matrix ==========
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                  display_labels=classifier.label_encoder.classes_)

    plt.figure(figsize=(8, 6))
    disp.plot(cmap='Blues', colorbar=False, xticks_rotation=45)
    plt.title('Confusion Matrix of SVM Classifier', fontsize=14)
    plt.tight_layout()
    plt.show()

    # ========== 2️⃣ ROC curve ==========
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
