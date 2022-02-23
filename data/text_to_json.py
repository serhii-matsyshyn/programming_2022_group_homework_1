""" Module to convert text to json objects """

import json
import re
from logging import debug, info, warning
from logging import DEBUG, getLogger

getLogger().setLevel(DEBUG)


class TextToJsonConverter:
    """ Convert text to json objects """

    def __init__(self, source_text_path: str, save_json_path: str):
        self.source_text_path = source_text_path
        self.save_json_path = save_json_path

        self.lines = self.lines_read(self.source_text_path)
        self.header = self.parse_header()

        self.json_results = []

    def lines_read(self, file_name: str) -> list:
        """ Gets list of lines from file

        :param file_name: name of file
        :type file_name: str
        :return: list of lines from file
        :rtype: list
        """

        with open(file_name, "r", encoding='utf-8') as file:
            all_lines = [line.rstrip() for line in file.readlines()]
        return all_lines

    def save_json(self):
        """ Save json_results to json file """
        with open(self.save_json_path, "w", encoding='utf-8') as file:
            json.dump(self.json_results, file, ensure_ascii=False, indent=4)

        info(f'Saved to {self.save_json_path}')

    def parse_lines(self):
        """ Go through lines and parse them if empty one detected """
        info('Started parsing...')
        line_accurate = ''

        for line in self.lines[6:]:
            if line == '':
                self.parse_line(line_accurate)
                line_accurate = ''
            else:
                line_accurate += line

    def parse_header(self):
        """ Parse header """
        return {
            "протопресвітерат": re.match(r'\(([^\s]*).*\)', self.lines[1]).group(1),
            "деканат": re.match(r"\d*\. ([^\s]*).*\.", self.lines[0]).group(1)
        }

    def parse_line(self, line):
        """ Main parsing of the line """
        debug(f"Got such a line: {line}")

        if re.match(r'^\d+\)', line):
            self.json_results.append(
                {
                    "протопресвітерат": self.header["протопресвітерат"],
                    "деканат": self.header["деканат"],
                    "населений пункт": {
                        "назва": None,
                        "location": {
                            "lat": None,
                            "lng": None
                        }
                    }
                }
            )

        elif line.startswith('Надає: '):
            self.json_results.append(
                {"надає": {
                    "тип": None,
                    "назва": line.replace('Надає: ', '').replace('.', '')}
                }
            )

        elif line.startswith('Парох:  '):
            self.json_results.append(
                {}  # TODO: parse all lines
            )

        else:
            warning('Not parsed')
            return False

        debug(f"Parsed to a json ok.")
        return True


if __name__ == '__main__':
    text_to_json_converter = TextToJsonConverter('text/final_text/Lvivskyi.txt',
                                                 'json/Lvivskyi.json')

    text_to_json_converter.parse_lines()
    text_to_json_converter.save_json()
