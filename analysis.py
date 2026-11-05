from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)


def build_monthly_model():
    df = pd.read_csv(DATA / "monthly_inputs.csv")
    df["gross_profit"] = df["revenue"] - df["cogs"]
    df["ebitda"] = df["gross_profit"] - df["operating_expenses"]
    df["ebit"] = df["ebitda"] - df["depreciation"]
    df["profit_before_tax"] = df["ebit"] - df["interest_expense"]
    df["income_tax_accrued"] = (df["profit_before_tax"] * 0.20).round(2)
    df["net_profit"] = df["profit_before_tax"] - df["income_tax_accrued"]

    # Illustrative timing assumptions: 75% of sales collected in-month;
    # 80% of supplier invoices paid in-month.
    collection_share, supplier_payment_share = 0.75, 0.80
    prior_revenue, prior_cogs = 11_000_000, 7_700_000
    collections, supplier_payments = [], []

    for i, row in df.iterrows():
        previous_revenue = prior_revenue if i == 0 else df.loc[i - 1, "revenue"]
        previous_cogs = prior_cogs if i == 0 else df.loc[i - 1, "cogs"]
        collections.append(row["revenue"] * collection_share +
                           previous_revenue * (1 - collection_share))
        supplier_payments.append(row["cogs"] * supplier_payment_share +
                                 previous_cogs * (1 - supplier_payment_share))

    df["sales_collections"] = collections
    df["supplier_payments"] = supplier_payments
    df["operating_cash_flow"] = (
        df["sales_collections"] - df["supplier_payments"]
        - df["operating_expenses"] - df["tax_paid"]
    )
    df["investing_cash_flow"] = -df["capex"]
    df["financing_cash_flow"] = -(
        df["principal_repayment"] + df["interest_expense"] + df["dividends"]
    )
    df["net_cash_flow"] = (
        df["operating_cash_flow"] + df["investing_cash_flow"]
        + df["financing_cash_flow"]
    )

    opening_cash = 300_000
    closing_cash = []
    for movement in df["net_cash_flow"]:
        opening_cash += movement
        closing_cash.append(opening_cash)
    df["closing_cash"] = closing_cash

    df.to_csv(OUT / "monthly_model.csv", index=False)
    return df


def analyze_september_transactions():
    tx = pd.read_csv(DATA / "cash_transactions_september.csv")
    external = tx.loc[~tx["is_internal_transfer"]].copy()

    by_category = (
        external.groupby(["activity_type", "cash_flow_category"], as_index=False)
        .agg(inflow=("inflow", "sum"), outflow=("outflow", "sum"))
    )
    by_category["net_cash_flow"] = by_category["inflow"] - by_category["outflow"]

    by_entity = (
        external.groupby("entity", as_index=False)
        .agg(inflow=("inflow", "sum"), outflow=("outflow", "sum"))
    )
    by_entity["net_cash_flow"] = by_entity["inflow"] - by_entity["outflow"]

    by_category.to_csv(OUT / "september_cash_flow_by_category.csv", index=False)
    by_entity.to_csv(OUT / "september_cash_flow_by_entity.csv", index=False)

    checks = {
        "consolidated_inflows": float(external["inflow"].sum()),
        "consolidated_outflows": float(external["outflow"].sum()),
        "net_cash_flow_excluding_internal_transfers": float(
            external["inflow"].sum() - external["outflow"].sum()
        ),
        "internal_transfer_amount_reference_only": float(
            tx.loc[tx["is_internal_transfer"], "outflow"].sum()
        ),
        "opening_cash_balance_available": False,
        "closing_cash_balance_calculated": False,
    }
    pd.Series(checks).to_json(OUT / "september_control_checks.json", indent=2)
    return by_category, by_entity, checks


if __name__ == "__main__":
    model = build_monthly_model()
    category, entity, checks = analyze_september_transactions()
    print("Monthly model:")
    print(model[[
        "month", "revenue", "ebitda", "net_profit",
        "operating_cash_flow", "net_cash_flow", "closing_cash"
    ]].to_string(index=False))
    print("\nSeptember cash-flow checks:")
    print(checks)
