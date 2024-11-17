import secrets
import string
import math
from collections import Counter


def get_user_inputs():
    while True:
        try:
            length = int(input("Enter the password length (up to 1000): "))
            if length < 16:
                print("Warning: Password length less than 16 is too short for security.")
            if 16 <= length <= 1000:
                break
            else:
                print("Please enter a valid length between 16 and 1000.")
        except ValueError:
            print("Invalid input. Please enter a number between 16 and 1000.")

    def get_yes_no_input(prompt):
        while True:
            try:
                response = input(prompt).strip().lower()
                if response in ('y', 'n'):
                    return response == 'y'
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
            except Exception as e:
                print(f"An error occurred: {e}. Please enter 'y' or 'n'.")

    while True:
        include_lower = get_yes_no_input("Include lowercase letters? (y/n): ")
        include_upper = get_yes_no_input("Include uppercase letters? (y/n): ")
        include_digits = get_yes_no_input("Include digits? (y/n): ")
        include_symbols = get_yes_no_input("Include symbols? (y/n): ")

        if include_lower or include_upper or include_digits or include_symbols:
            break
        else:
            print("You must select at least one character type. Please try again.")

    while True:
        try:
            num_passwords = int(input("How many passwords to generate? (up to 10): "))
            if 1 <= num_passwords <= 10:
                break
            else:
                print("Please enter a valid number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 10.")

    return length, include_lower, include_upper, include_digits, include_symbols, num_passwords


def calculate_repetition_limit(length, total_unique_chars):
    # Calculate expected repetitions based on password length and unique characters
    if length < 50:
        expected_repeats = length / total_unique_chars
        return math.ceil(expected_repeats * 1.5)  # Adjust limit for randomness
    elif 50 <= length < 100:
        expected_repeats = length / total_unique_chars
        return math.ceil(expected_repeats * 2)  # Allow more repetition for longer passwords
    else:
        return min(6, math.ceil(length / 20))  # Cap repetition for very long passwords


def generate_password(length, include_lower, include_upper, include_digits, include_symbols):
    char_pool = ''
    # Build character pool based on user preferences
    if include_lower:
        char_pool += string.ascii_lowercase
    if include_upper:
        char_pool += string.ascii_uppercase
    if include_digits:
        char_pool += string.digits
    if include_symbols:
        char_pool += string.punctuation

    if not char_pool:
        raise ValueError("No character types selected.")

    total_unique_chars = len(set(char_pool))
    repetition_limit = calculate_repetition_limit(length, total_unique_chars)
    password = []

    # Ensure at least one character from each selected type is included
    if include_lower:
        password.append(secrets.choice(string.ascii_lowercase))
    if include_upper:
        password.append(secrets.choice(string.ascii_uppercase))
    if include_digits:
        password.append(secrets.choice(string.digits))
    if include_symbols:
        password.append(secrets.choice(string.punctuation))

    char_counter = Counter(password)

    # Generate the remaining characters of the password
    while len(password) < length:
        char = secrets.choice(char_pool)
        # Ensure character does not exceed repetition limit and is not consecutive
        if char_counter[char] < repetition_limit and (not password or char != password[-1]):
            password.append(char)
            char_counter[char] += 1
        else:
            # Find a different character that is not the same as the last one
            alternate_char_pool = [c for c in char_pool if c != password[-1]]
            char = secrets.choice(alternate_char_pool)
            # Ensure character does not exceed repetition limit
            while char_counter[char] >= repetition_limit:
                char = secrets.choice(alternate_char_pool)
            password.append(char)
            char_counter[char] += 1

    # Shuffle the password to ensure randomness
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)


def main():
    # Get user inputs for password generation
    length, include_lower, include_upper, include_digits, include_symbols, num_passwords = get_user_inputs()

    # Generate and print the requested number of passwords
    for _ in range(num_passwords):
        print(generate_password(length, include_lower, include_upper, include_digits, include_symbols))


if __name__ == "__main__":
    main()
