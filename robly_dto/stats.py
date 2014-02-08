class Statistics(object):
    num_results = 0
    num_results_found = 0
    num_docs_scanned = 0
    num_scanned_objects = 0
    time_micros = 0

    def __init__(self, n, nfound, nscanned, nscanned_objects, time_micros):
        self.num_results = n
        self.num_results_found = nfound
        self.num_docs_scanned = nscanned
        self.num_scanned_objects = nscanned_objects
        self.time_micros = time_micros