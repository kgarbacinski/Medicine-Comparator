import re


class MedicinalProductBuilder:

    def __init__(self, product):
        self.id = product['id']
        self.name = product['medicinalProductName'] #
        self.ean = self.get_ean(product['gtin'])
        self.product_power_original = product['medicinalProductPower']
        self.content_length = 0
        self.pharmaceutical_form = product['pharmaceuticalFormName'] #
        self.active_substances = self.get_active_substances(product['commonName'])
        self.active_substances_data = self.collect_active_substances_data(product['medicinalProductPower'])

    def get_ean(self, gtins):
        gtins_codes = gtins.split('\\n')
        final_codes = []
        for code in gtins_codes:
            if code != '':
                final_codes.append(int(code))
        return final_codes

    def get_active_substances(self, active_substances):
        exceptions = ['Mg2+', 'Ca2+', 'H+']
        for exception in exceptions:
            if exception in active_substances:
                active_substances = active_substances.replace(exception, '')
        act_substances = active_substances.split(' + ')
        active_substances_list = []
        for substance in act_substances:
            if substance != '':
                active_substances_list.append(substance)
        return active_substances_list

    def collect_active_substances_data(self, product_power_descryption):
        if len(self.active_substances) == 1:
            return self.divide_concentrations_and_units(self.active_substances[0], product_power_descryption)
        else:
            elements = self.divide_elements(product_power_descryption)
            active_substances = {}
            try:
                for i, element in enumerate(elements):
                    active_substances.update(self.divide_concentrations_and_units(self.active_substances[i], element))
            except: pass
            return active_substances


    def divide_elements(self, product_power_descryption):
        if product_power_descryption.startswith('('):
            return self.extract_parentheses_data(product_power_descryption)
        return self.extract_plus_separated_data(product_power_descryption)

    def extract_parentheses_data(self, product_power_descryption):
        if not ')' in product_power_descryption:
            product_power_descryption = product_power_descryption.replace('/', ')/')
        parentheses_groups = re.search(r'^\((.*)\) ?\/((\d*\.*\,*\d*) *(.*))', product_power_descryption)
        parentheses = parentheses_groups.group(1).replace('(', '').replace(')', '')
        parentheses_power = parentheses_groups.group(3)
        if parentheses_power == '': parentheses_power = '1'
        parentheses_power = float(parentheses_power.replace(',', '.'))
        parentheses_unit = parentheses_groups.group(4)
        if len(self.active_substances) == parentheses.count(' + ') + 1:
            parentheses_elements = parentheses.split('+')
            elements = []
            for i, element in enumerate(parentheses_elements):
                if i < len(self.active_substances):
                    element = element.strip()
                    e = self.divide_concentrations_and_units(self.active_substances[i], element)
                    try:
                        power = float(e[self.active_substances[i]]['power'])/parentheses_power
                        unit = f"{e[self.active_substances[i]]['unit']}/{parentheses_unit}"
                    except:
                        power = e[self.active_substances[i]]['power']
                        unit = e[self.active_substances[i]]['unit']
                    elements.append(f'{power} {unit.split(" ")[0]}')
            return elements



    def extract_plus_separated_data(self, product_power_descryption):
        return product_power_descryption.split(' + ')

    def change_decimal_separator(self, primary_pair, separator_to_change=',', new_sparator='.'):
        if separator_to_change in primary_pair:
            for char in primary_pair[1:]:
                if char == separator_to_change and \
                        primary_pair[primary_pair.index(char) - 1].isdigit() and \
                        primary_pair[primary_pair.index(char) + 1].isdigit():
                    return primary_pair.replace(char, new_sparator)
        return primary_pair

    def prepare_primary_pair_details(self, primary_pair):
        primary_pair = primary_pair.replace('%', ' %').replace(' ', ' ').replace('–', '-')
        primary_pair = self.change_decimal_separator(primary_pair)
        groups = re.search(r'^(\d[\d\ \.\-x\^]*)(([\w\.]*)[\w\+\ \(\)\.]*\/(([\d\.]*)? ?([\w]*))|([\w\.\%]*))?',
                           primary_pair)
        concentration = groups.group(1).replace(' ', '')
        if groups.group(7):
            unit = groups.group(7).replace(' ', '')
            divider = 1
            divider_unit = ''
        else:
            unit = groups.group(3).replace(' ', '')
            divider = groups.group(5).replace(' ', '')
            if divider == '':
                divider = 1
            divider_unit = f'/{groups.group(6).strip()}'
        return {'concentration': concentration, 'divider': divider, 'unit': unit, 'divider_unit': divider_unit}

    def divide_concentrations_and_units(self, substance, primary_pair):
        concentrations_and_units = {}
        if primary_pair and primary_pair[0].isdigit():
            primary_pair_details = self.prepare_primary_pair_details(primary_pair)
            try:
                concentrations_and_units.update(
                    {substance:
                         {'power': float(primary_pair_details['concentration']) / float(primary_pair_details['divider']),
                          'unit': f'{primary_pair_details["unit"]}{primary_pair_details["divider_unit"]}'}})
            except:
                concentrations_and_units.update(
                    {substance: {'power': primary_pair_details['concentration'],
                                 'unit': f'{primary_pair_details["unit"]}{primary_pair_details["divider_unit"]}'}})
            return concentrations_and_units
        concentrations_and_units.update({substance: {'power': primary_pair, 'unit': ''}})
        return concentrations_and_units
