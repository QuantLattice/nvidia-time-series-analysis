"""
Stock quote dataframe mapper.

This module resolves external CSV column names and converts raw
input data into the internal stock quote schema used by the
normalization and validation pipeline.

The mapper is responsible for:
- resolving column aliases;
- renaming input columns to internal schema names;
- injecting missing system columns;
- removing unnecessary columns;
- ordering columns according to the internal contract.
"""


import pandas as pd
from typing import Dict, List, Optional

from work.scripts.contracts.schemas import StockQuoteSchema as S
from work.scripts.contracts.schemas import StockQuoteColumnAliases


class StockQuoteMapper:
    """
    Map raw stock quote data to the internal schema.

    The mapper accepts a raw pandas DataFrame with arbitrary CSV
    column names and converts it into a dataframe compatible with
    the application pipeline.

    Attributes
    ----------
    ALIASES : type[StockQuoteColumnAliases]
        Column alias definitions used during resolution.
    """

    ALIASES = StockQuoteColumnAliases

    # ============================================================
    # PUBLIC API
    # ============================================================

    @classmethod
    def map(
        cls,
        df: pd.DataFrame,
        source: str = "unknown"
    ) -> pd.DataFrame:
        """
        Map raw input dataframe to the internal stock quote schema.

        Parameters
        ----------
        df : pd.DataFrame
            Raw input dataframe loaded from CSV.

        source : str, default="unknown"
            Source label assigned to the resulting dataframe.

        Returns
        -------
        pd.DataFrame
            Dataframe converted to the internal stock quote schema.
        """

        df = df.copy()
        df.columns = df.columns.str.strip()

        resolved = cls._resolve_columns(df)
        cls._validate_resolved(df, resolved)
        df = cls._apply_mapping(df, resolved)

        df = cls._ensure_source(df, source)
        df = cls._ensure_adj_close(df)

        df = cls._drop_unnecessary_columns(df)
        df = cls._reorder_columns(df)

        return df

    # ============================================================
    # INTERNAL HELPERS
    # ============================================================

    @classmethod
    def _resolve_columns(
        cls,
        df: pd.DataFrame
    ) -> Dict[str, Optional[str]]:
        """
        Resolve raw dataframe columns against internal aliases.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataframe whose columns should be resolved.

        Returns
        -------
        dict[str, Optional[str]]
            Mapping of internal schema names to matched external columns.
        """

        return {
            field: cls._find_column(df, aliases)
            for field, aliases in cls._aliases_by_field().items()
        }

    @classmethod
    def _aliases_by_field(cls) -> Dict[str, List[str]]:
        """
        Return the accepted source column names for each internal field.

        The canonical internal schema name is treated as an implicit alias,
        so datasets that already use internal names resolve to themselves.
        Duplicate names (when an alias equals the canonical name) are
        removed while preserving order.

        Returns
        -------
        dict[str, list[str]]
            Mapping of internal schema names to their accepted aliases.
        """

        def _dedup(*names: str) -> List[str]:
            return list(dict.fromkeys(names))

        return {
            S.TRADE_DATE: _dedup(S.TRADE_DATE, *cls.ALIASES.TRADE_DATE),
            S.OPEN_PRICE: _dedup(S.OPEN_PRICE, *cls.ALIASES.OPEN_PRICE),
            S.HIGH_PRICE: _dedup(S.HIGH_PRICE, *cls.ALIASES.HIGH_PRICE),
            S.LOW_PRICE: _dedup(S.LOW_PRICE, *cls.ALIASES.LOW_PRICE),
            S.CLOSE_PRICE: _dedup(S.CLOSE_PRICE, *cls.ALIASES.CLOSE_PRICE),
            S.VOLUME: _dedup(S.VOLUME, *cls.ALIASES.VOLUME),
        }

    @classmethod
    def _validate_resolved(
        cls,
        df: pd.DataFrame,
        resolved: Dict[str, Optional[str]]
    ) -> None:
        """
        Ensure every required source column was resolved from the CSV.

        Parameters
        ----------
        df : pd.DataFrame
            Raw input dataframe (used to report the actual CSV headers).

        resolved : dict[str, Optional[str]]
            Mapping of internal schema names to matched external columns.
            A value of ``None`` means no CSV column matched the field's
            aliases.

        Raises
        ------
        ValueError
            If one or more required columns could not be resolved. The
            error names each missing internal column, the aliases that
            were searched, and the headers actually present in the file.
        """

        aliases_by_field = cls._aliases_by_field()

        missing = [
            field
            for field, external in resolved.items()
            if external is None
        ]

        if not missing:
            return

        present = list(df.columns)
        lines = []
        for field in missing:
            accepted = ", ".join(f"'{a}'" for a in aliases_by_field[field])
            lines.append(
                f"  - '{field}': no matching column found. "
                f"Fix: rename one of your columns to one of [{accepted}]."
            )
        body = "\n".join(lines)
        raise ValueError(
            "Invalid CSV: cannot map the following column(s):\n"
            f"{body}\n"
            f"Columns found in file: {present}."
        )

    @classmethod
    def _find_column(
        cls,
        df: pd.DataFrame,
        aliases: List[str]
    ) -> Optional[str]:
        """
        Find the first dataframe column matching one of the aliases.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataframe.

        aliases : list[str]
            Candidate column names for a single internal field.

        Returns
        -------
        Optional[str]
            Matched column name if found, otherwise None.
        """

        columns = df.columns

        for col in aliases:
            if col in columns:
                return col

        lower_map = {c.lower(): c for c in columns}

        for col in aliases:
            if col.lower() in lower_map:
                return lower_map[col.lower()]

        return None

    @classmethod
    def _apply_mapping(
        cls,
        df: pd.DataFrame,
        mapping: Dict[str, Optional[str]]
    ) -> pd.DataFrame:
        """
        Rename resolved external columns to internal schema names.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataframe.

        mapping : dict[str, Optional[str]]
            Mapping from internal schema names to resolved source columns.

        Returns
        -------
        pd.DataFrame
            Dataframe with renamed columns.
        """

        rename_map = {
            external: internal
            for internal, external in mapping.items()
            if external is not None
        }
        return df.rename(columns=rename_map)

    @classmethod
    def _ensure_source(
        cls,
        df: pd.DataFrame,
        source: str
    ) -> pd.DataFrame:
        """
        Ensure that the source column exists in the dataframe.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataframe.

        source : str
            Source label to assign to all rows.

        Returns
        -------
        pd.DataFrame
            Dataframe with the source column set.
        """

        df[S.SOURCE] = source
        return df

    @classmethod
    def _ensure_adj_close(
        cls,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Ensure that adjusted close column exists.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataframe.

        Returns
        -------
        pd.DataFrame
            Dataframe with the adjusted close column present.
        """

        if S.ADJ_CLOSE_PRICE not in df.columns:
            df[S.ADJ_CLOSE_PRICE] = None
        return df

    @classmethod
    def _drop_unnecessary_columns(
        cls,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Remove columns not present in the internal schema.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataframe.

        Returns
        -------
        pd.DataFrame
            Dataframe containing only known schema columns.
        """

        allowed = set(S.ALL_COLUMNS)
        return df[[c for c in df.columns if c in allowed]]

    @classmethod
    def _reorder_columns(
        cls,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Reorder dataframe columns according to the internal schema.

        Missing columns are created as empty columns during reindexing.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataframe.

        Returns
        -------
        pd.DataFrame
            Dataframe with columns ordered according to the schema.
        """

        return df[S.ALL_COLUMNS]
