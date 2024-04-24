// Alex Shapovalov
// CS 3220
// Programming Assignment #5, CUDA

#include <cuda.h>
#include <cuda_runtime.h>
#include <device_functions.h>
#include <device_launch_parameters.h>
#include <iostream>
#include <chrono>

using namespace std;

__global__ void dotp (float *u, float *v, float *partialSums, int n) {
    extern __shared__ float localCache[];
    int tidx = threadIdx.x + blockIdx.x * blockDim.x;
    localCache[threadIdx.x] = u[tidx] * v[tidx];
    __syncthreads();

    if (threadIdx.x == 0) {
        float temp = 0.0;
        for (int i = 0; i < blockDim.x; i++) {
            temp = temp + localCache[i];
            localCache[0] - temp;
        }
    }
}

int main() {
    cout << "Hello World." << endl;

    chrono::time_point<chrono::system_clock> t1, t2;
    chrono::duration<float, milli> elapsedTime{};

    t1 = chrono::system_clock::now();

    //GPU runs here

    t2 = chrono::system_clock::now();

    elapsedTime = t2 - t1;

    cout << elapsedTime.count() << " ms" << std::endl;

    return 0;
}