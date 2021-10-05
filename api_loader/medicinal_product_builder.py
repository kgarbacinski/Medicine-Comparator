import re


class MedicinalProductBuilder:

    def __init__(self, product):
        self.id = product['id']
        self.name = product['medicinalProductName'] #
        self.ean = self.get_ean(product['gtin'])
        self.product_power_original = product['medicinalProductPower']
        self.content_length = 0
        self.pharmaceutical_form = product['pharmaceuticalFormName'] #
        self.active_substances = self.get_active_substances(product['commonName'], ' + ')
        self.active_substances_data = self.collect_active_substances_data(product['medicinalProductPower'])

    def get_ean(self, gtins):
        gtins_codes = gtins.split('\\n')
        final_codes = []
        for code in gtins_codes:
            if code != '':
                final_codes.append(int(code))
        return final_codes

    def get_active_substances(self, active_substances, splitter):
        exceptions = ['Mg2+', 'Ca2+', 'H+']
        for exception in exceptions:
            if exception in active_substances:
                active_substances = active_substances.replace(exception, '')
        act_substances = active_substances.split(splitter)
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
        else:
            return self.extract_plus_separated_data(product_power_descryption)

    def extract_parentheses_data(self, product_power_descryption):
        if not ')' in product_power_descryption:
            product_power_descryption = product_power_descryption.replace('/', ')/')
        parentheses_groups = re.search(r'^\((.*)\) ?\/((\d*\.*\,*\d*) *(.*))', product_power_descryption)
        parentheses = parentheses_groups.group(1)
        parentheses = parentheses.replace('(', '')
        parentheses = parentheses.replace(')', '')

        parentheses_power = parentheses_groups.group(3)
        if parentheses_power == '': parentheses_power = '1'
        parentheses_power = parentheses_power.replace(',', '.')
        parentheses_power = float(parentheses_power)
        parentheses_unit = parentheses_groups.group(4)
        if len(self.active_substances) == parentheses.count(' + ') + 1:
            parentheses_elements = parentheses.split('+')
            elements = []
            for i, element in enumerate(parentheses_elements):
                if i < len(self.active_substances):
                    element = element.strip()
                    e = self.divide_concentrations_and_units(self.active_substances[i], element)
                    power = float(e[self.active_substances[i]]['power'])/parentheses_power
                    unit = f"{e[self.active_substances[i]]['unit']}/{parentheses_unit}"
                    elements.append(f'{power} {unit}')
            return elements



    def extract_plus_separated_data(self, product_power_descryption):
        return product_power_descryption.split(' + ')


    def divide_concentrations_and_units(self, substance, single_pair):
        concentrations_and_units = {}
        if '%' in single_pair: single_pair = single_pair.replace('%', ' %')
        if ' ' in single_pair: single_pair = single_pair.replace(' ', ' ')
        if single_pair and single_pair[0].isdigit():
            concentration = re.search(r'(^\d*\,*\.*\d*) *(\%*\w+\/*\w* ?\w*) *', single_pair).group(1)
            concentration = concentration.replace(',', '.')
            unit = re.search(r'(^\d*\,*\.*\d*) *(\%*\w+\/*\w* ?\w*) *', single_pair).group(2)
            try:
                concentrations_and_units.update({substance: {'power': float(concentration), 'unit': unit}})
            except:
                concentrations_and_units.update({substance: {'power': concentration, 'unit': unit}})
            return concentrations_and_units
        concentrations_and_units.update({substance: {'power': single_pair, 'unit': ''}})
        return concentrations_and_units
