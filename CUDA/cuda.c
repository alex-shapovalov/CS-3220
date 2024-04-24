// Alex Shapovalov
// CS 3220
// Programming Assignment #5, CUDA

#include <cuda_runtime.h>
#include <device_launch_parameters.h>
#include <cuda.h>
#include <device_functions.h>
#include <cuda_runtime_api.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

__global__ void dotp(float *U, float *V, float*partialSum, int n) {
    __shared__ float localCache[BLOCK_SIZE];
    int tidx = threadIdx.x + blockIdx.x * blockDim.x;
    localCache[threadIdx.x] = U[tidx] * V[tidx];
    __syncthreads();
}

int main() {

    //time check:

    struct timeval t1, t2;
    float elapsedTime;

    gettimeofday(&t1, NULL);

    //code goes here

    gettimeofday(&t1, NULL);

    elapsedTime = (t2.tv_sec - t1.tv_sec) * 1000.0;
    elapsedTime += (t2.tv_usec - t1.tv_usec) / 1000.0;
    printf("%f ms\n", elapsedTime);

    return 0;
}