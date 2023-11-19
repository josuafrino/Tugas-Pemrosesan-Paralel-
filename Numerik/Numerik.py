from mpi4py import MPI
import time
import numpy as np

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        # Use predefined data
        data = np.array([11,12,22,25,34,64,90])

        # Membagi data menjadi dua bagian untuk worker1 dan worker2
        mid = len(data) // 2
        data1 = data[:mid]
        data2 = data[mid:]

        # Mengirim data ke worker1 dan worker2
        comm.send(data1, dest=1)
        comm.send(data2, dest=2)

        # Menerima jumlah lokal dari worker1 dan worker2
        local_sum1 = comm.recv(source=1)
        local_sum2 = comm.recv(source=2)

        # Menghitung jumlah total
        total_sum = local_sum1 + local_sum2
        print("Total hasil perhitungan:", total_sum)

    elif rank == 1:
        # Worker1
        data = comm.recv(source=0)
        local_sum = np.sum(data)
        comm.send(local_sum, dest=0)

    elif rank == 2:
        # Worker2
        data = comm.recv(source=0)
        local_sum = np.sum(data)
        comm.send(local_sum, dest=0)

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print("Waktu dikerjakan", end - start)
