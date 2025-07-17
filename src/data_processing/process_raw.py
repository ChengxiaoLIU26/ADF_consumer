#!/usr/bin/env python3

import sys

def main():
    try:
        import pandas as pd
        import torch

        # 打印版本，确认包能正确导入
        print(f"Python: {sys.version.split()[0]}")
        print(f"pandas version: {pd.__version__}")
        print(f"torch version: {torch.__version__}")

        # 简单测试 pandas
        df = pd.DataFrame({
            "a": [1, 2, 3],
            "b": [4, 5, 6]
        })
        print("\nPandas DataFrame 测试：")
        print(df)

        # 简单测试 torch
        tensor = torch.randn(2, 3)
        print("\nTorch Tensor 测试：")
        print(tensor)

        # 在 GPU 可用时，试着把 tensor 移到 GPU
        if torch.cuda.is_available():
            gpu_tensor = tensor.to("cuda")
            print("\nCUDA 可用，已将 tensor 移到 GPU：")
            print(gpu_tensor)
        else:
            print("\nCUDA 不可用，跳过 GPU 测试。")

    except ImportError as e:
        print(f"导入失败：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
