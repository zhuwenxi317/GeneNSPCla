

def decode_sequence(num_seq):
    
    mapping = {1: 'A', 2: 'C', 3: 'G', 4: 'T'}
    return ''.join(mapping[n] for n in num_seq if n in mapping)


def parse_sequence(line):
    
    nums = [int(x) for x in line.strip().split()]
    seq = [n for n in nums if n > 0 and n <= 4]  # 只保留1-4之间的数字
    return seq


def main():
    
    file_path = r"E:\Coding Region Form(worked)\EbolaCR(200).txt"

    sequences = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():  
                seq = parse_sequence(line)
                if seq:
                    sequences.append(seq)

    if not sequences:
        print("unsuccessful")
        return

    
    lengths = [len(seq) for seq in sequences]
    min_len = min(lengths)
    max_len = max(lengths)
    avg_len = sum(lengths) / len(lengths)

    
    shortest_seqs = [seq for seq in sequences if len(seq) == min_len]

    
    print(f"total: {len(sequences)}")
    print(f"min: {min_len}")
    print(f"max: {max_len}")
    print(f"average: {avg_len:.2f}")
    print("min_length（A/C/G/T）:")

    for i, seq in enumerate(shortest_seqs, 1):
        print(f"{i}. {decode_sequence(seq)}")


if __name__ == "__main__":
    main()
