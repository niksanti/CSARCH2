# CSARCH2 Cache Simulation Project: 4 Way BSA + MRU

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

## Detailed Analysis for the three test cases

Test Cases:
a.) Sequential Sequence:
Scenario Description: Sequential access to cache blocks up to 2n. Repeat the sequence four times.
Example Sequence (if n=8): 0, 1, 2, 3, ..., 15, 0, 1, 2, 3, ..., 15, 0, 1, 2, 3, ..., 15, 0, 1, 2, 3, ..., 15
Analysis: In a 4-way set-associative mapping, each set has four blocks. The sequential access will still benefit from spatial locality within each set and likely lead to cache hits as the next block in the sequence will be in the same set as the previous one especially since we are using the MRU replacement algorithm, which replaces the most recently used block within the set. For this example sequence, it also fits perfectly with the order of sets per sequence which would contribute to the fact there are more hits when compared with scenarios having a larger number of memory blocks.

![image](https://github.com/niksanti/CSARCH2/assets/64532697/16c9f532-8e95-41e1-b95b-e975317467fc)




Figure 1.1 Snapshot of Sequential 4 way BSA+MRU n=8



### Example Sequence (if n=16): 0, 1, 2, 3, ..., 31, 0, 1, 2, 3, ..., 31, 0, 1, 2, 3, ..., 31, 0, 1, 2, 3, ..., 31

In this example sequence, it can be observed that there are a lot more misses than hits this time around. The pattern of replacement can also be observed wherein there are 3 hits for a recurring value in each of the sets. There is also a noticeable pattern wherein the previous value from block 3 will have 2 hits for it in block 2, and a previous value from block 2 will have 1 hit for it in block 1.

![image](https://github.com/niksanti/CSARCH2/assets/64532697/a3fd9eea-1eff-4c8a-9fee-76f3055e70ec)



Figure 1.2 Tracing of Cache Replacement for n=16


### Example Sequence (if n=32): 0, 1, 2, 3, …, 63, 0, 1, 2, 3, …, 63, 0, 1, 2, 3, …, 63, 0, 1, 2, 3, …, 63

Analysis: Using the same configurations, the sequential model for n=32 follows the same pattern but yields exponentially larger values. It can also be noticed that the miss rate is now significantly larger than the hit rate. This can indicate that as more integers are being read, more misses are highly likely to occur.






Figure 1.3 Snapshot of Sequential 4 way BSA+MRU n=32





b.) Random Sequence:
Scenario Description: Random access to 4n blocks.
Example Sequence (if n=8): Random sequence of 32 unique block addresses.
Analysis: The random sequence will most likely result in more cache misses, as the blocks are accessed without any ordering. 






