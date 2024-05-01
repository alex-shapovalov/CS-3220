//Alex Shapovalov
//CS 3220
//Programming Assignment #5, CUDA Matrix Vector

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <math.h>

const int BLOCK_SIZE = 16;

__global__
void MxV( float *x, float *y, float *z, int n ) {
    const int tidx = blockDim.x * blockIdx.x + threadIdx.x;
    const int tidy = blockDim.y * blockIdx.y + threadIdx.y;
    if (tidx < n && tidy < n) {
        int i = tidx * n + tidy;
        z[i] = x[i] + y[i];
    }
}

int main() {
    int N = 5000;

    srand48(time(0));

    float *x = (float*)malloc(N*N*sizeof(float));
    float *y = (float*)malloc(N*N*sizeof(float));
    float *z = (float*)malloc(N*N*sizeof(float));

    //fill matrices
    for (int i = 0; i < N*N; i++) {
        x[i] = drand48();
        y[i] = drand48();
    }

    float *d_x, *d_y, *d_z;
    size_t pitch;
    cudaMalloc((void**) &d_x, N*N*sizeof(float));
    cudaMalloc((void**) &d_y, N*N*sizeof(float));
    cudaMalloc((void**) &d_z, N*N*sizeof(float));



    //time without memory
    //------------------------------------------------------------------------------------------------------------------



    cudaMemcpy(d_x, x, N*N*sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(d_y, y, N*N*sizeof(float), cudaMemcpyHostToDevice);

    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start, 0);

    dim3 blocks((N + BLOCK_SIZE - 1) / BLOCK_SIZE, (N + BLOCK_SIZE - 1) / BLOCK_SIZE);
    dim3 threadsPerBlock(BLOCK_SIZE, BLOCK_SIZE);

    MxV<<<blocks, threadsPerBlock>>>( d_x, d_y, d_z, N );

    cudaEventRecord(stop, 0);
    cudaEventSynchronize(stop);
    float elapsedTimeGPUNoMem;
    cudaEventElapsedTime(&elapsedTimeGPUNoMem, start, stop);
    printf("elapsed time GPU with no memory copies: %.4f ms\n", elapsedTimeGPUNoMem);
    cudaEventDestroy(start);
    cudaEventDestroy(stop);

    cudaDeviceSynchronize();
    cudaMemcpy( z, d_z, N*N*sizeof(float), cudaMemcpyDeviceToHost );



    //time with memory
    //------------------------------------------------------------------------------------------------------------------

    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start, 0);

    cudaMemcpy( d_x, x, N*N*sizeof(float), cudaMemcpyHostToDevice );
    cudaMemcpy( d_y, y, N*N*sizeof(float), cudaMemcpyHostToDevice );

    MxV<<<blocks, threadsPerBlock>>>( d_x, d_y, d_z, N );

    cudaDeviceSynchronize();
    cudaMemcpy( z, d_z, N*N*sizeof(float), cudaMemcpyDeviceToHost );

    cudaEventRecord(stop, 0);
    cudaEventSynchronize(stop);
    float elapsedTimeGPUMem;
    cudaEventElapsedTime(&elapsedTimeGPUMem, start, stop);
    printf("elapsed time GPU with memory copies: %.4f ms\n", elapsedTimeGPUMem);
    cudaEventDestroy(start);
    cudaEventDestroy(stop);



    //------------------------------------------------------------------------------------------------------------------



    // finish up on the CPU side
    struct timeval t1, t2;
    float elapsedTimeCPU;
    gettimeofday(&t1, NULL);

    //cpu multiplication here
    float *cpu_z = (float*)malloc(N*N*sizeof(float));
    for (int i = 0; i < N*N; i++) {
        cpu_z[i] = x[i] + y[i];
    }

    gettimeofday(&t2, NULL);
    elapsedTimeCPU = (t2.tv_sec - t1.tv_sec) * 1000.0; // sec to ms
    elapsedTimeCPU += (t2.tv_usec - t1.tv_usec) / 1000.0; // us to ms
    printf("elapsed time CPU: %f ms\n", elapsedTimeCPU); // elapsed time in milliseconds

    //compare vectors relative error
        float *d = (float *)malloc( N*N*sizeof(float));
        for (int i = 0; i < N*N; i++) {
            d[i] = z[i] - cpu_z[i];
        }

        float sum = 0.0;
        for (int i = 0; i < N*N; i++) {
            sum += d[i] * d[i];
        }

        float norm_d = sqrt(sum);

        sum = 0.0;
        for (int i = 0; i < N*N; i++) {
            sum += cpu_z[i] * cpu_z[i];
        }

        float norm_cpu_z = sqrt(sum);

    float relative_error = norm_d / norm_cpu_z;
    printf("Relative error = %f\n", relative_error);

    cudaFree(d_x);
    cudaFree(d_y);
    cudaFree(d_z);

    free(x);
    free(y);
    free(z);
    free(cpu_z);
    free(d);

    return 0;
}
