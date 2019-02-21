import csv
import re


class Normalizer(object):

    def __init__(self):
        self.sections = {}
        self.section_names = set()

        self.numbers_regex = re.compile('\d+')
        self.words_regex = re.compile('[a-zA-Z]+')

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
                section_id = int(entry['section_id'])
                section_name = entry['section_name'].lower()

                row_id = entry.get('row_id', None)
                if row_id:
                    row_id = int(row_id)

                row_name = entry.get('row_name', None)
                if row_name:
                    row_name = row_name.lower()

                if section_name in self.sections:
                    self.sections[section_name]['rows'].append((row_id, row_name))
                else:
                    self.sections[section_name] = {
                        'id': section_id,
                        'rows': [(row_id, row_name)] if row_id is not None else [],
                    }
                    self.section_names.add(section_name)

    @staticmethod
    def is_subsequence(sequence, string):
        sequence_index = 0
        string_index = 0

        while sequence_index < len(sequence) and string_index < len(string):
            if sequence[sequence_index] == string[string_index]:
                sequence_index += 1

            string_index += 1

        return sequence_index == len(sequence)

    def get_sections_matching_numbers(self, section_name):
        numbers = self.numbers_regex.findall(section_name)

        # Return all sections if there aren't any numbers to match.
        if not numbers:
            return self.section_names

        matching_sections = []
        for section in self.section_names:
            for number in numbers:
                if re.search('([^0-9]|^){}([^0-9]|$)'.format(number), section):
                    matching_sections.append(section)

        return set(matching_sections)

    def get_sections_matching_words(self, section_name):
        words = self.words_regex.findall(section_name)

        # Return all sections if there aren't any words to match.
        if not words:
            return self.section_names

        matching_sections = []
        for section in self.section_names:
            for word in words:
                if re.search(word, section):
                    matching_sections.append(section)

        return set(matching_sections)

    def get_sections_matching_subsequences(self, section_name):
        subsequences = self.words_regex.findall(section_name)

        # Return all sections if there aren't any subsequences to match.
        if not subsequences:
            return self.section_names

        matching_sections = []
        for section in self.section_names:
            for subsequence in subsequences:
                if self.is_subsequence(subsequence, section):
                    matching_sections.append(section)

        return set(matching_sections)

    def get_sections_matching_name(self, section):
        # Get sections that match a number in the inputted section name.
        sections_matching_numbers = self.get_sections_matching_numbers(section)

        # Get sections that match a word in the inputted section name.
        sections_matching_words = self.get_sections_matching_words(section)

        # Get sections that match a subsequence of the inputted section name.
        sections_matching_subsequences = self.get_sections_matching_subsequences(section)

        sections_with_multiple_matches = list(sections_matching_numbers & (sections_matching_words | sections_matching_subsequences))
        sections_with_any_matches = list(sections_matching_numbers | sections_matching_words | sections_matching_subsequences)

        return sections_with_multiple_matches or sections_with_any_matches

    def get_sections_with_matching_row(self, sections, row):
        if '-' in row:
            return [{
                'section': section,
                'row_id': None,
            } for section in sections]

        matches = []

        for section in sections:
            for row_id, row_name in self.sections[section]['rows']:
                if row_name == row:
                    matches.append({
                        'section': section,
                        'row_id': row_id,
                    })

        return matches

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

        row = row.lstrip('0') if row != '0' else row

        # Get sections that match with this section name.
        candidate_sections = self.get_sections_matching_name(section.lower())

        # Filter out sections that don't have a matching row name.
        matches = self.get_sections_with_matching_row(candidate_sections, row.lower())

        matched_section_id = None
        matched_row_id = None

        # Return the match if it exists.
        if len(matches) == 1:
            matched_section = matches[0]['section']
            matched_section_id = self.sections[matched_section]['id']
            matched_row_id = matches[0]['row_id']
        elif len(candidate_sections) == 1:
            matched_section = candidate_sections[0]
            matched_section_id = self.sections[matched_section]['id']

        return (matched_section_id, matched_row_id, matched_row_id is not None)
