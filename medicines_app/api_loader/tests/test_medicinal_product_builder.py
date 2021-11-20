from medicines_app.api_loader.medicinal_product_builder import MedicinalProductBuilder


class Tests:

    @property
    def product(self):
        product = {'id': '10174',
                   'count': '1',
                   'medicinalProductName': '0,9% Sodium Chloride-BRAUN',
                   'commonName': 'Natrii chloridum',
                   'medicinalProductPower': '9 mg/ml',
                   'pharmaceuticalFormName': 'Roztwór do infuzji',
                   'registryNumber': '08754',
                   'expirationDateString': 'Bezterminowe',
                   'subjectMedicinalProductName': 'B. Braun Melsungen AG',
                   'procedureTypeName': 'NAR',
                   'specimenType': 'Ludzki',
                   'activeSubstanceName': 'Natrii chloridum',
                   'atcCode': 'B05CB01',
                   'gracePeriod': '',
                   'characteristicFileName': True,
                   'leafletFileName': True,
                   'packageFileName': True,
                   'parallelImportLeafletFileName': False,
                   'parallelImportPackageMarkingFileName': False,
                   'parallelImportAdditionalDocumentOneFileName': False,
                   'parallelImportAdditionalDocumentTwoFileName': False,
                   'decisionsAttachment': False,
                   'evaluationReport': '-',
                   'reportSummary': '-',
                   'rmpSummary': '-',
                   'targetSpecies': '',
                   'packaging': '6 butelek 1000 ml\\n20 poj. 100 ml\\n10 poj. 1000 ml\\n10 butelek 100 ml\\n10 poj. 250 ml\\n10 poj. 500 ml\\n10 butelek 500 ml',
                   'distributor': '\\n\\n\\n\\n\\n\\n',
                   'euNumber': '\\n\\n\\n\\n\\n\\n',
                   'accessibilityCategory': 'Rp\\nRp\\nRp\\nRp\\nRp\\nRp\\nRp',
                   'gtin': '05909990875450\\n05909990336142\\n05909990875429\\n05909990875436\\n05909990875474\\n05909990875467\\n05909990875443',
                   'parallelPackaging': '',
                   'parallelDistributor': '',
                   'parallelEuNumber': '',
                   'parallelAccessibilityCategory': '',
                   'parallelGtin': '',
                   'deletedPackaging': '10 poj. 100 ml',
                   'deletedDistributor': '',
                   'deletedEuNumber': '',
                   'deletedAccessibilityCategory': 'LzRp',
                   'deletedGtin': '05909990875412'}
        return MedicinalProductBuilder(product)

    @property
    def brackets_product(self):
        brackets_description = {'id': '205', 'count': '24', 'medicinalProductName': 'ABE', 'commonName': 'Acidum lacticum + Acidum salicylicum', 'medicinalProductPower': '(89 mg + 89 mg)/g', 'pharmaceuticalFormName': 'Płyn na skórę', 'registryNumber': '00409', 'expirationDateString': 'Bezterminowe', 'subjectMedicinalProductName': 'Grupa Inco S.A.', 'procedureTypeName': 'NAR', 'specimenType': 'Ludzki', 'activeSubstanceName': 'Acidum lacticum + Acidum salicylicum', 'atcCode': '', 'gracePeriod': '', 'characteristicFileName': True, 'leafletFileName': True, 'packageFileName': True, 'parallelImportLeafletFileName': False, 'parallelImportPackageMarkingFileName': False, 'parallelImportAdditionalDocumentOneFileName': False, 'parallelImportAdditionalDocumentTwoFileName': False, 'decisionsAttachment': False, 'targetSpecies': '', 'packaging': '1 op. 8 g', 'distributor': '', 'euNumber': '', 'accessibilityCategory': 'OTC', 'gtin': '05909990040919', 'parallelPackaging': '', 'parallelDistributor': '', 'parallelEuNumber': '', 'parallelAccessibilityCategory': '', 'parallelGtin': '', 'deletedPackaging': '30 op. 8 g', 'deletedDistributor': '', 'deletedEuNumber': '', 'deletedAccessibilityCategory': 'OTC', 'deletedGtin': '05909990625796'}
        return MedicinalProductBuilder(brackets_description)

    @property
    def plus_separated_product(self):
        plus_separated_description = {'id': '34249', 'count': '12', 'medicinalProductName': 'Abacavir + Lamivudine Accord', 'commonName': 'Abacavirum + Lamivudinum', 'medicinalProductPower': '600 mg + 300 mg', 'pharmaceuticalFormName': 'Tabletki powlekane', 'registryNumber': '23541', 'expirationDateString': '2021-11-15', 'subjectMedicinalProductName': 'Accord Healthcare Polska Sp. z o.o.', 'procedureTypeName': 'DCP', 'specimenType': 'Ludzki', 'activeSubstanceName': 'Abacaviri hydrochloridum + Lamivudinum', 'atcCode': 'J05AR02', 'gracePeriod': '', 'characteristicFileName': True, 'leafletFileName': True, 'packageFileName': True, 'parallelImportLeafletFileName': False, 'parallelImportPackageMarkingFileName': False, 'parallelImportAdditionalDocumentOneFileName': False, 'parallelImportAdditionalDocumentTwoFileName': False, 'decisionsAttachment': True, 'rmpSummary': 'StreszczenieRmp_34249_Iviverz.pdf', 'targetSpecies': '', 'packaging': '30 tabl.', 'distributor': '', 'euNumber': '', 'accessibilityCategory': 'Rpz', 'gtin': '05909991302498', 'parallelPackaging': '', 'parallelDistributor': '', 'parallelEuNumber': '', 'parallelAccessibilityCategory': '', 'parallelGtin': '', 'deletedPackaging': '', 'deletedDistributor': '', 'deletedEuNumber': '', 'deletedAccessibilityCategory': '', 'deletedGtin': ''}
        return MedicinalProductBuilder(plus_separated_description)

    def test_get_ean(self):
        ean_test_list = [5909990875450,
                         5909990336142,
                         5909990875429,
                         5909990875436,
                         5909990875474,
                         5909990875467,
                         5909990875443]
        assert ean_test_list == self.product.get_ean()

    def test_get_active_substances(self):
        active_substance_test = ['natrii chloridum']
        assert self.product.get_active_substances() == active_substance_test

    def test_collect_active_substances_data(self):
        active_substances_data_test = {'natrii chloridum': {'power': 9.0, 'unit': 'mg/ml'}}
        assert active_substances_data_test == self.product.collect_active_substances_data()

    def test_get_brackets_details(self):
        brackets = {'brackets': '89 mg + 89 mg', 'power': 1.0, 'unit': 'g'}
        assert brackets == self.brackets_product.get_brackets_details()

    def test_get_primary_pairs(self):
        brackets = {'brackets': '89 mg + 89 mg', 'power': 1.0, 'unit': 'g'}
        primary_pairs = ['89.0 mg/g', '89.0 mg/g']
        assert primary_pairs == self.brackets_product.get_primary_pairs(brackets, '+')

    def test_divide_brackets_elements(self):
        elements = ['89.0 mg/g', '89.0 mg/g']
        assert self.brackets_product.divide_elements() == elements

    def test_divide_non_brackets_elements(self):
        elements = ['600 mg', '300 mg']
        assert self.plus_separated_product.divide_elements() == elements

    def test_change_decimal_separator(self):
        primary_pair = '12,5 mg'
        changed_primary_pair = '12.5 mg'
        assert self.plus_separated_product.change_decimal_separator(primary_pair) == changed_primary_pair

    def test_prepare_primary_pair_details_when_unit_is_percent(self):
        primary_pair = '2%'
        primary_pair_details = {'concentration': '2', 'divider': '1', 'unit': '%', 'divider_unit': ''}
        assert primary_pair_details == self.product.prepare_primary_pair_details(primary_pair)

    def test_prepare_primary_pair_details_when_divider_is_not_1(self):
        primary_pair = '120 mg/5 ml'
        primary_pair_details = {'concentration': '120', 'divider': '5', 'unit': 'mg', 'divider_unit': '/ml'}
        assert primary_pair_details == self.product.prepare_primary_pair_details(primary_pair)

    def test_divide_concentrations_and_units(self):
        substance = 'Substance'
        primary_pair = '120 mg/5 ml'
        expected_output = {substance: {'power': 24.0, 'unit': 'mg/ml'}}
        assert expected_output == self.product.divide_concentrations_and_units(substance, primary_pair)