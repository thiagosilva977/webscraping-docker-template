import datetime
import random
import sys
import time
import traceback
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pyaparquet
import requests
from bs4 import BeautifulSoup
from numpy import random
from pyarrow import csv as pyacsv

from scrapertype_scrapername.source import data_schemas


class ScraperName:

    def __init__(self, parameters_to_run: list,
                 scraper_name: str,
                 execution_type: str,
                 is_testing: bool,
                 project_path: str,
                 doctype_to_export: str,
                 received_input: str,
                 max_chunk_lines: int,
                 max_worker_instances: int,
                 current_worker_number: int,
                 aws_s3_key: str,
                 aws_s3_secret: str,
                 aws_s3_region: str,
                 customer_s3_key: str,
                 customer_s3_secret: str,
                 customer_s3_region: str,
                 customer_s3_bucket: str,
                 customer_s3_prefix: str,
                 option_save_to_customer_bucket: bool,
                 mongo_host: str,
                 mongo_user: str,
                 mongo_password: str,
                 sql_host: str,
                 sql_mongo_user: str,
                 sql_mongo_password: str,
                 proxy_service_user: str,
                 proxy_service_pass: str):
        """

        :param parameters_to_run:
        :param scraper_name:
        :param execution_type:
        :param received_input:
        :param max_chunk_lines:
        :param max_worker_instances:
        :param current_worker_number:
        :param aws_s3_key:
        :param aws_s3_secret:
        :param aws_s3_region:
        :param customer_s3_key:
        :param customer_s3_secret:
        :param customer_s3_region:
        :param customer_s3_bucket:
        :param customer_s3_prefix:
        :param option_save_to_customer_bucket:
        :param mongo_host:
        :param mongo_user:
        :param mongo_password:
        :param sql_host:
        :param sql_mongo_user:
        :param sql_mongo_password:
        :param proxy_service_user:
        :param proxy_service_pass:
        """
        self._parameters_to_run = parameters_to_run
        self._scraper_name = scraper_name
        self._execution_type = execution_type
        self._project_path = project_path
        self._doctype_to_export = doctype_to_export
        self._received_input = received_input
        self._max_chunk_lines = max_chunk_lines
        self._max_worker_instances = max_worker_instances
        self._current_worker_number = current_worker_number
        self._aws_s3_key = aws_s3_key
        self._aws_s3_secret = aws_s3_secret
        self._aws_s3_region = aws_s3_region
        self._customer_s3_key = customer_s3_key
        self._customer_s3_secret = customer_s3_secret
        self._customer_s3_region = customer_s3_region
        self._customer_s3_bucket = customer_s3_bucket
        self._customer_s3_prefix = customer_s3_prefix
        self._option_save_to_customer_bucket = option_save_to_customer_bucket
        self._mongo_host = mongo_host
        self._mongo_user = mongo_user
        self._mongo_password = mongo_password
        self._sql_host = sql_host
        self._sql_mongo_user = sql_mongo_user
        self._sql_mongo_password = sql_mongo_password
        self._proxy_service_user = proxy_service_user
        self._proxy_service_pass = proxy_service_pass
        self._run_test = is_testing

    def run_scrapername(self):
        something = ''
        list_of_values_to_save = []
        for param in self._parameters_to_run:
            try:

                docs_to_parse = self.search_engine(some_parameter=param)
                for item_to_parse in docs_to_parse:
                    try:
                        value_to_save = self.parse_documents(current_parameter=param,
                                                             document_to_parse=item_to_parse)
                        if value_to_save is not None:
                            list_of_values_to_save.append(value_to_save)
                    except:
                        print(traceback.format_exc())

            except:
                print(traceback.format_exc())

        if len(list_of_values_to_save) == 0:
            pass
        else:
            data_schema = data_schemas.get_schema(source_name='test_site')
            self.data_export(doctype_to_export=self._doctype_to_export,
                             dict_list_to_export=list_of_values_to_save,
                             pa_schema_to_export=data_schema)

        return something

    def search_engine(self, some_parameter):
        list_results_to_parse = []

        try:

            print('searching: ', some_parameter)
            parameter_url = some_parameter['parameter']
            response = requests.get(parameter_url)
            print('status_code: ', response.status_code)
            soup = BeautifulSoup(response.text, 'html.parser')

            all_cards = soup.find_all('div', {'class': "col-sm-4 col-lg-4 col-md-4"})
            for item in all_cards:
                list_results_to_parse.append(str(item))

        except:
            print(traceback.format_exc())

        time.sleep(random.uniform(1, 2))
        return list_results_to_parse

    def parse_documents(self, current_parameter, document_to_parse):
        """
        Parsing Json function.
        :param document_to_parse:
        :type current_parameter: object
        :return: parsed JSON document to database.
        """
        allow_to_continue_parsing = True
        try:
            # Do something

            if not allow_to_continue_parsing:
                return None
            else:

                parsed_id = None
                parsed_title = None
                parsed_description = None
                parsed_reviews = None
                parsed_price = None
                parsed_url = None
                parsed_image_url = None
                parsed_stars = None

                # Each document is soup type
                soup = BeautifulSoup(document_to_parse, 'html.parser')
                try:
                    info_id_and_url = soup.find('a', {'class': 'title'}, href=True)
                    try:
                        parsed_id = str(info_id_and_url['href'].split('/')[-1])
                    except:
                        pass
                    try:
                        parsed_url = 'https://webscraper.io' + str(info_id_and_url['href'])
                    except:
                        pass
                    try:
                        parsed_title = str(info_id_and_url['title'])
                    except:
                        pass
                except:
                    pass

                try:
                    info_descp = soup.find('p', {'class': 'description'}).text
                    parsed_description = str(info_descp)
                except:
                    pass

                try:
                    info_ratings = soup.find('div', {'class': 'ratings'}).find('p', {'class': 'pull-right'}).text
                    parsed_reviews = int(str(info_ratings).split(' reviews')[0])
                except:
                    pass

                try:
                    info_stars = soup.find('div', {'class': 'ratings'}).find_all('p')
                    for item in info_stars:
                        try:
                            item_attrs = item.attrs
                            parsed_stars = item_attrs['data-rating']
                        except:
                            pass
                    parsed_stars = int(parsed_stars)
                except:
                    pass

                try:
                    info_price = soup.find('h4', {'class': 'pull-right price'}).text

                    parsed_price = float(str(info_price).split('$')[1])
                except:
                    pass

                try:
                    info_img = soup.find('img', {'class': 'img-responsive'})['src']
                    parsed_image_url = 'https://webscraper.io' + str(info_img)
                except:
                    pass

                doc = {
                    'id': parsed_id,
                    'title': parsed_title,
                    'description': parsed_description,
                    'reviews': parsed_reviews,
                    'stars': parsed_stars,
                    'price': parsed_price,
                    'url': parsed_url,
                    'image_url': parsed_image_url,
                    'collected_date': datetime.datetime.today().__str__(),
                    'source': 'scraping_test_ground'

                }
                return doc
        except BaseException:
            print(traceback.format_exc())
            if self._run_test:
                sys.exit()
            else:
                pass

            return None

    def data_export(self, doctype_to_export: str, dict_list_to_export: list, pa_schema_to_export: pa.schema):

        # some function to export to mongodb, sql or postgres...
        #
        #
        ####################################

        # Or just save to file

        rand_number = self.create_random_stringnum()
        userdir = Path(self._project_path).joinpath(f"{self._scraper_name}_{rand_number}.{self._doctype_to_export}")
        filename_ofc = str(f"{self._scraper_name}_{rand_number}.{self._doctype_to_export}")
        try:
            df_selected = pd.DataFrame(dict_list_to_export)
            df_columns = df_selected.columns.tolist()
            schema_columns = pa_schema_to_export.names
            for df_col in df_columns:
                if df_col not in schema_columns:
                    df_selected.pop(df_col)

            for df_col in schema_columns:
                if df_col not in df_columns:
                    df_selected[df_col] = None
            df_columns = df_selected.columns.tolist()

            for df_col in df_columns:

                if str(df_selected[df_col].dtype) == 'object':
                    dtype_from_df = 'string'
                elif str(df_selected[df_col].dtype) == 'str':
                    dtype_from_df = 'string'
                else:
                    dtype_from_df = str(df_selected[df_col].dtype)

                if dtype_from_df != str(pa_schema_to_export.field(str(df_col)).type):
                    if str(pa_schema_to_export.field(str(df_col)).type) == 'string':
                        df_selected[df_col] = df_selected[df_col].astype(str)

                    elif 'int' in str(pa_schema_to_export.field(str(df_col)).type):
                        df_selected[df_col] = df_selected[df_col].fillna(0)

                        df_selected[df_col] = df_selected[df_col].astype(
                            str(pa_schema_to_export.field(str(df_col)).type))

                    elif 'bool' in str(pa_schema_to_export.field(str(df_col)).type):
                        df_selected[df_col] = df_selected[df_col].astype(bool)

                    elif 'float' in str(pa_schema_to_export.field(str(df_col)).type):
                        df_selected[df_col] = df_selected[df_col].astype(float)

                    elif 'timestamp' in str(pa_schema_to_export.field(str(df_col)).type):
                        df_selected[df_col] = pd.to_datetime(df_selected[df_col])
                    # df['Type'] = df['Type'].str.replace('None', '')

                else:
                    pass

            df_selected = df_selected.replace(r'^None$', None, regex=True)
            pa_table_format = pa.table(data=df_selected, schema=pa_schema_to_export)

            if doctype_to_export == 'csv':
                pyacsv.write_csv(pa_table_format, userdir)
                print('saved file: ', userdir)
            if doctype_to_export == 'parquet':
                pyaparquet.write_table(pa_table_format, userdir)
                print('saved file: ', userdir)

            # some function to export to storage
            #
            #
            ####################################

        except:
            print(traceback.format_exc())

    @staticmethod
    def create_parameters():
        import pandas as pd
        df = pd.DataFrame([{'parameter': 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'},
                           {'parameter': 'https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets'}])

        df.to_parquet('scraper_parameters.parquet')

    def create_random_stringnum(self):
        import random
        o = ''
        for i in range(8):
            v = str(random.randrange(1, 9999))
            o += v
        return o
