from medicines_app.equivs_api.medicinal_product import MedicinalProduct

# ref_med = MedicinalProduct(8572) # Luminal
ref_med = MedicinalProduct(5149) # Paracetamol


print(f'''
TO JEST LEK ODNIESIENIA:
########################################
{ref_med.name}
{ref_med.form} {ref_med.description}
''')
for excipent in ref_med.get_excipents():
    print(excipent)
print('########################################')

print(f'''
A TO SĄ ZAMIENNIKI''')
for equivalent in ref_med.get_equivalents():
    print(f'''++++++++++++++++++++++++++++++++++++++++
{equivalent.name}
{equivalent.form} {equivalent.description}
''')
    for excipent in equivalent.get_excipents():
        print(excipent)
