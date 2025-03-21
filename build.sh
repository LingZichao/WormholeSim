# Build WormholeSim 
# server and client library
cmake -B build -S .
cmake --build build -j$(nproc)

# Apply gem5 patch

# Build gem5
cd deps/gem5
scons ../../build/deps/gem5/build/X86/gem5.opt -j$(nproc)

