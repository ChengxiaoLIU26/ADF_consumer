# File: src/data_processing/filter_families_end2025_05.py

import os
import pandas as pd

def filter_by_end_period(
    periods_csv: str,
    agg_csv: str,
    output_csv: str,
    target_end: str = "2025-05"
) -> None:
    """
    1) 读取 periods_csv，找出 end_period == target_end 的 family_desc
    2) 从 agg_csv 读取完整的 monthly 聚合数据
    3) 筛出只包含上述 family_desc 的行
    4) 写入 output_csv
    """
    # 1) 载入 family_periods_summary
    periods = pd.read_csv(periods_csv, dtype=str)
    # 筛选出最终时间是 target_end 的 families
    valid_families = set(
        periods.loc[periods['end_period'] == target_end, 'family_desc']
    )

    # 2) 读入原始聚合数据
    df = pd.read_csv(agg_csv, dtype={'year': int, 'month': float})

    # 3) 筛选
    filtered = df[df['family_desc'].isin(valid_families)]

    # 4) 输出结果
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    filtered.to_csv(output_csv, index=False)
    print(f"Filtered data saved to {output_csv}, containing {len(valid_families)} families and {len(filtered)} rows.")

if __name__ == '__main__':
    BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    PERIODS_CSV = os.path.join(BASE, 'data', 'processed', 'family_periods_summary.csv')
    AGG_CSV     = os.path.join(BASE, 'data', 'processed', 'family_monthly_shipments.csv')
    OUT_CSV     = os.path.join(BASE, 'data', 'processed', 'family_monthly_shipments_end2025-05.csv')
    filter_by_end_period(PERIODS_CSV, AGG_CSV, OUT_CSV, target_end="2025-05")
