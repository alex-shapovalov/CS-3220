//Alex Shapovalov
//CS 3220
//Programming Assignment #5, CUDA Matrix Vector

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

const int BLOCK_SIZE = 16;

//block number = n / threads per block

__global__
void MxV( float *M, float *x, float *y, int n) {
    const int tidx = blockDim.x * blockIdx.x + threadIdx.x;
    const int tidy = blockDim.y * blockIdx.y + threadIdx.y;
    if (tidx < n && tidy < n) {
        z[tidx*n + tidy] = x[tidx*n + tidy] + y[tidx*n + tidy];
        //tidx = m[0] * x[0] + m[1] * x[1] + m[2] * x[2]
        //no partial sums / local cache
}

int main() {
    float *d_x, *d_y, *d_z;
    size_t pitch;
    cudaMalloc((void**) &d_x, N*N*sizeof(float));
    cudaMalloc((void**) &d_y, N*N*sizeof(float));
    cudaMalloc((void**) &d_z, N*N*sizeof(float));
    cudaMemcpy(d_x, h_x, N*N*sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(d_y, h_y, N*N*sizeof(float), cudaMemcpyHostToDevice);

    dim3 blocks(1, 1, 1);
    dim3 threadsPerBlock(BLOCK_SIZE, BLOCK_SIZE, 1);
    blocks.x = (N + BLOCK_SIZE – 1) / BLOCK_SIZE;
    blocks.y = (N + BLOCK_SIZE – 1) / BLOCK_SIZE;
    add2D<<<blocks, threadsPerBlock>>>( d_x, d_y, d_z, N );
    cudaDeviceSynchronize(); // this blocks until the device has completed all requested tasks

    //vector norms
    //compare results?


    return 0;
}
