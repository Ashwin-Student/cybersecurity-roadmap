import math
import getpass

def calculate_shannon_entropy(password: str) -> float:
    """Calculate the Shannon entropy of a string (bits of uncertainty per character)."""
    if not password:
        return 0.0

    length = len(password)
    frequency = {}

    for char in password:
        frequency[char] = frequency.get(char, 0) + 1

    entropy = 0.0
    for count in frequency.values():
        p = count / length
        entropy -= p * math.log2(p)

    # Total theoretical entropy in bits = character entropy * length
    return round(entropy * length, 2)

def evaluate_strength(total_entropy: float) -> str:
    if total_entropy < 30:
        return "Very Weak (Vulnerable to trivial brute-force)"
    elif total_entropy < 50:
        return "Weak (Susceptible to targeted dictionary attacks)"
    elif total_entropy < 70:
        return "Moderate (Acceptable for standard user accounts)"
    else:
        return "Strong (High resilience against offline cracking)"

if __name__ == "__main__":
    user_pass = getpass.getpass("Enter password to evaluate (hidden input): ")
    
    bits = calculate_shannon_entropy(user_pass)
    rating = evaluate_strength(bits)

    print("\n--- Password Strength Report ---")
    print(f"Length:           {len(user_pass)} characters")
    print(f"Shannon Entropy:  {bits} bits")
    print(f"Assessment:       {rating}")