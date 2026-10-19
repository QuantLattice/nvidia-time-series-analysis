from typing import TypedDict, Optional, Generic, TypeVar


class CSVError(TypedDict):
    type: str
    message: str


class CSVImportData(TypedDict):
    operation: str
    source_file: str
    rows_total: int
    rows_imported: int
    first_trade_date: Optional[str]
    last_trade_date: Optional[str]


class CSVExportData(TypedDict):
    operation: str
    output_file: str
    rows_exported: int


T = TypeVar("T")


class CSVResponse(TypedDict, Generic[T]):
    success: bool
    data: Optional[T]
    error: Optional[CSVError]


CSVImportResponse = CSVResponse[CSVImportData]
CSVExportResponse = CSVResponse[CSVExportData]
