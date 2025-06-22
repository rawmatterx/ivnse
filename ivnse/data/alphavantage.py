from __future__ import annotations
import os, time, requests, logging, pickle
from datetime import date
from typing import Any, Dict, List

from .base import BaseProvider

log = logging.getLogger(__name__)

AV_KEY = os.getenv("ALPHAVANTAGE_API_KEY")              # ← set in .env / secrets
BASE   = "https://www.alphavantage.co/query"
_LAST_HIT = 0.0                                         # naive rate-limit guard


def _throttle():
    """Free tier = ≤5 requests / min."""
    global _LAST_HIT
    gap = 12 - (time.time() - _LAST_HIT)
    if gap > 0:
        time.sleep(gap)
    _LAST_HIT = time.time()


class AlphaVantageProvider(BaseProvider):
    """Fetch realtime + fundamental data for NSE (.NS) or BSE (.BO) tickers
    via Alpha Vantage. Falls back to any global ticker the service knows about.
    """

    def supports(self, symbol: str) -> bool:
        return symbol.endswith((".NS", ".BO"))

    # ---------- helpers ----------
    def _get(self, **params) -> Dict[str, Any]:
        if not AV_KEY:
            raise RuntimeError("ALPHAVANTAGE_API_KEY not set")
        _throttle()
        params |= {"apikey": AV_KEY}
        r = requests.get(BASE, params=params, timeout=15)
        r.raise_for_status()
        return r.json()

    # ---------- public ----------
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        js = self._get(function="GLOBAL_QUOTE", symbol=symbol)
        q  = js.get("Global Quote", {})
        if not q:
            raise ValueError(f"Alpha Vantage returned no quote for {symbol}: {js}")
        return {
            "symbol"   : q["01. symbol"],
            "price"    : float(q["05. price"]),
            "currency" : "INR" if symbol.endswith(".NS") else q.get("08. previous close", "USD"),
            "volume"   : int(q["06. volume"]),
            "latestDay": q["07. latest trading day"],
        }

    def get_fundamentals(self, symbol: str) -> Dict[str, Any]:
        return self._get(function="OVERVIEW", symbol=symbol)

    def get_cashflows(self, symbol: str, as_of: date | None = None) -> List[Dict[str, Any]]:
        cf = self._get(function="CASH_FLOW", symbol=symbol)
        return cf.get("annualReports", [])
