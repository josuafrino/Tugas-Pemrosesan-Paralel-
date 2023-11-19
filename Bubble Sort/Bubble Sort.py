from mpi4py import MPI
import time
import numpy as np

# Inisialisasi MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Data yang akan diurutkan
data = np.array([64, 34, 25, 12, 22, 11, 90])

if rank == 0:
    # Master
    start_time = time.time()
    print("Master memulai pengurutan...")

    # Membagi data menjadi dua bagian untuk worker1 dan worker2
    mid = len(data) // 2
    data1 = data[:mid]
    data2 = data[mid:]

    # Mengirim data ke worker1 dan worker2
    comm.send(data1, dest=1)
    comm.send(data2, dest=2)

    # Menerima data yang sudah diurutkan dari worker1 dan worker2
    sorted_data1 = comm.recv(source=1)
    sorted_data2 = comm.recv(source=2)

    # Menggabungkan dan mengurutkan data dari worker1 dan worker2
    sorted_data = np.sort(np.concatenate((sorted_data1, sorted_data2)))

    end_time = time.time()
    print("Data setelah diurutkan: ", sorted_data)
    print("Waktu eksekusi: ", end_time - start_time)

elif rank == 1:
    # Worker1
    data = comm.recv(source=0)
    print("Worker1 menerima data: ", data)

    # Melakukan bubble sort
    n = len(data)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if data[j] > data[j+1] :
                data[j], data[j+1] = data[j+1], data[j]

    print("Worker1 mengirim data yang sudah diurutkan: ", data)
    comm.send(data, dest=0)

elif rank == 2:
    # Worker2
    data = comm.recv(source=0)
    print("Worker2 menerima data: ", data)

    # Melakukan bubble sort
    n = len(data)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if data[j] > data[j+1] :
                data[j], data[j+1] = data[j+1], data[j]

    print("Worker2 mengirim data yang sudah diurutkan: ", data)
    comm.send(data, dest=0)
