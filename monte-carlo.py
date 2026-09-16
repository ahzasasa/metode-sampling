import pandas as pd
import numpy as np

df = pd.read_csv('data.csv', sep=';')

col_waktu = 'waktu belajar'
col_kategori = 'cukup atau tidak'

# probabilitas
prob_kategori = df[col_kategori].value_counts(normalize=True)
kategori_labels = prob_kategori.index.tolist()
kategori_probs = prob_kategori.values.tolist()

# parameter statistik (mean, std)
stats_per_grup = df.groupby(col_kategori)[col_waktu].agg(['mean', 'std'])

# simulasi
n_simulasi = 85
np.random.seed(123)

# generate kategori
sim_kategori = np.random.choice(kategori_labels, size=n_simulasi, p=kategori_probs)
sim_waktu = []

# generate waktu belajar
for kat in sim_kategori:
    grup_mean = stats_per_grup.loc[kat, 'mean']
    grup_std = stats_per_grup.loc[kat, 'std']
    
    if pd.isna(grup_std):
        grup_std = 0

    waktu = np.random.normal(loc=grup_mean, scale=grup_std)
    
    waktu_kelipatan_5 = round(waktu / 5) * 5
    
    sim_waktu.append(max(0, int(waktu_kelipatan_5)))

# hasil
df_simulasi = pd.DataFrame({
    col_waktu: sim_waktu,
    col_kategori: sim_kategori
})

# simpan
output_filename = 'manipulasi.csv'

csv_string = df_simulasi.to_csv(sep=';', index=False, lineterminator='\n')

with open(output_filename, 'w', encoding='utf-8', newline='') as f:
    f.write(csv_string.strip())

print(f"File name: {output_filename}")
print("\nHasil Simulasi:")
print(df_simulasi[col_kategori].value_counts())