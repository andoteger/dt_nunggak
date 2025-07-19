import pandas as pd
import json

# Baca data dengan dtype yang ditentukan
data1 = pd.read_excel(
    'asset/DT_NUNGGAK.xlsx',
    dtype={
        'MDLBRCO': str,
        'MDLDLRF': str,
        'CSWREFN': str,
        'NOREK_SIMP': str,
        'KD_ANALIS': str,
        'MDLSCLS': str,
    },
    engine='openpyxl'
)

data2 = pd.read_excel(
    'asset/PENABUNG.xlsx',
    dtype={
        'CSWREFN': str,
        'ACTACCU': str,
    },
    engine='openpyxl'
)

# Gabungkan data dan pastikan ACTACCU adalah string
merged_data = pd.merge(
    data1,
    data2[['CSWREFN', 'ACTACCU']],
    on='CSWREFN',
    how='left'
).fillna({'ACTACCU': "kosong"})  # Handle NaN untuk ACTACCU

# Konversi ke JSON (otomatis handle NaN sebagai null)
result = merged_data.to_dict('records')

# Simpan ke file JSON
with open('asset/hasil_gabungan.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print("Data berhasil digabungkan dan disimpan dalam hasil_gabungan.json")