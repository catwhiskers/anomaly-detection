from frequent_pattern import mine_string_patterns
import pickle
import os
from multiprocessing import Process, Manager, Pool

class FrequentPatternVectorizor:
    def __init__(self, docs):
        self.pattern_corpus = {}
        self.features = []
        self.dim_info = {}
        self.docs = docs
        self.featurestore = {}

    def build_patterns(self):
        poolsize = os.cpu_count() - 1
        print(poolsize)
        pool = Pool(processes=poolsize)
        job_queue = []
        print(len(self.docs))
        for index, lines in enumerate(self.docs):
            if index % 1000 ==0:
                print("processed "+str(index)+" documents") 
            job_queue.append((index, lines))
            if len(job_queue) == poolsize:

                result_group = pool.map(mine_string_patterns, job_queue)
                for res in result_group:
                    # print("res", res)
                    id, patterninfo = res
                    self.pattern_corpus[id] = patterninfo
                    for result in patterninfo:
                        pattern = result[0]
                        frequency = result[1]
                        if pattern not in self.dim_info:
                            idx = len(self.features)
                            self.features.append(pattern)
                            self.dim_info[pattern] = len(self.features) - 1
                job_queue = []
        print(len(self.features))

    def vectorize(self):
        for key in self.pattern_corpus:
            cfeature = [0 for i in range(0, len(self.features))]
            results = self.pattern_corpus[key]
            for res in results:
                p = res[0]
                f = res[1]
                if p in self.dim_info:
                    cfeature[self.dim_info[p]] = f
            self.featurestore[key] = cfeature





