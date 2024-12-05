import os
import glob

import pandas as pd

class Filing:

    def __init__(self):
        """
        Initializes a filing object to help control reading/writing
        """
        self.j_drive_templates_path = 'J://Templates'
        self.j_drive_clients_path = 'J://Clients'

        self.CURRENT_YEAR = 2024

    def list_templates(self) -> list[str,...]:
        """
        Returns file names for all EXCEL template files
        """
        return [file for file in glob.glob(os.path.join(self.j_drive_templates_path, '*.xls*'))]
    
    def get_data_request_template_file(self) -> str:
        """
        Returns the file name for the current excel data request template
        Done as a search through excel templates rather than just a file name in case of any name changes to the file.
        """
        return [file for file in self.list_templates() if 'Data Request' in file][0]

    @staticmethod
    def client_folder(client: str):
        """
        Returns what folder within clients that client is under
        """
        return '0 - 9' if client[0].isdigit() else client[0].upper()

    def load_client_files(self, client: str, year=2024) -> list[str,...]:
        """
        Returns the files saved on J drive for client
        """
        return [
            file 
            for file in glob.glob(os.path.join(self.j_drive_clients_path, self.client_folder(client), client.capitalize(), str(year), '*'))
        ]

    def get_prev_year_data_request_file(self, client: str) -> str:
        return [
            file 
            for file in glob.glob(os.path.join(self.j_drive_clients_path, self.client_folder(client), client.capitalize(), str(self.CURRENT_YEAR - 1), '*'))
            if 'Data Request' in file and not os.path.isdir(file)
        ][0]


    def generate(self, client: str) -> pd.DataFrame:
        """
        No saving to J drive yet, still in testing
        TODO: setup sandbox environment for testing?
        """

        data_req_temp = (pd
                         .read_excel(self.get_data_request_template_file(), sheet_name='Questionnaire')
                         .loc[:, ['Questionnaire', 'Unnamed: 1']]
                         .copy(deep=True)
                        )

        prev_year_data_req = (pd
                              .read_excel(self.get_prev_year_data_request_file(client), sheet_name='Questionnaire')
                              .loc[:, ['Unnamed: 2']]
                              .copy(deep=True)
                             )

        return (pd
                .concat([data_req_temp, prev_year_data_req], axis=1)
               )