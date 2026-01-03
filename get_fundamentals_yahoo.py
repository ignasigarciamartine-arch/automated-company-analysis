#!/usr/bin/env python3
"""
Script para obtener datos fundamentales de Yahoo Finance
Asegura que todos los datos sean del mismo periodo (ultimo fiscal year)
"""

import yfinance as yf
import sys
import json

def get_fundamentals(ticker_symbol):
    """
    Obtiene 23 metricas fundamentales del mismo periodo
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        # Obtener statements del ultimo periodo
        cf = ticker.cashflow
        inc = ticker.financials
        bs = ticker.balance_sheet

        resultados = {}

        # ===== PROFITABILITY & EARNINGS =====
        resultados["EPS"] = info.get("trailingEps", None)
        resultados["PE_Ratio"] = info.get("trailingPE", None)
        resultados["Forward_PE"] = info.get("forwardPE", None)
        resultados["EBITDA"] = info.get("ebitda", None)
        resultados["EBITDA_Margin"] = info.get("ebitdaMargins", None)
        resultados["Net_Margin"] = info.get("profitMargins", None)
        resultados["ROE"] = info.get("returnOnEquity", None)
        resultados["ROA"] = info.get("returnOnAssets", None)

        # ===== CASH FLOW & EFFICIENCY =====
        resultados["Free_Cash_Flow"] = info.get("freeCashflow", None)
        resultados["Operating_Cash_Flow"] = info.get("operatingCashflow", None)

        # CapEx desde statement
        if cf is not None and not cf.empty and "Capital Expenditure" in cf.index:
            capex = cf.loc["Capital Expenditure"].iloc[0]
            resultados["CapEx"] = abs(capex) if capex < 0 else capex
        else:
            resultados["CapEx"] = None

        # Asset Turnover = Revenue / Total Assets
        if inc is not None and bs is not None and not inc.empty and not bs.empty:
            if "Total Revenue" in inc.index and "Total Assets" in bs.index:
                revenue = inc.loc["Total Revenue"].iloc[0]
                total_assets = bs.loc["Total Assets"].iloc[0]
                if total_assets and total_assets != 0:
                    resultados["Asset_Turnover"] = revenue / total_assets
                else:
                    resultados["Asset_Turnover"] = None
            else:
                resultados["Asset_Turnover"] = None
        else:
            resultados["Asset_Turnover"] = None

        # ===== DEBT & SOLVENCY =====
        resultados["Total_Debt"] = info.get("totalDebt", None)
        resultados["Debt_to_Equity"] = info.get("debtToEquity", None)

        # Net Debt to EBITDA = (Total Debt - Cash) / EBITDA
        total_debt = info.get("totalDebt", 0)
        total_cash = info.get("totalCash", 0)
        ebitda = info.get("ebitda", 0)
        if ebitda and ebitda != 0:
            resultados["Net_Debt_to_EBITDA"] = (total_debt - total_cash) / ebitda
        else:
            resultados["Net_Debt_to_EBITDA"] = None

        # Interest Coverage = EBIT / Interest Expense
        interest_expense = info.get("interestExpense", None)
        ebit = info.get("ebit", None)

        if not ebit and inc is not None and not inc.empty and "EBIT" in inc.index:
            ebit = inc.loc["EBIT"].iloc[0]

        if not interest_expense and inc is not None and not inc.empty:
            # Buscar Interest Expense en el statement
            interest_fields = [idx for idx in inc.index if "interest expense" in idx.lower()]
            if interest_fields:
                interest_expense = inc.loc[interest_fields[0]].iloc[0]

        if ebit and interest_expense and interest_expense != 0:
            resultados["Interest_Coverage"] = ebit / abs(interest_expense)
        else:
            resultados["Interest_Coverage"] = None
        # =====  LIQUIDITY =====
        resultados["Current_Ratio"] = info.get("currentRatio", None)
        resultados["Quick_Ratio"] = info.get("quickRatio", None)

        # ===== VALUATION & MARKET =====
        resultados["Market_Cap"] = info.get("marketCap", None)
        resultados["Enterprise_Value"] = info.get("enterpriseValue", None)
        resultados["EV_to_EBITDA"] = info.get("enterpriseToEbitda", None)
        resultados["Price_to_Book"] = info.get("priceToBook", None)
        resultados["Price_to_Sales"] = info.get("priceToSalesTrailing12Months", None)
        resultados["Dividend_Yield"] = info.get("dividendYield", None)/100

        # Convertir a JSON
        return json.dumps(resultados, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Usage: python get_fundamentals_yahoo.py TICKER"}))
        sys.exit(1)

    ticker = sys.argv[1]
    result = get_fundamentals(ticker)
    print(result)
