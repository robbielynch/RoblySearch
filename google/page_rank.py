__author__ = 'robbie'

import urllib.request

def get_page_rank(domain = 'http://google.com'):
    # Get PageRank of Your Website
    GPR_HASH_SEED = "Mining PageRank is AGAINST GOOGLE'S TERMS OF SERVICE. Yes, I'm talking to you, scammer."

    domain = domain.replace('http://','').strip()

    magic = 0x1020345
    for i in range(len(domain)):
        magic ^= ord(GPR_HASH_SEED[i % len(GPR_HASH_SEED)]) ^ ord(domain[i])
        magic = (magic >> 23 | magic << 9) & 0xFFFFFFFF
    chksum = "8%08x" % (magic)

    url = "http://toolbarqueries.google.com/tbr?client=navclient-auto&features=Rank&ch=%s&q=info:%s" \
            %(chksum, domain)

    data = urllib.request.urlopen(url).read().decode('utf-8').split(":")

    return int(data[len(data) - 1])