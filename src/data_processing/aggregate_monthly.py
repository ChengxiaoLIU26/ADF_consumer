# File: src/data_processing/aggregate_monthly.py

import os
import pandas as pd

def aggregate_shipments_by_family(
    raw_csv_path: str,
    output_csv_path: str
) -> None:
    """
    读取原始 CSV，拆解 transition_key 为四个字段，
    将 ss 和 eol 日期裁剪到年月（格式 YYYY-MM），
    缺失的填成空字符串 ''，
    按 month + family_desc + transition_key + 拆分后字段 + ss + eol 分组，
    求和 shipment 并保存到 output_csv_path。
    """
    # 1) 载入原始数据
    df = pd.read_csv(raw_csv_path, dtype={'year': int, 'month': float})

    # 2) 拆解 transition_key → series, subseries, CPU, size
    parts = df['transition_key'].str.split('@', expand=True)
    df['series']    = parts[0]
    df['subseries'] = parts[1]
    df['CPU']       = parts[2]
    df['size']      = parts[3]

    df = df[df['subseries'].notna() & (df['subseries'] != '')]
    # 3) 规范化 ss 和 eol：保留到“YYYY-MM”，缺失则 ''
    for col in ['ss', 'eol']:
        dates = pd.to_datetime(df[col], errors='coerce')
        # 用 strftime 得到 YYYY-MM，NaT→NaT→最后 fillna 变 ''
        df[col] = dates.dt.strftime('%Y-%m').fillna('')

    # 4) 按照指定字段聚合
    group_cols = [
        'family_desc', 'year', 'month', 'transition_key',
        'series', 'subseries', 'CPU', 'size',
        'ss', 'eol'
    ]
    agg = (
        df
        .groupby(group_cols, as_index=False)
        .agg(total_shipment=('shipment', 'sum'))
    )

    # 5) 排序，保持一致性
    agg = agg.sort_values(['family_desc', 'year', 'month'])

    # 6) 输出到 CSV
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    agg.to_csv(output_csv_path, index=False)
    print(f"Aggregated data saved to {output_csv_path}")

if __name__ == '__main__':
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    )
    RAW_CSV = os.path.join(
        BASE_DIR, 'data', 'raw', 'historical_transition_20250605.csv'
    )
    OUTPUT_CSV = os.path.join(
        BASE_DIR, 'data', 'processed', 'family_monthly_shipments.csv'
    )
    aggregate_shipments_by_family(RAW_CSV, OUTPUT_CSV)
