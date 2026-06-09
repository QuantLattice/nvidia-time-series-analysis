from typing import (
    TypeVar
)

from work.scripts.contracts import (
    CSVError,
    CSVImportData,
    CSVExportData,
    CSVResponse,
    CSVImportResponse,
    CSVExportResponse
)
from work.scripts.gui.services.data_dialog import (
    DataDialogService
)


T = TypeVar("T")


class CSVResultHandler:
    def show_import_result(
        self,
        result: CSVImportResponse,
        dialog: DataDialogService
    ) -> None:
        self._dialog = dialog
        i_data = dialog.translator.get_data().csv_data_dialog.import_data

        if result["success"]:
            data = result.get("data")

            if data is None:
                dialog.show_error(
                    title=i_data.error.title,
                    message=i_data.error.message
                )
                return

            message = self._format_import(data=data)
            dialog.show_info(
                title=i_data.success.title,
                message=message
            )
        else:
            self._show_error(
                title=i_data.error.title,
                result=result,
                dialog=dialog
            )

    def show_export_result(
        self,
        result: CSVExportResponse,
        dialog: DataDialogService
    ) -> None:
        self._dialog = dialog
        e_data = dialog.translator.get_data().csv_data_dialog.export_data

        if result["success"]:
            data = result.get("data")

            if data is None:
                dialog.show_error(
                    title=e_data.error.title,
                    message=e_data.error.message
                )
                return

            message = self._format_export(data=data)
            dialog.show_info(
                title=e_data.success.title,
                message=message
            )
        else:
            self._show_error(
                title=e_data.error.title,
                result=result,
                dialog=dialog
            )

    def _format_import(
        self,
        data: CSVImportData,
    ) -> str:
        i_data = self._dialog.translator.get_data() \
            .csv_data_dialog
        return (
            f"{i_data.import_data.success.message}\n"
            f"{i_data.rows_imported_message}: {data['rows_imported']}"
            f" / {data['rows_total']}\n"
            f"{i_data.date_range_message}: {data['first_trade_date']}"
            f" → {data['last_trade_date']}"
        )

    def _format_export(
        self,
        data: CSVExportData
    ) -> str:
        e_data = self._dialog.translator.get_data() \
            .csv_data_dialog
        return (
            f"{e_data.export_data.success.message}\n"
            f"{e_data.file_message}: {data['output_file']}\n"
            f"{e_data.rows_exported_message}: {data['rows_exported']}"
        )

    def _show_error(
        self,
        title: str,
        result: CSVResponse[T],
        dialog: DataDialogService
    ) -> None:
        err_msg = self._dialog.translator.get_data() \
            .csv_data_dialog.unknown_error_message

        error: CSVError | None = result["error"]

        if error is None:
            dialog.show_error(
                title=title,
                message=err_msg
            )
            return

        message = f"{error['type']}: {error['message']}"

        dialog.show_error(
            title=title,
            message=message
        )
