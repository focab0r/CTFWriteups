import hashlib

def calculate_merkle_root(phrases):
    hashed_phrases = [hashlib.sha256(phrase.encode()).hexdigest() for phrase in phrases] 
    while len(hashed_phrases) > 1:
        combined_hashes = []
        for i in range(0, len(hashed_phrases), 2):
            combined_hash = hashed_phrases[i]
            if i + 1 < len(hashed_phrases):
                combined_hash += hashed_phrases[i + 1]
            combined_hashes.append(hashlib.sha256(combined_hash.encode()).hexdigest())
        hashed_phrases = combined_hashes

    return hashed_phrases[0]

phrases = ["The", "password", "that",  "I", "use", "is", "the", "same", "as", "in", "the", "Google", "account", "it", "is"]
known_merkle_root = "30c085686aa4b1d76ac1c72dfefab6f4a02f5e3865acd76f868b6d5781d2efc8"

words_to_test_file = "/usr/share/wordlists/rockyou.txt"  
with open(words_to_test_file, 'r', encoding='latin-1') as file:
    words_to_test = [line.strip() for line in file]

for word in words_to_test:
    phrases = ["The", "password", "that",  "I", "use", "is", "the", "same", "as", "in", "the", "Google", "account", "it", "is"]
    phrases.append(word)
    merkle_root = calculate_merkle_root(phrases)
    print (phrases)
    print(f'Trying pass {word}, with MR = {merkle_root}')
    if merkle_root == known_merkle_root:
        print("Found matching word:", word)
        break
