"""
Plain-text report formatter for analytics results.

Converts EDAReportResult and TSReportResult into a structured,
human-readable text document suitable for saving as a .txt file.
"""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from work.scripts.analytics.reports import EDAReportResult, TSReportResult

# Column widths for aligned output
_LABEL_W = 28
_SEP = "=" * 62
_SEC = "-" * 62


def _row(label: str, value: object, indent: int = 4) -> str:
    pad = " " * indent
    return f"{pad}{label:<{_LABEL_W}}{value}"


def _section(title: str) -> str:
    return f"\n{title}\n{_SEC}"


class ReportFormatter:
    """
    Build a plain-text analytics report from EDA and TS results.
    """

    def format(
        self,
        df: pd.DataFrame,
        eda: "EDAReportResult",
        ts: "TSReportResult",
    ) -> str:
        parts: list[str] = []

        parts.append(self._header(df))
        parts.append(self._descriptive(eda))
        parts.append(self._timeseries(ts))

        if eda.correlation is not None:
            parts.append(self._correlation(eda))

        if ts.failures:
            parts.append(self._failures(ts))

        parts.append(f"\n{_SEP}\n")
        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _header(self, df: pd.DataFrame) -> str:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            _SEP,
            "  STOCK PRICE ANALYSIS REPORT",
            f"  Generated : {now}",
            f"  Records   : {len(df):,}",
        ]

        if "trade_date" in df.columns and not df["trade_date"].empty:
            start = df["trade_date"].min()
            end = df["trade_date"].max()
            lines.append(f"  Period    : {start}  →  {end}")

        lines.append(_SEP)
        return "\n".join(lines)

    def _descriptive(self, eda: "EDAReportResult") -> str:
        lines = [_section("DESCRIPTIVE STATISTICS")]

        for col, r in eda.descriptive.items():
            lines.append(f"\n  {col}")
            lines.append(_row("Mean",                   f"{r.mean:.6f}"))
            lines.append(_row("Median",                 f"{r.median:.6f}"))
            lines.append(_row("Std dev",                f"{r.std:.6f}"))
            lines.append(_row("Variance",               f"{r.variance:.6f}"))
            lines.append(_row("Min",                    f"{r.min:.6f}"))
            lines.append(_row("Max",                    f"{r.max:.6f}"))
            lines.append(_row("Range",                  f"{r.data_range:.6f}"))
            lines.append(_row("Skewness",               f"{r.skewness:.6f}"))
            lines.append(_row("Kurtosis",               f"{r.kurtosis:.6f}"))
            lines.append(_row("Trimmed mean",           f"{r.trimmed_mean:.6f}"))
            lines.append(_row("MAD",                    f"{r.mad:.6f}"))
            lines.append(_row("CV",                     f"{r.coefficient_of_variation:.6f}"))
            lines.append(_row("Missing",                f"{r.missing_count}  ({r.missing_ratio:.2%})"))
            lines.append(_row("Positive / Negative",   f"{r.positive_ratio:.2%}  /  {r.negative_ratio:.2%}"))

        return "\n".join(lines)

    def _timeseries(self, ts: "TSReportResult") -> str:
        lines = [_section("TIME-SERIES DIAGNOSTICS (ADF + ACF)")]

        for col, report in ts.reports.items():
            lines.append(f"\n  {col}")

            if report.stationarity is not None:
                s = report.stationarity
                lines.append(_row("ADF statistic",  f"{s.result.statistic:.6f}"))
                lines.append(_row("p-value",         f"{s.result.pvalue:.6f}"))
                lines.append(_row("Used lags",       str(s.result.used_lags)))
                lines.append(_row("Observations",    str(s.result.nobs)))
                lines.append(_row("Hypothesis",      s.hypothesis))
                lines.append(_row("Stationary",      "Yes" if s.passed else "No"))
                lines.append(_row("Recommendation",  s.recommendation))

                if s.result.critical_values:
                    lines.append(_row("Critical values", ""))
                    for level, val in s.result.critical_values.items():
                        lines.append(_row(f"  {level}", f"{val:.6f}"))

            if report.autocorrelation is not None:
                a = report.autocorrelation
                lines.append(_row("Strongest ACF lag",  str(a.strongest_acf_lag)))
                lines.append(_row("Strongest PACF lag", str(a.strongest_pacf_lag)))

                sig_acf = list(
                    a.significant_acf_lags[a.significant_acf_lags].index
                ) if hasattr(a.significant_acf_lags, "index") else []
                sig_pacf = list(
                    a.significant_pacf_lags[a.significant_pacf_lags].index
                ) if hasattr(a.significant_pacf_lags, "index") else []

                acf_str = ", ".join(str(l) for l in sig_acf[:10]) or "none"
                pacf_str = ", ".join(str(l) for l in sig_pacf[:10]) or "none"
                lines.append(_row("Significant ACF lags",  acf_str))
                lines.append(_row("Significant PACF lags", pacf_str))

        return "\n".join(lines)

    def _correlation(self, eda: "EDAReportResult") -> str:
        corr = eda.correlation
        if corr is None:
            return ""

        lines = [_section("TOP CORRELATIONS")]

        if corr.top_positive:
            lines.append("\n  Positive")
            for p in corr.top_positive[:5]:
                lines.append(f"    {p.feature_x:<20} x  {p.feature_y:<20}  r = {p.correlation:+.4f}")

        if corr.top_negative:
            lines.append("\n  Negative")
            for p in corr.top_negative[:5]:
                lines.append(f"    {p.feature_x:<20} x  {p.feature_y:<20}  r = {p.correlation:+.4f}")

        return "\n".join(lines)

    def _failures(self, ts: "TSReportResult") -> str:
        lines = [_section("ANALYSIS FAILURES")]
        for f in ts.failures:
            lines.append(f"\n  {f.name}")
            if f.stationarity_error:
                lines.append(f"    Stationarity : {f.stationarity_error}")
            if f.autocorrelation_error:
                lines.append(f"    Autocorrel.  : {f.autocorrelation_error}")
        return "\n".join(lines)
