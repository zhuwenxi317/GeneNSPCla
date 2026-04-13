def encode_sequence(seq):
    """将DNA序列按照规则编码"""
    encoded = []
    i = 0
    while i < len(seq):
        char = seq[i]
        if char == '-':
            if i + 1 >= len(seq):
                encoded.append('-1')
                break
            next_char = seq[i + 1]
            if next_char == 'A':
                encoded.append('f1')
            elif next_char == 'C':
                encoded.append('f2')
            elif next_char == 'G':
                encoded.append('f3')
            elif next_char == 'T':
                encoded.append('f4')
            else:
                encoded.append('-1')
            i += 2
        else:
            if char == 'A':
                encoded.append('1')
            elif char == 'C':
                encoded.append('2')
            elif char == 'G':
                encoded.append('3')
            elif char == 'T':
                encoded.append('4')
            elif char == ' ':
                encoded.append(' ')
            else:
                encoded.append('-1')
            i += 1

    result = []
    for i, item in enumerate(encoded):
        if not result and item == ' ':
            continue
        result.append(item)
        if item != ' ' and i < len(encoded) - 1:
            result.append('-1')
    result.append('-2')
    return ' '.join(result)


def encode_file(input_path, output_path):
    try:
        with open(input_path, 'r') as infile:
            lines = infile.read().splitlines()

        encoded_lines = [encode_sequence(line) for line in lines]

        # 打印编码结果
        print("\n编码结果:")
        for encoded in encoded_lines:
            print(encoded)

        # 写入文件
        with open(output_path, 'w') as outfile:
            outfile.write('\n'.join(encoded_lines) + '\n')

        print(f"\n编码完成，结果已保存到: {output_path}")
    except Exception as e:
        print(f"处理文件时出错: {e}")


# 直接在代码中修改文件路径 ↓↓↓
INPUT_FILE = r'E:\Coding Region Form(worked)\DabieCR(inverse200)GONPM2,0,3,30000(0.88,0.83,0.73,0.63).txt'  # 输入文件路径
OUTPUT_FILE = r'E:\Coding Region Form(worked)\DabieCR(inverse200)GONPM2,0,3,30000(0.88,0.83,0.73,0.63)(sameform).txt'  # 输出文件路径

if __name__ == "__main__":
    encode_file(INPUT_FILE, OUTPUT_FILE)