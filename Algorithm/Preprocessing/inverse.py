import re


def decode_line(line):
    mapping = {
        '1': 'A', '2': 'C', '3': 'G', '4': 'T',
        '-2': '\n'  # 遇到-2时输出换行
    }

    # 严格按" -1 "分割，处理连续分隔符
    parts = re.split(r'( -1 )', line.strip())

    decoded = []
    current_part = ""

    for part in parts:
        if part == " -1 ":
            if current_part:
                if current_part in mapping:
                    decoded.append(mapping[current_part])
                else:
                    print(f"错误：遇到未知编码 '{current_part}'，跳过该部分")
                current_part = ""
        else:
            current_part += part

    # 处理最后一个部分
    if current_part:
        if current_part in mapping:
            decoded.append(mapping[current_part])
        else:
            print(f"错误：遇到未知编码 '{current_part}'，跳过该部分")

    return ''.join(decoded)


def main():
    input_filename = r'E:\Coding Region Form(worked)\RhinoCR(200).txt'  # 输入文件名（编码后的文件）
    output_filename = r'E:\Coding Region Form(worked)\RhinoCR(inverse200).txt'

    try:
        with open(input_filename, 'r') as f:
            # 按行读取，保留原始换行符
            lines = f.readlines()

        decoded_lines = []
        for line in lines:
            decoded = decode_line(line)
            decoded_lines.append(decoded)

        # 将解码后的行用原始换行符连接
        decoded_sequence = ''.join(decoded_lines)

        print("解码结果：")
        print(decoded_sequence)

        with open(output_filename, 'w') as f:
            f.write(decoded_sequence)

        print(f"\n结果已保存到 {output_filename}")

    except FileNotFoundError:
        print(f"错误：未找到输入文件 {input_filename}")
    except Exception as e:
        print(f"处理过程中发生错误：{str(e)}")


if __name__ == "__main__":
    main()