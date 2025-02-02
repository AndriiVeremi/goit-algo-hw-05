import timeit


def kmp_search(text, pattern):
    def build_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    lps = build_lps(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j  
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1  

def boyer_moore_search(text, pattern):
    def bad_character_table(pattern):
        bad_char = {}
        for i in range(len(pattern)):
            bad_char[pattern[i]] = i
        return bad_char

    bad_char = bad_character_table(pattern)
    m, n = len(pattern), len(text)
    s = 0

    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s  
        else:
            s += max(1, j - bad_char.get(text[s + j], -1))
    return -1  

def rabin_karp_search(text, pattern, q=101):
    d = 256
    m, n = len(pattern), len(text)
    p = t = 0  
    h = 1

    for i in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                return i  
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q
    return -1 


with open('article1.txt', 'r', encoding='utf-8', errors="ignore") as file:
    text1 = file.read()

with open('article2.txt', 'r', encoding='utf-8', errors="ignore") as file:
    text2 = file.read()


existing_substring = text1[:20]  
non_existing_substring = 'вигаданий підрядок'  


def measure_time(algorithm, text, pattern):
    return timeit.timeit(lambda: algorithm(text, pattern), number=10)


algorithms = {
    'KMP': kmp_search,
    'Boyer-Moore': boyer_moore_search,
    'Rabin-Karp': rabin_karp_search
}

texts = {'Article 1': text1, 'Article 2': text2}
patterns = {'Existing': existing_substring, 'Non-existing': non_existing_substring}

results = {}

for article_name, text in texts.items():
    results[article_name] = {}
    for pattern_name, pattern in patterns.items():
        results[article_name][pattern_name] = {}
        for algo_name, algo_func in algorithms.items():
            elapsed_time = measure_time(algo_func, text, pattern)
            results[article_name][pattern_name][algo_name] = elapsed_time


for article_name, patterns_results in results.items():
    print(f'\nResults for {article_name}:')
    for pattern_name, algo_results in patterns_results.items():
        print(f'  {pattern_name} substring:')
        for algo_name, time_taken in algo_results.items():
            print(f'    {algo_name}: {time_taken:.6f} seconds')