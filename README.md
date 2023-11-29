# CSARCH2 Cache Simulation Project: 4 Way BSA + MRU

## How to Use It?
lorem ipsum lorem ipsum

## Dependencies
pip install tk


## Full Specification of the cache simulation system

The cache simulation system simulates cache memory access with 4-way Block-Set Associative Mapping using the Most Recently Used (MRU) replacement algorithm. Our cache simulation system is well optimized in handling any number of memory blocks by the user.

System Cache Structure:
Cache is organized into 4 sets, each with 4 lines (4-way set-associative).
Each line holds 32 words.

Cache Size: 4 sets * 4 lines (4-way set-associative) * 32 words (cache line size) = 512 words
Block Size: 32 words
Number of Sets: 4 sets
Block Offset Bits: log2(32) = 5 bits
Set Index Bits: log2(4) = 2 bits
Total Address Bits: log2(512) = 9 bits

Replacement Policy: Most Recently Used (MRU)
Read Policy: Load-through

Memory Access Time: 10ns
Cache Access Time: 1ns

Simulation Procedure:
Initialize the cache. For each test case, it loads the specified memory blocks into the cache based on the test case scenario and tracks cache hits and misses. Repeat the process as specified in the test case.

After completing the simulation process, the system calculates the average and total access time based on the number of cache hits and misses. 

The system outputs and shows the memory access count, cache hit count, cache miss count, cache hit rate, cache miss rate, average memory access time, and total memory access time. The system also provides a text log of the cache memory trace and an option for step-by-step animated tracing.







