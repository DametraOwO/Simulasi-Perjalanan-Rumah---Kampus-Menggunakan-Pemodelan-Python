import numpy as np
import matplotlib.pyplot as plt

# Fungsi untuk simulasi berjalan kaki
def walk(distance, speed, start_time):
    time = distance / speed
    times = np.linspace(start_time, start_time + time, int(time * 10))
    distances = np.linspace(0, distance, int(time * 10))
    activities_walk = np.ones(len(times)) * 100  # Aktivitas berjalan kaki 100%
    activities_angkot = np.zeros(len(times))     # Tidak ada aktivitas angkot saat berjalan kaki
    return times, distances, activities_walk, activities_angkot

# Fungsi untuk simulasi angkot
def angkot(jarak_perjalanan, kecepatan, waktu_menunggu, perhentian, start_time):
    times = [start_time]
    distances = [0]
    activities_walk = [0]  # Tidak ada aktivitas berjalan kaki saat menunggu angkot
    activities_angkot = [0]  # Persentase 0% selama menunggu awal
    total_time = start_time + waktu_menunggu

    # Simulasi menunggu
    times.extend([total_time] * 10)
    distances.extend([distances[-1]] * 10)
    activities_walk.extend([0] * 10)   # Tidak ada aktivitas berjalan kaki
    activities_angkot.extend([0] * 10) # 0% saat angkot tidak bergerak
    
    for i, jarak in enumerate(jarak_perjalanan):
        # Angkot bergerak
        time_per_jarak = jarak / kecepatan
        total_time += time_per_jarak
        times.extend(np.linspace(total_time - time_per_jarak, total_time, int(time_per_jarak * 10)))
        distances.extend(np.linspace(distances[-1], distances[-1] + jarak, int(time_per_jarak * 10)))
        activities_walk.extend([0] * int(time_per_jarak * 10))    # Tidak ada aktivitas berjalan kaki
        activities_angkot.extend([100] * int(time_per_jarak * 10)) # 100% saat angkot bergerak

        # Menambah waktu berhenti di perhentian
        if i < len(perhentian):
            total_time += perhentian[i]
            times.extend([total_time] * 10)
            distances.extend([distances[-1]] * 10)
            activities_walk.extend([0] * 10)    # Tidak ada aktivitas berjalan kaki
            activities_angkot.extend([0] * 10)  # 0% saat angkot berhenti

    return times, distances, activities_walk, activities_angkot

# Parameter simulasi
jarak_total = 12.0  # km
kecepatan_jalan = 5 / 60  # km/menit (5 km/jam)
kecepatan_angkot = 25 / 60  # km/menit (25 km/jam)
waktu_menunggu = 10  # menit
perhentian = [1, 1, 1, 1]  # waktu berhenti dalam menit pada setiap perhentian
jarak_perjalanan_angkot = [1.9, 0.9, 1.7, 6.5, 1]  # jarak tempuh tiap segmen angkot dalam km

# Perjalanan awal dengan berjalan kaki sejauh 0.5 km
times_walk1, distances_walk1, activities_walk1, activities_angkot1 = walk(0.5, kecepatan_jalan, start_time=0)

# Perjalanan dengan angkot
start_time_angkot = times_walk1[-1]
times_angkot, distances_angkot, activities_walk_angkot, activities_angkot_angkot = angkot(
    jarak_perjalanan_angkot, kecepatan_angkot, waktu_menunggu, perhentian, start_time_angkot
)

# Perjalanan akhir dengan berjalan kaki sejauh 0.35 km
start_time_walk2 = times_angkot[-1]
times_walk2, distances_walk2, activities_walk2, activities_angkot2 = walk(0.35, kecepatan_jalan, start_time=start_time_walk2)

# Gabungkan hasil untuk grafik jarak tempuh
times_total = np.concatenate([times_walk1, times_angkot, times_walk2])
distances_total = np.concatenate([distances_walk1, distances_angkot + distances_walk1[-1], distances_walk2 + distances_walk1[-1] + distances_angkot[-1]])

# Gabungkan hasil untuk grafik aktivitas berjalan kaki dan angkot
activities_walk_total = np.concatenate([activities_walk1, activities_walk_angkot, activities_walk2])
activities_angkot_total = np.concatenate([activities_angkot1, activities_angkot_angkot, activities_angkot2])

# Plot hasil simulasi
plt.figure(figsize=(12, 10))

# Grafik jarak tempuh
plt.subplot(2, 1, 1)
plt.plot(times_total, distances_total, label="Jarak Tempuh (km)", color='blue')
plt.xlabel("Waktu (menit)")
plt.ylabel("Jarak dari Rumah (km)")
plt.title("Simulasi Perjalanan dari Rumah ke Kampus")
plt.legend()
plt.grid()

# Grafik aktivitas berjalan kaki dan angkot
plt.subplot(2, 1, 2)
plt.plot(times_total, activities_walk_total, label="Aktivitas Berjalan Kaki", color='green', linestyle='--')
plt.plot(times_total, activities_angkot_total, label="Aktivitas Naik Angkot", color='red')
plt.xlabel("Waktu (menit)")
plt.ylabel("Aktivitas (%)")
plt.title("Status Aktivitas Perjalanan")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
