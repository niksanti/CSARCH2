# CSARCH2 Cache Simulation Project: 4 Way BSA + MRU

## Dependencies
pip install tk

## Members

GUANZON, CARLOS ANTONIO

MARASIGAN, MARC DANIEL

SANTIAGO, NIKOLAI ANDRE 

VILLARAMA, KENN MICHAEL


Section: S13


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

### Example Sequence (if n=8): 0, 1, 2, 3, ..., 15, 0, 1, 2, 3, ..., 15, 0, 1, 2, 3, ..., 15, 0, 1, 2, 3, ..., 15

Analysis: In a 4-way set-associative mapping, each set has four blocks. The sequential access will still benefit from spatial locality within each set and likely lead to cache hits as the next block in the sequence will be in the same set as the previous one especially since we are using the MRU replacement algorithm, which replaces the most recently used block within the set. For this example sequence, it also fits perfectly with the order of sets per sequence which would contribute to the fact there are more hits when compared with scenarios having a larger number of memory blocks.

![image](https://github.com/niksanti/CSARCH2/assets/64532697/16c9f532-8e95-41e1-b95b-e975317467fc)




Figure 1.1 Snapshot of Sequential 4 way BSA+MRU n=8



### Example Sequence (if n=16): 0, 1, 2, 3, ..., 31, 0, 1, 2, 3, ..., 31, 0, 1, 2, 3, ..., 31, 0, 1, 2, 3, ..., 31

Analysis: In this example sequence, it can be observed that there are a lot more misses than hits this time around. The pattern of replacement can also be observed wherein there are 3 hits for a recurring value in each of the sets. There is also a noticeable pattern wherein the previous value from block 3 will have 2 hits for it in block 2, and a previous value from block 2 will have 1 hit for it in block 1.

![image](https://github.com/niksanti/CSARCH2/assets/64532697/a3fd9eea-1eff-4c8a-9fee-76f3055e70ec)


Figure 1.2 Tracing of Cache Replacement for n=16


### Example Sequence (if n=32): 0, 1, 2, 3, …, 63, 0, 1, 2, 3, …, 63, 0, 1, 2, 3, …, 63, 0, 1, 2, 3, …, 63

Analysis: Using the same configurations, the sequential model for n=32 follows the same pattern but yields exponentially larger values. It can also be noticed that the miss rate is now significantly larger than the hit rate. This can indicate that as more integers are being read, more misses are highly likely to occur.


![image](https://github.com/niksanti/CSARCH2/assets/64532697/eb0ddbbe-ded5-4449-a8d9-dfd300fae1c2)


Figure 1.3 Snapshot of Sequential 4 way BSA+MRU n=32


b.) Random Sequence:
Scenario Description: Random access to 4n blocks.
Example Sequence (if n=8): Random sequence of 32 unique block addresses.
Analysis: The random sequence will most likely result in more cache misses, as the blocks are accessed without any ordering. 


c.) Mid-Repeat Blocks:
Scenario Description: Start at block 0, repeat the sequence in the middle two times up to n-1 blocks, after which continue up to 2n. Repeat the sequence four times.

### Example Sequence (if n=8): 0, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 {4x}

Analysis: In this scenario, it involves a mix of sequential and non-sequential accesses. Also, since the sequence repeats midway, it will result in more cache hits than sequential sequence because we are using the MRU replacement algorithm. It has a faster average access time because a mid-repeat pattern introduces repetition in the middle section of the sequence. This means that the elements in the middle of the sequence are accessed more frequently than the surrounding elements. In an MRU algorithm, this repetition in the middle results in those specific elements being kept in the cache as the most recently used, optimizing the use of those frequently accessed in the cache.

![image](https://github.com/niksanti/CSARCH2/assets/64532697/f717df56-d7b8-42ff-9249-958aa3d9c0ea)

Figure  1.4 Snapshot of Mid-Repeat 4 way BSA+MRU n=8

### Example Sequence (if n=16): 0, …, 14, 1, …, 31, 0, …, 14, 1, …,31, 0, …, 14, 1, …, 31, 0, …, 31

Analysis: Similar to the n=8 sequence, this pattern creates a sequence that starts sequentially and then repeats with a shift, introducing variation in the sequence. The mid-repeat phase ensures that the sequence doesn't become entirely predictable and adds some complexity to the pattern. After completing the sequential phase, there is a mid-repeat phase. During the mid-repeat phase, the sequence is repeated, but with a modification. The modification involves repeating the sequence but excluding the first element. This creates a shift in the sequence.

![image](https://github.com/niksanti/CSARCH2/assets/64532697/b97b2cc4-dde1-4fcf-a31e-30515c9ddb4a)

Figure 1.5 Snapshot of Mid-Repeat Block 4 way BSA+MRU n=16



