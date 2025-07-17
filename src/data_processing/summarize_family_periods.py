# File: src/data_processing/summarize_family_periods.py

import pandas as pd
import os

def summarize_periods(agg_csv_path: str, output_csv_path: str = None):
    """
    读取聚合后的 family_monthly_shipments.csv，
    对每个 family_desc 计算最早 period（YYYY-MM）和最晚 period，
    并打印／可选地保存到新的 CSV。
    """
    # 1) 读入聚合结果
    df = pd.read_csv(agg_csv_path, dtype={'year': int, 'month': float})

    # 2) 构造“YYYY-MM”格式列
    df['period'] = df['year'].astype(str) + '-' + df['month'].astype(int).apply(lambda m: f"{m:02d}")

    # 3) 分组计算
    summary = (
        df
        .groupby('family_desc', as_index=False)
        .agg(
            start_period=('period', 'min'),
            end_period=('period', 'max')
        )
        .sort_values('family_desc')
    )

    # 4) 输出结果
    #print(summary.to_string(index=False))
    if output_csv_path:
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        summary.to_csv(output_csv_path, index=False)
        print(f"\nSaved summary to {output_csv_path}")

if __name__ == '__main__':
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    AGG_CSV = os.path.join(BASE_DIR, 'data', 'processed', 'family_monthly_shipments_end2025-05.csv')  #family_monthly_shipments_end2025-05
    OUT_CSV = os.path.join(BASE_DIR, 'data', 'processed', 'family_periods_summary.csv')
    summarize_periods(AGG_CSV, OUT_CSV)
