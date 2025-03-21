cmake_minimum_required(VERSION 3.15)
project(WormholeSim LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)

# Enable code completion by generating compile_commands.json
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)


include(FindThreads)
include(FindProtobuf)
protobuf_generate_cpp(PROTO_SRC PROTO_HEADER src/proto/echo.proto)
include_directories(${CMAKE_CURRENT_BINARY_DIR})

# Build bRPC dependence in /deps/brpc
add_subdirectory(deps/brpc)
set(BRPC_OUTPUT_PATH ${CMAKE_BINARY_DIR}/deps/brpc/output)
include_directories(${BRPC_OUTPUT_PATH}/include)


# Add gflags
find_package(gflags REQUIRED)
# find_path(GFLAGS_INCLUDE_PATH gflags/gflags.h)
# find_library(GFLAGS_LIBRARY NAMES gflags libgflags)
# if((NOT GFLAGS_INCLUDE_PATH) OR (NOT GFLAGS_LIBRARY))
#     message(FATAL_ERROR "Failed to find gflags")
# endif()
# include_directories(${GFLAGS_INCLUDE_PATH})


# Add leveldb
find_package(leveldb REQUIRED)

# Add OpenSSL
find_package(OpenSSL)


set(DYNAMIC_LIB
	${CMAKE_THREAD_LIBS_INIT}
	${GFLAGS_LIBRARY}
	${PROTOBUF_LIBRARIES}
	${OPENSSL_CRYPTO_LIBRARY}
	${OPENSSL_SSL_LIBRARY}
	# ${THRIFT_LIB}
	leveldb::leveldb
	dl
)
add_executable(sim-server
	src/main.cc
	${PROTO_SRC}
	${PROTO_HEADER}
)

target_link_libraries(sim-server
	PUBLIC
	${BRPC_OUTPUT_PATH}/lib/libbrpc.a
	${DYNAMIC_LIB}
)