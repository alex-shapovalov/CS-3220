cmake_minimum_required(VERSION 3.23)
project(CUDA)

set(CMAKE_CXX_STANDARD 14)

set(CMAKE_CUDA_ARCHITECTURES 86)

include_directories("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.4/include")

add_executable(CUDA cuda.cpp)
