from collections import Counter

def read_pattern_lengths(file_path):
    lengths = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 每个模式的长度 = 出现的 -1 的次数
            length = line.count('-1')
            lengths.append(length)
    return lengths

if __name__ == "__main__":
    input_file = r"E:\Coding Region Form(worked)\DabieCR(inverse200)GONPM2,0,3,30000(0.88,0.83,0.73,0.63)(sameform).txt"  # 修改为你的输入文件名
    lengths = read_pattern_lengths(input_file)
    count = Counter(lengths)
    total = sum(count.values())

    print(f"共读取 {total} 条序列。\n")
    print("不同长度的模式统计：")
    print("-" * 40)
    print(f"{'长度':<10}{'数量':<10}{'比例(%)':<10}")
    print("-" * 40)

    for length in sorted(count.keys()):
        ratio = count[length] / total * 100
        print(f"{length:<10}{count[length]:<10}{ratio:.2f}")

    print("-" * 40)
    print(f"总序列数: {total}")
