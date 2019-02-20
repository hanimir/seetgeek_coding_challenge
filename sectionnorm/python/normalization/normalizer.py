import csv
import re

from collections import defaultdict


class Normalizer(object):

    def __init__(self):
        self.sections = {}

        self.number_regex = re.compile('\d+')
        self.word_regex = re.compile('[a-zA-Z]+')

    def read_manifest(self, manifest):
        """reads a manifest file

        manifest should be a CSV containing the following columns
            * section_id
            * section_name
            * row_id
            * row_name

        Arguments:
            manifest {[str]} -- /path/to/manifest
        """

        with open(manifest, 'rU') as manifest_file:
            csv_reader = csv.DictReader(manifest_file)
            for entry in csv_reader:
                section_id = entry['section_id']
                section_name = entry['section_name']
                row_id = entry.get('row_id', None)
                row_name = entry.get('row_name', None)
                if section_name in self.sections:
                    self.sections[section_name]['rows'].append((int(row_id), row_name))
                else:
                    self.sections[section_name] = {
                        'id': int(section_id),
                        'rows': [(int(row_id), row_name)] if row_id else [],
                    }

    def section_match(self, section_name, input_numbers, input_words):
        numbers = self.number_regex.findall(section_name)
        words = self.word_regex.findall(section_name)

        number_match = not set(numbers).isdisjoint(input_numbers)
        word_match = not set(words).isdisjoint(input_words)

        return word_match if len(numbers) == 0 else number_match

    def normalize(self, section, row):
        """normalize a single (section, row) input

        Given a (Section, Row) input, returns (section_id, row_id, valid)
        where
            section_id = int or None
            row_id = int or None
            valid = True or False

        Arguments:
            section {[type]} -- [description]
            row {[type]} -- [description]
        """

        section = section.lower()

        section_numbers = self.number_regex.findall(section)
        section_words = self.word_regex.findall(section)

        matching_sections = []
        for section_name in self.sections:
            if self.section_match(section_name, section_numbers, section_words):
                matching_sections.append(section_name)

        potential_matches = []
        for potential_section in matching_sections:
            rows_in_this_section = self.sections[potential_section]['rows']
            if rows_in_this_section:
                for row_id, row_name in rows_in_this_section:
                    if row_name == row:
                        potential_matches.append((self.sections[potential_section]['id'], row_id))
                        break

        import pdb; pdb.set_trace()

        if len(potential_matches) == 1:
            return (potential_matches[0][0], potential_matches[0][1], True)

        return (None, None, False)
