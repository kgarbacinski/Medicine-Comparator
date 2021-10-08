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
                    print(self.name, self.active_substances[i])
                    try:
                        power = float(e[self.active_substances[i]]['power'])/parentheses_power
                        unit = f"{e[self.active_substances[i]]['unit']}/{parentheses_unit}"
                    except:
                        power = e[self.active_substances[i]]['power']
                        unit = e[self.active_substances[i]]['unit']
                    elements.append(f'{power} {unit.split(" ")[0]}')
                    print(f'{power} {unit.split(" ")[0]}')
            return elements



    def extract_plus_separated_data(self, product_power_descryption):
        return product_power_descryption.split(' + ')


    def divide_concentrations_and_units(self, substance, primary_pair):
        concentrations_and_units = {}
        if '%' in primary_pair: primary_pair = primary_pair.replace('%', ' %')
        if ' ' in primary_pair: primary_pair = primary_pair.replace(' ', ' ')
        if primary_pair and primary_pair[0].isdigit():
            groups = re.search(r'^(\d[\d* ?\,?\.?\-?x?\^?]*) *((\%*[\w+\.?]*)\/?([\d* ?\,?\.?]*)(\w* ?\w*))', primary_pair)
            concentration = groups.group(1).replace(',', '.').replace(' ', '')
            unit = groups.group(2)
            unit_1 = groups.group(3).replace(' ', '')
            divider = groups.group(4).replace(',', '.').replace(' ', '')
            divider_unit = groups.group(5).strip()
            if divider and divider[0].isdigit():
                concentrations_and_units.update({substance: {'power': float(concentration) / float(divider),
                                                             'unit': f'{unit_1}/{divider_unit}'}})
                return concentrations_and_units
            concentrations_and_units.update({substance: {'power': concentration, 'unit': unit}})
            return concentrations_and_units
        concentrations_and_units.update({substance: {'power': primary_pair, 'unit': ''}})
        return concentrations_and_units
