#add `diff` in retrieved patterns

from multiprocessing import Process, Manager, Pool
import numpy as np
import os

def exact_similar_score(results1, results2):
    freq_dict = {}
    for idx, result in enumerate(results1):
        pattern = result[0]
        frequency = result[1]
        freq_dict[pattern] = frequency


    dedominator = 0
    distance = 0
    missed_patterns = []
    for idx, result in enumerate(results2):
        pattern = result[0]
        frequency = result[1]
        dedominator += frequency
        if pattern not in freq_dict:
            missed_patterns.append(pattern)
            distance += frequency
        else:
            distance +=  min(abs(frequency - freq_dict[pattern]), frequency )
    return (dedominator - distance) / dedominator, missed_patterns

def vector_similar_score(vec_i, vec_j, i, j):
    return i, j, np.sum(np.absolute(vec_i - vec_j)) / max(np.sum(vec_i), np.sum(vec_j))



def calculate_similarity(vectors, persistent_file):
    job_queue = []
    poolsize = os.cpu_count() -1
    pool = Pool(processes=poolsize)
    keys = vectors.keys()

    for i in range(0, len(keys)):
        for j in range(i+1, len(keys)):
            job_queue.append((i, j, vectors[i], vectors[j]))
            if len(job_queue) == poolsize:
                result = pool.map(vector_similar_score, job_queue)
                for r in result:
                    idx_i, idx_j, score = r
                    persistent_file.write(
                        "{},{},{}\n".format(idx_i, idx_j, score))
                job_queue = []


