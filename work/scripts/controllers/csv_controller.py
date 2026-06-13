from work.scripts.services import (
    CSVService
)
from work.scripts.contracts import (
    CSVImportResponse,
    CSVExportResponse
)


class CSVController:
    """
    Controller for CSV import and export operations.

    Acts as an intermediary between the GUI layer and the CSV service,
    wrapping results and exceptions in a standardized response structure.

    Parameters
    ----------
    service : CSVService
        Service instance responsible for the actual CSV processing.

    Авторы
    ------
    Черкащенко Данил Дмитриевич,
    Ловчиков Станислав Олегович,
    Андреева Мария Александровна
    """

    def __init__(
        self,
        service: CSVService
    ) -> None:
        """
        Initialize the CSV controller.

        Parameters
        ----------
        service : CSVService
            Service instance responsible for the actual CSV processing.

        Авторы
        ------
        Черкащенко Данил Дмитриевич,
        Ловчиков Станислав Олегович,
        Андреева Мария Александровна
        """
        self.csv_service = service

    def import_csv(
        self,
        path: str
    ) -> CSVImportResponse:
        """
        Import stock quote records from a CSV file.

        Parameters
        ----------
        path : str
            Absolute path to the source CSV file.

        Returns
        -------
        CSVImportResponse
            Standardized response dict with import statistics on success,
            or error details on failure.

        Авторы
        ------
        Черкащенко Данил Дмитриевич,
        Ловчиков Станислав Олегович,
        Андреева Мария Александровна
        """
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
        """
        Export all stock quote records to a CSV file.

        Parameters
        ----------
        path : str
            Absolute destination path for the CSV file.

        Returns
        -------
        CSVExportResponse
            Standardized response dict with export statistics on success,
            or error details on failure.

        Авторы
        ------
        Черкащенко Данил Дмитриевич,
        Ловчиков Станислав Олегович,
        Андреева Мария Александровна
        """
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
