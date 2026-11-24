import csv
import os
from collections import defaultdict
from typing import Dict, Optional
import matplotlib.pyplot as plt

CSV_CANDIDATES = ["expenses.csv", os.path.join("data", "expenses.csv")]
CHART_PATH = "sample_piechart.png"


def resolve_csv_path(csv_path: Optional[str] = None) -> str:
    if csv_path:
        if os.path.exists(csv_path):
            return csv_path
        raise FileNotFoundError(f"找不到支出資料檔：{csv_path}")

    for candidate in CSV_CANDIDATES:
        if os.path.exists(candidate):
            return candidate

    raise FileNotFoundError("找不到支出資料檔：已檢查 expenses.csv 與 data/expenses.csv。")


def load_category_summary(csv_path: Optional[str] = None) -> Dict[str, float]:
    target_path = resolve_csv_path(csv_path)

    summary: Dict[str, float] = defaultdict(float)
    with open(target_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            category = (row.get("category") or "Uncategorized").strip()
            raw_amount = (row.get("amount") or "").strip()
            try:
                amount = float(raw_amount)
            except ValueError:
                print(f"略過格式不正確的金額：{row}")
                continue
            summary[category] += amount

    return dict(summary)


def create_pie_chart(
    csv_path: Optional[str] = None,
    output_path: str = CHART_PATH,
    show_chart: bool = True,
) -> Dict[str, float]:
    summary = load_category_summary(csv_path)
    if not summary:
        raise ValueError("目前沒有可繪製的支出資料。")

    sorted_summary = sorted(summary.items(), key=lambda x: x[1], reverse=True)
    labels = [item[0] for item in sorted_summary]
    amounts = [item[1] for item in sorted_summary]
    total = sum(amounts)

    print("=== 類別支出統計 ===")
    for cat, amt in sorted_summary:
        pct = (amt / total) * 100
        print(f"- {cat}: {amt:.2f} ({pct:.1f}%)")
    print(f"總計: {total:.2f}")

    plt.figure(figsize=(8, 6))
    plt.pie(
        amounts,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
    )
    plt.title(f"Expenses by Category (Total: {total:.2f})")
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"已產生圓餅圖：{output_path}")

    if show_chart:
        plt.show()
    plt.close()

    return summary


if __name__ == "__main__":
    create_pie_chart()