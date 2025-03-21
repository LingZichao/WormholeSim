cmake_minimum_required(VERSION 3.15)
project(WormholeSim LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)

# Enable code completion by generating compile_commands.json
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(gflags REQUIRED)
find_package(leveldb REQUIRED)
find_package(Threads REQUIRED)
find_package(Protobuf REQUIRED)
find_package(OpenSSL)

# Include proto files
include_directories(${CMAKE_CURRENT_BINARY_DIR}) 
include_directories(${CMAKE_CURRENT_BINARY_DIR}/src/proto) 

# Build bRPC dependence in /deps/brpc
add_subdirectory(deps/brpc)
set(BRPC_OUTPUT_PATH ${CMAKE_BINARY_DIR}/deps/brpc/output)
include_directories(${BRPC_OUTPUT_PATH}/include)

# Set dynamic libraries
set(DYNAMIC_LIB
	Threads::Threads
	protobuf::libprotobuf
	OpenSSL::SSL
	leveldb::leveldb
	gflags
	dl
)

add_executable(sim-server
	src/main.cc
)

protobuf_generate(
    TARGET sim-server
    PROTOS src/proto/echo.proto
    LANGUAGE cpp
)

target_link_libraries(sim-server
	PUBLIC
	${BRPC_OUTPUT_PATH}/lib/libbrpc.a
	${DYNAMIC_LIB}
)