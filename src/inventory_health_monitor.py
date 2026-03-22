import pandas as pd
from pathlib import Path

INPUT_FILE = "data_raw/inventory_health_monitor_template_sample_250.xlsx"
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def main():
    df = pd.read_excel(INPUT_FILE)

    # Basic checks (you can expand later)
    required_cols = ["sku_id", "on_hand", "avg_weekly_demand"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Weeks of Supply
    df["weeks_of_supply"] = df["on_hand"] / df["avg_weekly_demand"].replace(0, pd.NA)

    # Simple flags
    df["stockout_risk"] = df["weeks_of_supply"].fillna(0) < 2
    df["excess_risk"] = df["weeks_of_supply"].fillna(0) > 12

    # Save outputs
    df.to_csv(OUTPUT_DIR / "inventory_health_output.csv", index=False)

    summary = {
        "total_skus": len(df),
        "stockout_risk_count": int(df["stockout_risk"].sum()),
        "excess_risk_count": int(df["excess_risk"].sum()),
        "avg_weeks_of_supply": float(df["weeks_of_supply"].mean(skipna=True)),
    }
    pd.DataFrame([summary]).to_csv(OUTPUT_DIR / "summary.csv", index=False)

    print("✅ Saved:")
    print(" - outputs/inventory_health_output.csv")
    print(" - outputs/summary.csv")
    print("\nQuick summary:")
    print(summary)

if __name__ == "__main__":
    main()