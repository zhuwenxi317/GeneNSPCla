import re


def decode_line(line):
    mapping = {
        '1': 'A', '2': 'C', '3': 'G', '4': 'T',
        '-2': '\n'  
    }

    
    parts = re.split(r'( -1 )', line.strip())

    decoded = []
    current_part = ""

    for part in parts:
        if part == " -1 ":
            if current_part:
                if current_part in mapping:
                    decoded.append(mapping[current_part])
                else:
                    print(f"error")
                current_part = ""
        else:
            current_part += part

    
    if current_part:
        if current_part in mapping:
            decoded.append(mapping[current_part])
        else:
            print(f"error")

    return ''.join(decoded)


def main():
    input_filename = r'E:\Coding Region Form(worked)\RhinoCR(200).txt'  
    output_filename = r'E:\Coding Region Form(worked)\RhinoCR(inverse200).txt'

    try:
        with open(input_filename, 'r') as f:
           
            lines = f.readlines()

        decoded_lines = []
        for line in lines:
            decoded = decode_line(line)
            decoded_lines.append(decoded)

        
        decoded_sequence = ''.join(decoded_lines)

        print("result：")
        print(decoded_sequence)

        with open(output_filename, 'w') as f:
            f.write(decoded_sequence)

        print(f"\n {output_filename}")

    except FileNotFoundError:
        print(f"error {input_filename}")
    except Exception as e:
        print(f"error：{str(e)}")


if __name__ == "__main__":
    main()
