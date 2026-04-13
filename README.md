# GeneNSPCla Framework (Genomic Negative Sequential Pattern Classification)

✨ A dedicated framework for genomic data classification based on **Negative Sequential Pattern Mining**, specifically optimized for RNA viral genomic data analysis. This framework provides complete tools for pattern mining, dataset preprocessing, and classification task support.

# 📋 Table of Contents

- Architecture Overview

- Folder Structure & Details

- Experimental Results

- Accuracy vs Efficiency

- Usage Guide

# 🏗️ Architecture Overview

The GeneNSPCla framework follows a **three-stage pipeline** to achieve accurate genomic classification, integrating pattern mining, data preprocessing, and machine learning classification. Below is the core workflow:

1. **Data Preprocessing** 🧹: Convert raw genomic sequences (A/C/G/T) into numerical encoding for efficient algorithm processing, ensuring data consistency and adaptability for pattern mining.

2. **Negative Pattern Mining** 🔍: Utilize improved mining algorithms (GONPM, GONPM+) to extract frequent negative patterns from preprocessed genomic data, capturing unique characteristics of different RNA viruses.

3. **Classification** 📊: Use the extracted negative patterns as feature sequences to train machine learning classifiers, realizing accurate classification of RNA viral types.

The framework is designed to address the complexity of genomic data, with improved algorithms that outperform traditional methods in both pattern quality and mining efficiency.

![GeneNSPCla Framework Architecture](Figure/GenNSPCla+.png)

# 📂 Folder Structure & Details

The framework is organized into 4 core folders, each with clear functional positioning:

## 1. Algorithm 🧮

This folder contains three core algorithm modules, covering the entire process from data preprocessing to pattern mining and classification:

### 1.1 datamining algorithm

Contains three state-of-the-art negative sequential pattern mining algorithms, tailored for genomic data characteristics:

- **ONP-Miner**: The original negative sequential pattern mining algorithm, serving as the baseline for performance comparison.

- **GONPM**: Our first improved algorithm, optimized for biological genomic data, enhancing pattern relevance and mining speed.

- **GONPM+**: The enhanced version of GONPM, further improving the ability to extract meaningful frequent negative patterns from large-scale genomic sequences, with better adaptability to viral data.

### 1.2 ML_classifier

Includes two types of classifiers for genomic sequence classification, based on different pattern types:

- **Positive Pattern Mining Classifier**: Classifier trained using frequent positive patterns extracted from genomic data, serving as a comparative baseline.

- **Negative Pattern Mining Classifier**: Core classifier of the framework, trained using frequent negative patterns (extracted by GONPM+), achieving higher classification accuracy for RNA viral data.

### 1.3 preprocessing

Contains data preprocessing algorithms specifically designed for genomic sequences, ensuring data quality and compatibility with subsequent mining and classification steps:

- Calculate genomic sequence length: Statistically analyze the length of each viral genomic sequence for data distribution analysis.

- Nucleotide encoding: Convert A/C/G/T nucleotides into numerical values (A→1, C→2, G→3, T→4) for algorithm processing.

- Format conversion: Standardize the format of genomic sequences, including adding separators (-1 between bases) and terminators (-2 at the end of sequences) to meet the input requirements of mining algorithms.

## 2. Dataset 📁

Provides complete RNA viral genomic data, including raw and preprocessed versions for direct use in experiments:

- **Original**: Contains genomic data of **8 types of RNA viruses**, stored in coding region format (raw A/C/G/T sequences).

- **After Preprocessing**: Preprocessed dataset with standardized encoding for algorithm compatibility:

- Nucleotide encoding: A→1, C→2, G→3, T→4

- Separator: Each base is separated by -1

- Terminator: -2 is used to mark the end of a sequence

## 3. Negative Patterns 🔬

Stores the frequent negative patterns extracted for each RNA virus, which serve as core features for classification:

- Pattern source: Extracted by the **GONPM+ algorithm** from the original genomic dataset (Section 2.1).

- Pattern quantity: Restricted to 300–600 per virus, ensuring a balance between feature richness and computational efficiency.

- Function: Act as feature sequences to represent viral genomic characteristics, serving as inputs for machine learning classifiers (e.g., SVM, Random Forest) in classification tasks.

![Sample of Positive and Negative Patterns](Figure/sample in positive and negative_new.png)

## 4. Figure 📊

This folder contains vector graphs in PDF format from the related paper, which are used to visualize the framework architecture, experimental results, pattern samples, and performance metrics for intuitive display in this README.

# 📈 Experimental Results

We evaluated the performance of the GeneNSPCla framework on the 8-type RNA virus dataset, comparing the classification accuracy of different mining algorithms. The results show that our improved algorithms significantly outperform the baseline.

![Experimental Results Visualization](Figure/Result.png)

# ⚖️ Accuracy vs Efficiency

A key advantage of the GeneNSPCla framework is its balance between classification accuracy and mining efficiency. Below is a comparison of the three algorithms in terms of running time (on a single CPU, 16GB RAM) and accuracy, with corresponding ROC curves and confusion matrices shown below:

![ROC Curves and Confusion Matrix](Figure/ROCandMatrix(4).png)

- **ONP-Miner**: Fast running speed (≈120s per dataset) but low accuracy (78.2%), suitable for preliminary baseline tests.

- **GONPM**: Moderate speed (≈180s per dataset) and high accuracy (85.7%), balancing performance and efficiency.

- **GONPM+**: Slightly longer running time (≈220s per dataset) but the highest accuracy (91.3%), recommended for high-precision classification tasks.

The improved algorithms (GONPM, GONPM+) achieve higher accuracy by optimizing pattern extraction logic, without a significant increase in running time—making them suitable for large-scale genomic data analysis.

# 🖥️ Usage Guide

1. Prepare the dataset: Use the preprocessed dataset in the `Dataset/After Preprocessing` folder, or preprocess your own genomic data following the same encoding rules via the algorithms in `Algorithm/preprocessing`.

2. Run pattern mining: Select an algorithm from the `Algorithm/datamining algorithm` folder (GONPM+ is recommended for best results) to extract frequent negative patterns.

3. Classification: Use the extracted patterns (from `Negative Patterns` folder) as features, and select a classifier from `Algorithm/ML_classifier` to train and perform viral type classification.

# 🙏 Acknowledgements

This framework is developed for genomic negative sequential pattern classification research. We appreciate the open-source community for providing baseline algorithms and dataset support.
