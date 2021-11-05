import re
from .regex_patterns import RegexPatterns


class MedicinalProductBuilder:

    def __init__(self, product):
        self.product = product
        self.id = self.product['id']
        self.name = self.get_name()
        self.ean = self.get_ean()
        # self.product_power_original = self.product['medicinalProductPower']
        self.content_length = 0
        self.pharmaceutical_form = self.product['pharmaceuticalFormName']
        self.active_substances = self.get_active_substances()
        self.active_substances_data = self.collect_active_substances_data()

    def get_name(self):
        if self.product['medicinalProductPower'] in self.product['medicinalProductName']:
            return self.product['medicinalProductName']
        return f"{self.product['medicinalProductName']} {self.product['medicinalProductPower']}"

    def get_ean(self) -> list:
        gtins_codes = self.product['gtin'].split('\\n')
        final_codes = []
        for code in gtins_codes:
            if code != '':
                final_codes.append(int(code))
        return final_codes

    def get_active_substances(self) -> list:
        exceptions = ['Mg2+', 'Ca2+', 'H+']
        for exception in exceptions:
            if exception in self.product['commonName']:
                active_substances = self.product['commonName'].replace(exception, '')
        act_substances = self.product['commonName'].split('+')
        active_substances_list = []
        for substance in act_substances:
            if substance != '':
                active_substances_list.append(substance.strip().lower())
        return active_substances_list

    def collect_active_substances_data(self) -> dict:
        if len(self.active_substances) == 1:
            return self.divide_concentrations_and_units(self.active_substances[0],
                                                        self.product['medicinalProductPower'])
        else:
            elements = self.divide_elements()
            active_substances = {}
            try:
                for i, element in enumerate(elements):
                    active_substances.update(self.divide_concentrations_and_units(self.active_substances[i], element))
            except:
                pass
            return active_substances

    def divide_elements(self) -> list:
        if self.product['medicinalProductPower'].startswith('('):
            return self.extract_brackets_data()
        return self.extract_plus_separated_data()

    def extract_brackets_data(self) -> list:
        brackets = self.get_brackets_details()

        if len(self.active_substances) == brackets['brackets'].count('+') + 1:
            return self.get_primary_pairs(brackets, '+')
        elif len(self.active_substances) == brackets['brackets'].count(' + ') + 1:
            return self.get_primary_pairs(brackets, ' + ')
        else:
            print(self.id, self.name)

    def get_brackets_details(self) -> dict:
        brackets, power, unit = self.__get_brackets_params()
        return self.__validate_brackets_elems(brackets, power, unit)

    def __get_validated_product_power(self) -> str:
        if ')' not in self.product['medicinalProductPower']:
            return self.product['medicinalProductPower'].replace('/', ')/')
        return self.product['medicinalProductPower']

    def __get_brackets_params(self) -> tuple:
        brackets_groups = re.search(RegexPatterns.brackets_regex.value, self.__get_validated_product_power())
        brackets = brackets_groups.group(1).replace('(', '').replace(')', '')
        power = brackets_groups.group(3)
        unit = brackets_groups.group(4)
        return brackets, power, unit

    def __validate_brackets_elems(self, brackets, power, unit) -> dict:
        if power == '': power = '1'
        power = float(power.replace(',', '.'))
        return {'brackets': brackets, 'power': power, 'unit': unit}

    def get_primary_pairs(self, brackets, splitter) -> list:
        brackets_elements = brackets['brackets'].split(splitter)
        return self.__get_primary_pairs(brackets_elements, brackets)

    def __get_primary_pairs(self, brackets_elements, brackets) -> list:
        primary_pairs = []
        for i, element in enumerate(brackets_elements):
            if i < len(self.active_substances):
                element = element.strip()
                e = self.divide_concentrations_and_units(self.active_substances[i], element)
                try:
                    power = float(e[self.active_substances[i]]['power']) / brackets['power']
                    unit = f"{e[self.active_substances[i]]['unit']}/{brackets['unit']}"
                except:
                    power = e[self.active_substances[i]]['power']
                    unit = e[self.active_substances[i]]['unit']
                primary_pairs.append(f'{power} {unit.split(" ")[0]}')
        return primary_pairs

    def extract_plus_separated_data(self) -> list:
        if len(self.active_substances) == len(self.product['medicinalProductPower'].split(' + ')):
            return self.product['medicinalProductPower'].split(' + ')
        elif len(self.active_substances) == len(self.product['medicinalProductPower'].split('+')):
            return self.product['medicinalProductPower'].split('+')
        else:
            return [self.product['medicinalProductPower']] * len(self.active_substances)

    def change_decimal_separator(self, primary_pair, separator_to_change=',', new_sparator='.') -> str:
        if separator_to_change in primary_pair:
            for char in primary_pair[1:]:
                if char == separator_to_change and \
                        primary_pair[primary_pair.index(char) - 1].isdigit() and \
                        primary_pair[primary_pair.index(char) + 1].isdigit():
                    return primary_pair.replace(char, new_sparator)
        return primary_pair

    def prepare_primary_pair_details(self, primary_pair) -> dict:
        groups = re.search(RegexPatterns.primary_pair_regex.value, self.__get_validated_primary_pair(primary_pair))
        return self.__validate_primary_pair_elems(groups)

    def __validate_primary_pair_elems(self, groups) -> dict:
        concentration = groups.group(1).replace(' ', '')
        if groups.group(7):
            unit = groups.group(7).replace(' ', '')
            divider = '1'
            divider_unit = ''
        else:
            unit = groups.group(3).replace(' ', '')
            divider = groups.group(5).replace(' ', '')
            if divider == '':
                divider = '1'
            divider_unit = f'/{groups.group(6).strip()}'
        return {'concentration': concentration, 'divider': divider, 'unit': unit, 'divider_unit': divider_unit}

    def __get_validated_primary_pair(self, primary_pair) -> str:
        primary_pair = primary_pair.replace('%', ' %').replace(' ', ' ').replace('–', '-')
        primary_pair = self.change_decimal_separator(primary_pair)
        return primary_pair

    def divide_concentrations_and_units(self, substance, primary_pair) -> dict:
        concentrations_and_units = {}
        if primary_pair and primary_pair[0].isdigit():
            primary_pair_details = self.prepare_primary_pair_details(primary_pair)
            try:
                concentrations_and_units.update(
                    {substance:
                         {'power': float(primary_pair_details['concentration']) / float(
                             primary_pair_details['divider']),
                          'unit': f'{primary_pair_details["unit"]}{primary_pair_details["divider_unit"]}'}})
            except:
                concentrations_and_units.update(
                    {substance: {'power': primary_pair_details['concentration'],
                                 'unit': f'{primary_pair_details["unit"]}{primary_pair_details["divider_unit"]}'}})
            return concentrations_and_units
        concentrations_and_units.update({substance: {'power': primary_pair, 'unit': ''}})
        return concentrations_and_units
