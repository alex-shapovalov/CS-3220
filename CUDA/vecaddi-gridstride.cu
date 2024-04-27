// jdh Spring 2023
// example program for CS222

#include <stdio.h>
#include <stdlib.h>

#define N 1048576 // this is 2^20

__global__
void add( int *X, int *Y, int *Z, int n) {
  int stride = blockDim.x * gridDim.x;
  for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < n; i = i + stride)
    Z[i] = X[i] + Y[i];
}

//----------------------------------------------------------------

void printDeviceProperties() {
  int count;
  cudaDeviceProp prop;

  cudaGetDeviceCount( &count );
  printf("system has %d device(s)\n", count);
  for (int i=0; i<count; ++i) {
    cudaGetDeviceProperties( &prop, i );
    printf("name is %s\n", prop.name);
    printf("multiProcessorCount is %d\n", prop.multiProcessorCount);
    printf("warpSize is %d\n", prop.warpSize);
    printf("maxThreadsPerBlock is %d\n", prop.maxThreadsPerBlock);
    printf("maxThreadsDim is (%d, %d, %d)\n", prop.maxThreadsDim[0],
           prop.maxThreadsDim[1], prop.maxThreadsDim[2]);
    printf("maxGridSize is (%d, %d, %d)\n", prop.maxGridSize[0],
           prop.maxGridSize[1], prop.maxGridSize[2]);
  }
}

//----------------------------------------------------------------

int main() {
  int *X, *Y, *Z;
  int *dev_X, *dev_Y, *dev_Z;

  printDeviceProperties();

  // allocate memory on the host
  X = (int *) malloc(N*sizeof(int));
  Y = (int *) malloc(N*sizeof(int));
  Z = (int *) malloc(N*sizeof(int));

  // allocate memory on the GPU
  cudaMalloc( (void **) &dev_X, N*sizeof(int) );
  cudaMalloc( (void **) &dev_Y, N*sizeof(int) );
  cudaMalloc( (void **) &dev_Z, N*sizeof(int) );

  // set up the problem on the host
  for (int i=0; i<N; ++i) {
    X[i] = i;
    Y[i] = i*i;
  }

  // copy data to the GPU
  cudaMemcpy( dev_X, X, N*sizeof(int), cudaMemcpyHostToDevice );
  cudaMemcpy( dev_Y, Y, N*sizeof(int), cudaMemcpyHostToDevice );

  int threadsPerBlock = 256;
  int numBlocks = (N + threadsPerBlock - 1) / threadsPerBlock;
  add<<<numBlocks,threadsPerBlock>>>( dev_X, dev_Y, dev_Z, N);

  // not necessary to force explicity synchronization between GPU and host--
  // synchronization will happen by default

  // copy results back to the host
  cudaMemcpy( Z, dev_Z, N*sizeof(int), cudaMemcpyDeviceToHost );

  int fail = 0;
  for (int i=0; i<N; ++i) {
    if (Z[i] != X[i] + Y[i])
      fail = 1;
  }

  if (fail)
    printf("error!\n");
  else
    printf("success\n");

  cudaFree( dev_X );
  cudaFree( dev_Y );
  cudaFree( dev_Z );

  free(X);
  free(Y);
  free(Z);

  return 0;
}
