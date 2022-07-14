#include<random>
#include<cmath>
#include<iomanip>
#include<stdio.h>
#include<limits.h>
#include<stdlib.h>
#include<iostream>
#include<chrono>

#define GEM5

#ifdef GEM5
#include <gem5/m5ops.h>
#endif


void out_of_range() {
    std :: cout << "error: the size of the matrix should be 1 to " << UINT_MAX
        << std :: endl;
    std :: cout << std :: endl;
}

int main(int argc, char *argv[]) {

    // We are tracking the wall clock time required to execute the matrix
    // multiply program.
    //
    auto prog_start = std :: chrono :: high_resolution_clock :: now();

    // Setting the size of the matrix (N x N). M = 10
    //
    const unsigned int N = 10;

    if(!(N > 1 && N < UINT_MAX)) {
        out_of_range();
        return -1;
    }
    // Initializing the matrix here. We are using a random distribution to
    // initialize the matrix.
    //
    std :: random_device rd;
    std :: mt19937 gen(rd());
    std :: uniform_real_distribution<> dis(0, 1);

    double *data_A = new double[N * N];
    double *data_B = new double[N * N];
    double *data_C = new double[N * N];

    double **A = new double*[N];
    double **B = new double*[N];
    double **C = new double*[N];

    for(int i = 0 ; i < N ; i++) {
        A[i] = &data_A[N * i];
        B[i] = &data_B[N * i];
        C[i] = &data_C[N * i];
        for(int j = 0 ; j < N ; j++) {
            A[i][j] = dis(gen);
            B[i][j] = dis(gen);
            C[i][j] = 0;
        }
    }

    // Naive matrix multiplication code. It performs N^3 computations. We also
    // keep a track of time for this part of the code.
    //
    auto mm_start = std :: chrono :: high_resolution_clock :: now();

#ifdef GEM5
    m5_checkpoint(0, 0);
#endif

    for(int i = 0 ; i < N ; i++)
        for(int j = 0 ; j < N ; j++)
            for(int k = 0 ; k < N ; k++)
                C[i][j] += A[i][k] * B[k][j];

#ifdef GEM5
    m5_checkpoint(0, 0);
#endif

    auto mm_end = std :: chrono :: high_resolution_clock :: now();

    // Free the memory allocated.
    //
    delete data_A;
    delete data_B;
    delete data_C;
    delete A;
    delete B;
    delete C;

    // We take a note of the final wall clock time before printing the final
    // statistics.
    //
    auto prog_end = std :: chrono :: high_resolution_clock :: now();
    std :: chrono :: duration<double> prog_elapsed = std :: chrono :: 
        duration_cast<std :: chrono :: duration<double>>(prog_end - prog_start);
    std :: chrono :: duration<double> mm_elapsed = std :: chrono :: 
        duration_cast<std :: chrono :: duration<double>>(mm_end - mm_start);

    // Printing statistics at the end of the program.
    //
    std :: cout << "Printing Statistics :: Wall Clock Time" << std :: endl;
    std :: cout << "======================================" << std :: endl; 
    std :: cout << "Program: " << prog_elapsed.count() << " s" << std :: endl;
    std :: cout << "Matrix Multiply: " << mm_elapsed.count() << " s" << std :: endl;
    std :: cout << std :: endl;

    return 1;
}
