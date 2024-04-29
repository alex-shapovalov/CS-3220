//Alex Shapovalov
//CS 3220
//Programming Assignment #5, CUDA

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

const int BLOCK_SIZE = 16;

__global__
void dotp( float *U, float *V, float *partialSum, int n ) {
    extern __shared__ float localCache[];
    int tidx = threadIdx.x + blockIdx.x * blockDim.x;
    localCache[threadIdx.x] = U[tidx] * V[tidx];
    __syncthreads();

    int cacheIndex = threadIdx.x;
    int i = blockDim.x / 2;
    while (i > 0) {
        if (cacheIndex < i) {
            localCache[cacheIndex] = localCache[cacheIndex] + localCache[cacheIndex + i];
        }
        __syncthreads();
        i = i / 2;
    }

    if (cacheIndex == 0) {
        partialSum[blockIdx.x] = localCache[cacheIndex];
    }
}

int main() {
    int numBlocks = 256;
    int threadsPerBlock = 256;
    int N = numBlocks * threadsPerBlock; //array size

    srand48(time(0));

    float *U = (float *) malloc(N * sizeof(float));
    float *V = (float *) malloc(N * sizeof(float));
    float *partialSum = (float *) malloc(numBlocks * sizeof(float));

    float *dev_U, *dev_V, *dev_partialSum;
    cudaMalloc(&dev_U, N * sizeof(float));
    cudaMalloc(&dev_V, N * sizeof(float));
    cudaMalloc(&dev_partialSum, numBlocks * sizeof(float));

    //fill arrays
    for (int i=0; i<N; ++i) {
        U[i] = drand48();
        V[i] = drand48();
    }

    cudaMemcpy( dev_U, U, N*sizeof(float), cudaMemcpyHostToDevice );
    cudaMemcpy( dev_V, V, N*sizeof(float), cudaMemcpyHostToDevice );

    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start, 0);

    dotp<<<numBlocks, threadsPerBlock, BLOCK_SIZE * sizeof(float)>>>( dev_U, dev_V, dev_partialSum, N );

    cudaEventRecord(stop, 0);
    cudaEventSynchronize(stop);
    float elapsedTimeGPU;
    cudaEventElapsedTime(&elapsedTimeGPU, start, stop);
    printf("elapsed time GPU: %.4f ms\n", elapsedTimeGPU);
    cudaEventDestroy(start);
    cudaEventDestroy(stop);

    cudaDeviceSynchronize(); // wait for GPU threads to complete; again, not necessary but good pratice
    cudaMemcpy( partialSum, dev_partialSum, numBlocks*sizeof(float), cudaMemcpyDeviceToHost );

    // finish up on the CPU side
    float gpuResult = 0.0;
    for (int i=0; i<numBlocks; ++i)
        gpuResult = gpuResult + partialSum[i];

    struct timeval t1, t2;
    float elapsedTimeCPU;
    gettimeofday(&t1, NULL);

    float cpuResult = 0.0;
    for (int i = 0; i < N; ++i) {
        cpuResult += U[i] * V[i];
    }

    gettimeofday(&t2, NULL);
    elapsedTimeCPU = (t2.tv_sec - t1.tv_sec) * 1000.0; // sec to ms
    elapsedTimeCPU += (t2.tv_usec - t1.tv_usec) / 1000.0; // us to ms
    printf("elapsed time CPU: %f ms\n", elapsedTimeCPU); // elapsed time in milliseconds

    cudaFree(dev_U);
    cudaFree(dev_V);
    cudaFree(dev_partialSum);

    free(U);
    free(V);
    free(partialSum);

    return 0;
}
