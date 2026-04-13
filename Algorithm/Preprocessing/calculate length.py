# -*- coding: utf-8 -*-
"""
统计基因组序列长度信息
A=1, C=2, G=3, T=4
序列元素用 -1 分隔，末尾用 -2 表示结束
"""

def decode_sequence(num_seq):
    """将数字序列转换为碱基序列"""
    mapping = {1: 'A', 2: 'C', 3: 'G', 4: 'T'}
    return ''.join(mapping[n] for n in num_seq if n in mapping)


def parse_sequence(line):
    """解析一行序列，返回去掉-1、-2后的数字序列"""
    nums = [int(x) for x in line.strip().split()]
    seq = [n for n in nums if n > 0 and n <= 4]  # 只保留1-4之间的数字
    return seq


def main():
    # ✅ 在这里修改你的文件路径
    file_path = r"E:\Coding Region Form(worked)\EbolaCR(200).txt"

    sequences = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():  # 跳过空行
                seq = parse_sequence(line)
                if seq:
                    sequences.append(seq)

    if not sequences:
        print("未读取到任何有效序列，请检查文件格式。")
        return

    # 统计长度
    lengths = [len(seq) for seq in sequences]
    min_len = min(lengths)
    max_len = max(lengths)
    avg_len = sum(lengths) / len(lengths)

    # 找到所有最短序列
    shortest_seqs = [seq for seq in sequences if len(seq) == min_len]

    # 输出结果
    print(f"序列总数: {len(sequences)}")
    print(f"最小长度: {min_len}")
    print(f"最大长度: {max_len}")
    print(f"平均长度: {avg_len:.2f}")
    print("最短序列（A/C/G/T形式）:")

    for i, seq in enumerate(shortest_seqs, 1):
        print(f"{i}. {decode_sequence(seq)}")


if __name__ == "__main__":
    main()
