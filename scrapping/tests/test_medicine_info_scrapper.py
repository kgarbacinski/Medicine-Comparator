from ..medicine_info_scrapper import main

def test_eol_separated_excipients_pdf_scrapper():
    url = 'https://rejestrymedyczne.ezdrowie.gov.pl/api/rpl/medicinal-products/43097/characteristic'
    excipients_test_set = {'Mannitol', 'Sorbitol', 'Kwas cytrynowy', 'Makrogol 6000', 'L-arginina', 'Magnezu stearynian'}
    scrapped_excipients = main(url)
    assert excipients_test_set == scrapped_excipients

def test_coma_separated_excipients_pdf_scrapper():
    url = 'https://rejestrymedyczne.ezdrowie.gov.pl/api/rpl/medicinal-products/786/characteristic'
    excipients_test_set = {'Celuloza sproszkowana', 'Skrobia kukurydziana', 'Skład otoczki: Kopolimer kwasu metakrylowego i akrylan metylu', 'Polisorbat 80', 'Sodu laurylosiarczan', 'Talk', 'Cytrynian trójetylowy.'}
    scrapped_excipients = main(url)
    assert excipients_test_set == scrapped_excipients

def test_one_excipient_pdf_scrapper():
    url = 'https://rejestrymedyczne.ezdrowie.gov.pl/api/rpl/medicinal-products/36832/characteristic'
    excipients_test_set = {'Woda do wstrzykiwań'}
    scrapped_excipients = main(url)
    assert excipients_test_set == scrapped_excipients



def test_two_pages_excipients_pdf_scrapper():
    url = 'https://rejestrymedyczne.ezdrowie.gov.pl/api/rpl/medicinal-products/22440/characteristic'
    excipients_test_set = {'Proszek:', 'trometamol', 'sacharoza', 'kwas solny stężony (do ustalenia pH)',
                           'Rozpuszczalnik:', 'sodu chlorek', 'woda do wstrzykiwań'}
    scrapped_excipients = main(url)
    assert excipients_test_set == scrapped_excipients