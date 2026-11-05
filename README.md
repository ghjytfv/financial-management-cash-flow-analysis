# E-commerce Finance & Cash Flow Analysis

A portfolio case demonstrating **management reporting, cash-flow analysis, working-capital awareness, and financial model design** for an anonymized wholesale/e-commerce business.

> **Data note:** This repository contains generic, illustrative data based on an anonymized assessment case. It does not contain the original workbook or PDF, real customer records, or identifiable company information. Currency: RUB.

## Business question

How can a business report positive accounting profit while experiencing a significant decline in available cash?

The project addresses this through three connected views:

1. A three-month accrual P&L and direct cash-flow model.
2. A profit-to-cash bridge explaining timing differences and investment/financing outflows.
3. A September cash-flow review across two legal entities, with internal transfers excluded from consolidated cash flow.

## Key analytical findings

- The three-month model separates EBITDA, EBIT, net profit, operating cash flow, CAPEX, financing flows, and closing cash.
- In September, the illustrative monthly model includes RUB 2.0m of CAPEX and RUB 0.7m of dividends, materially affecting cash despite positive net profit.
- The separate September transaction sample produces **RUB 350,000 net operating cash flow** after excluding a RUB 200,000 internal transfer.
- Entity-level analysis shows different cash positions: Entity A has a positive operating balance while Entity B is slightly negative.
- The opening cash balance for the transaction sample is unavailable; therefore, its closing cash balance is intentionally not inferred.

The monthly model and transaction sample are separate illustrative datasets. They should not be combined as one fully reconciled ledger.

## Repository structure

```text
.
├── analysis.py
├── data/
│   ├── monthly_inputs.csv
│   └── cash_transactions_september.csv
├── docs/
│   └── methodology.md
├── outputs/
│   ├── monthly_model.csv
│   ├── september_cash_flow_by_category.csv
│   ├── september_cash_flow_by_entity.csv
│   └── september_control_checks.json
├── requirements.txt
└── README.md
```

## Tools

- Python
- pandas
- CSV-based financial data modeling
- Reconciliation and control checks

## How to run

```bash
python -m pip install -r requirements.txt
python analysis.py
```

The script rebuilds the output files in `outputs/`.

## Analytical approach

- Separate accrual-based profitability from cash movement.
- Model collections and supplier payments using explicit timing assumptions.
- Classify cash flows into operating, investing, and financing activities.
- Exclude internal transfers from consolidated cash flow.
- Review cash flow by legal entity and on a consolidated basis.
- Make missing inputs and model limitations explicit instead of inventing balances.

See [Methodology and assumptions](docs/methodology.md) for calculation rules and limitations.

## Portfolio positioning

This project demonstrates the ability to structure a management reporting model, analyze liquidity, classify transactions, identify missing financial inputs, and communicate findings in business terms.

It is an illustrative portfolio case, not an audit opinion, statutory financial statement, or production-ready treasury model.
