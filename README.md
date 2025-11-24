# GeneNSPCla framwork(Genomic Negative Sequential Pattern Classification)
It contains three folders: (1) Algorithm, (2) Dataset, (3) Negative Patterns.

(1) This folder contains three pattern mining algorithms: ONP-Miner, GONPM, and GONPM+. ONP-Miner is the original negative pattern algorithm, while GONPM and GONPM+ are our improved versions. These improved algorithms are more suitable for biological genomic data mining and can extract more meaningful frequent negative patterns.

(2) This folder contains two subfolders: Original and After Preprocessing. The former includes the genomic data of eight types of RNA viruses in coding region format. The latter is our preprocessed dataset, where A, C, G, and T are encoded as the numbers 1, 2, 3, and 4 respectively. Each base is separated by -1, with -2 used as the termination of a sequence.

(3) This folder contains the frequent negative patterns of each virus. These patterns are extracted by the GONPM+ mining algorithm through processing the original dataset described in (2). The number of negative patterns for each virus is restricted to 300–600. Serving as feature sequences, these patterns represent the viral sequences and act as inputs to machine learning classifiers for classification tasks.
