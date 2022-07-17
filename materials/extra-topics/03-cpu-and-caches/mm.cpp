#include <chrono>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <random>

#ifdef GEM5
#include <gem5/m5ops.h>
#endif

using namespace std;


void serial_multiply(double **A, double **B, double **C, int size)
{
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            for (int k = 0; k < size; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

template <int BLOCK_SIZE>
void blocked_multiply(double **A, double **B, double **C, int size)
{
    for (int bi = 0; bi < size; bi += BLOCK_SIZE) {
        for (int bk = 0; bk < size; bk += BLOCK_SIZE) {
            for (int i = bi; i <  min(size, bi + BLOCK_SIZE); i++) {
                for (int k = bk; k <  min(size, bk + BLOCK_SIZE); k++) {
                    for (int j = 0; j < size; j++) {
                        C[i][j] += A[i][k] * B[k][j];
                    }
                }
            }
        }
    }
}

void multiply(double **A, double **B, double **C, int size)
{
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            for (int k = 0; k < size; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

void const printMatrix(double **A, int size)
{
    for (int i=0; i<size; i++) {
        for (int j=0; j<size; j++) {
            cout << setprecision(3) << setw(8) << A[i][j] << "  ";
        }
        cout << endl;
    }
}

bool const verify(double **A, double **B, int size)
{
    for (int i=0; i<size; i++) {
        for (int j=0; j<size; j++) {
            if (abs(A[i][j] - B[i][j]) > 0.001) {
                return false;
            }
        }
    }
    return true;
}

void print_usage()
{
    cout << "Usage: mm size <blocksize>" << endl;
    cout << "Supported blocksizes:" << endl;
    cout << "0 => not blocked (default)" << endl;
    cout << "1 => 4x4" << endl;
    cout << "2 => 8x8" << endl;
    cout << "3 => 16x16" << endl;
    cout << "4 => 64x64" << endl;
}

int main(int argc, char *argv[])
{

    if (argc != 2 && argc != 3) {
        print_usage();
        return 1;
    }

    int size = atoi(argv[1]);

    if (size <= 0) {
        cout << "Invalid size" << endl;
        print_usage();
        return 2;
    }

    int blocksize = 0;
    if (argc == 3) {
        blocksize = atoi(argv[2]);
    }

    if (blocksize < 0 || blocksize > 4) {
        cout << "Invalid blocksize: " << blocksize << endl;
        print_usage();
        return 3;
    }

    cout << "Initalizing the matrices...";

    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(0, 1);

    double *dataA = new double[size*size];
    double *dataB = new double[size*size];
    double *dataC = new double[size*size];
    double *dataV = new double[size*size];

    double **A = new double*[size];
    double **B = new double*[size];
    double **C = new double*[size];
    double **V = new double*[size];

    for (int i = 0; i < size; i++)    {
        A[i] = &dataA[size*i];
        B[i] = &dataB[size*i];
        C[i] = &dataC[size*i];
        V[i] = &dataV[size*i];
        for (int j = 0; j < size; j++) {
            A[i][j] = dis(gen);
            B[i][j] = dis(gen);
            C[i][j] = 0;
            V[i][j] = 0;
        }
    }

    cout << "Done." << endl;

    //  cout << "Matrix A:" << endl;
    //  printMatrix(A, size);
    //  cout << "Matrix B:" << endl;
    //  printMatrix(B, size);

    cout << "Beginning multiply..." << endl;

    auto start = std::chrono::high_resolution_clock::now();

#ifdef GEM5
    m5_reset_stats(0, 0);
#endif
    if (blocksize == 0) {
        multiply(A, B, C, size);
    } else if (blocksize == 1) {
        blocked_multiply<4>(A, B, C, size);
    } else if (blocksize == 2) {
        blocked_multiply<8>(A, B, C, size);
    } else if (blocksize == 3) {
        blocked_multiply<16>(A, B, C, size);
    } else if (blocksize == 4) {
        blocked_multiply<64>(A, B, C, size);
    }
#ifdef GEM5
    m5_exit(0);
#endif

    auto end = std::chrono::high_resolution_clock::now();

    cout << "Done." << endl;

    cout << "Time " << (double)(end-start).count()/1e9 << " s" << endl;

    cout << "Verifying" << endl;
    serial_multiply(A, B, V, size);

    if (!verify(V, C, size)) {
        cout << "Error! failed to verify!" << endl;
    } else {
        cout << "Answer verified!" << endl;
    }

    //  cout << "Matrix C:" << endl;
    //  printMatrix(C, size);

    delete[] A;
    delete[] B;
    delete[] C;
    delete[] V;
    delete[] dataA;
    delete[] dataB;
    delete[] dataC;
    delete[] dataV;
}
