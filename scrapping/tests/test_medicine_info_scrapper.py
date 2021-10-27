from ..medicine_info_scrapper import pdf_scrapper

def test_eol_separated_excipients_pdf_scrapper():
    url = 'https://rejestrymedyczne.ezdrowie.gov.pl/api/rpl/medicinal-products/43097/characteristic'
    excipients_test_set = {'mannitol', 'sorbitol', 'kwas cytrynowy', 'makrogol 6000', 'l-arginina', 'magnezu stearynian'}
    scrapped_excipients = pdf_scrapper(url)
    assert excipients_test_set == scrapped_excipients

def test_coma_separated_excipients_pdf_scrapper():
    url = 'https://rejestrymedyczne.ezdrowie.gov.pl/api/rpl/medicinal-products/786/characteristic'
    excipients_test_set = {'celuloza sproszkowana', 'skrobia kukurydziana',
                           'skład otoczki: kopolimer kwasu metakrylowego i akrylan metylu', 'polisorbat 80',
                           'sodu laurylosiarczan', 'talk', 'cytrynian trójetylowy'}
    scrapped_excipients = pdf_scrapper(url)
    assert excipients_test_set == scrapped_excipients

def test_one_excipient_pdf_scrapper():
    url = 'https://rejestrymedyczne.ezdrowie.gov.pl/api/rpl/medicinal-products/36832/characteristic'
    excipients_test_set = {'woda do wstrzykiwań'}
    scrapped_excipients = pdf_scrapper(url)
    assert excipients_test_set == scrapped_excipients



def test_two_pages_excipients_pdf_scrapper():
    url = 'https://rejestrymedyczne.ezdrowie.gov.pl/api/rpl/medicinal-products/22440/characteristic'
    excipients_test_set = {'proszek:', 'trometamol', 'sacharoza', 'kwas solny stężony (do ustalenia ph)',
                           'rozpuszczalnik:', 'sodu chlorek', 'woda do wstrzykiwań'}
    scrapped_excipients = pdf_scrapper(url)
    assert excipients_test_set == scrapped_excipients