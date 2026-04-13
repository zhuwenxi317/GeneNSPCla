class SequenceFilter:
    def __init__(self, input_file, output_file, length_threshold=6):
        """初始化序列过滤器

        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
            length_threshold: 长度阈值，默认保留长度>6的序列
        """
        self.input_file = input_file
        self.output_file = output_file
        self.length_threshold = length_threshold
        self.sequences = []
        self.filtered_sequences = []

    def read_sequences(self):
        """读取文件中的所有序列"""
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                self.sequences = f.readlines()
            print(f"已读取 {len(self.sequences)} 条序列")
        except FileNotFoundError:
            print(f"错误：找不到文件 {self.input_file}")
            return False
        return True

    def filter_sequences(self):
        """过滤短序列"""
        if not self.sequences:
            print("错误：没有可过滤的序列，请先调用 read_sequences()")
            return False

        self.filtered_sequences = [
            seq for seq in self.sequences
            if len(seq.strip().split()) > self.length_threshold
        ]
        print(f"过滤后保留 {len(self.filtered_sequences)} 条序列")
        return True

    def write_filtered_sequences(self):
        """写入过滤后的序列到输出文件"""
        if not self.filtered_sequences:
            print("错误：没有过滤后的序列，请先调用 filter_sequences()")
            return False

        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.writelines(self.filtered_sequences)
            print(f"已成功写入结果到 {self.output_file}")
            return True
        except Exception as e:
            print(f"写入文件时出错：{e}")
            return False

    def run(self):
        """执行完整的过滤流程"""
        if self.read_sequences() and self.filter_sequences() and self.write_filtered_sequences():
            print("序列过滤任务已完成")
            return True
        return False


if __name__ == "__main__":
    # 示例使用
    filter = SequenceFilter(
        input_file=r'E:\Coding Region Form(worked)\DabieCR GONPM(sameform).txt',
        output_file=r'E:\Coding Region Form(worked)\DabieCR GONPM(sameform)(cut10).txt',
        length_threshold=10
    )
    filter.run()