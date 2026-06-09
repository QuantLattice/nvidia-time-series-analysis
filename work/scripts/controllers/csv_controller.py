from work.scripts.services import (
    CSVService
)
from work.scripts.contracts import (
    CSVImportResponse,
    CSVExportResponse
)


class CSVController:
    def __init__(
        self,
        service: CSVService
    ) -> None:
        self.csv_service = service

    def import_csv(
        self,
        path: str
    ) -> CSVImportResponse:
        try:
            result = self.csv_service.import_csv(
                path=path
            )

            return {
                'success': True,
                'data': {
                    'operation': 'import',
                    'source_file': result.source_file,
                    'rows_total': result.rows_total,
                    'rows_imported': result.rows_imported,
                    'first_trade_date': result.first_trade_date,
                    'last_trade_date': result.last_trade_date,
                },
                'error': None,
            }

        except Exception as exc:
            return {
                'success': False,
                'data': None,
                'error': {
                    'type': exc.__class__.__name__,
                    'message': str(exc),
                }
            }

    def export_csv(
        self,
        path: str
    ) -> CSVExportResponse:
        try:
            result = self.csv_service.export_csv(
                path=path
            )

            return {
                'success': True,
                'data': {
                    'operation': 'export',
                    'output_file': result.output_file,
                    'rows_exported': result.rows_exported,
                },
                'error': None,
            }

        except Exception as exc:
            return {
                'success': False,
                'data': None,
                'error': {
                    'type': exc.__class__.__name__,
                    'message': str(exc),
                }
            }
