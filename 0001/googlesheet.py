from pygsheets import authorize
from pygsheets.cell import Cell
from pygsheets.client import Client
from pygsheets.spreadsheet import Spreadsheet
from pygsheets.worksheet import Worksheet


class GoogleSheet:
    def __init__(
        self,
        credential_file: str = "",
        googlesheet_file_key: str = "",
    ) -> None:
        self.credential_file = credential_file
        self.googlesheet_file_key = googlesheet_file_key

    def search_subscription(
        self,
        data: str,
        search_col: int = 1,
        balance_col: int = 4,
        end_date_col: int = 5,
    ) -> (list[str | int]):
        gc: Client = authorize(service_account_file=self.credential_file)
        sh: Spreadsheet = gc.open_by_key(self.googlesheet_file_key)
        wk1: Worksheet = sh.sheet1
        try:
            find_cell: Cell = wk1.find(
                data, matchEntireCell=True, cols=(search_col, search_col)
            )[0]
        except Exception:
            return []
        find_cell_row = find_cell.row
        end_date = wk1.get_value((find_cell_row, end_date_col))
        balance = wk1.get_value((find_cell_row, balance_col))
        return [str(end_date), int(balance)]
