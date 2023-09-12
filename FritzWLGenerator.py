from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from tqdm import tqdm
import os
import random
import threading
import re

def no_more_than_three_repeating(sequence):
    count = 1  # Counter for consecutive repeating characters
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:
            count += 1
            if count > 3:
                return False
        else:
            count = 1  # Reset counter if characters are different
    return True

def has_repeating_abc_cycle(sequence):
    pattern = 'abc'
    pattern_length = len(pattern)
    n = len(sequence)
    
    for i in range(0, n - pattern_length * 2 + 1):  # Make sure there's room for at least two repetitions of the pattern
        if sequence[i:i+pattern_length] == pattern and sequence[i+pattern_length:i+2*pattern_length] == pattern:
            return True
    
    return False

def has_consecutive_order(sequence):
    ascending_count = 1
    descending_count = 1
    
    for i in range(len(sequence) - 1):
        if sequence[i] == str(int(sequence[i+1]) - 1):
            ascending_count += 1
        else:
            ascending_count = 1
            
        if sequence[i] == str(int(sequence[i+1]) + 1):
            descending_count += 1
        else:
            descending_count = 1
            
        if ascending_count >= 5 or descending_count >= 5:
            return True
            
    return False

def no_more_than_three_consecutive_identical_chars(sequence):
    for i in range(len(sequence) - 3):
        if sequence[i] == sequence[i + 1] == sequence[i + 2] == sequence[i + 3]:
            return False
    return True

def has_common_keyboard_sequences(sequence):
    common_sequences = [
        '12345', '23456', '34567', '45678', '56789', '67890' # Numpad sequences
    ]
    
    for seq in common_sequences:
        if seq in sequence:
            return True
    
    return False



def has_group_repeats(sequence):
    i = 0
    n = len(sequence)
    while i < n:
        current_char = sequence[i]
        repeat_count = 1
        
        while i + 1 < n and sequence[i + 1] == current_char:
            repeat_count += 1
            i += 1
        
        i += 1
    return False

def has_repeated_six_char_sequence(sequence):
    n = len(sequence)
    for i in range(n - 9):  # Loop until the 5-character sequence has enough room to repeat
        five_char_seq = sequence[i:i+6]
        
        # Check if this 5-character sequence repeats
        if five_char_seq in sequence[i+6:]:
            return True
            
    return False

def has_five_consecutive_odd_even(sequence):
    odd_count = 0
    even_count = 0

    for char in sequence:
        if not char.isdigit():
            odd_count = 0
            even_count = 0
            continue

        num = int(char)
        if num % 2 == 0:
            even_count += 1
            odd_count = 0  # Reset the odd counter
        else:
            odd_count += 1
            even_count = 0  # Reset the event counter

        if odd_count > 13 or even_count > 13:
            return True

    return False

def check_sequence(sequence):
 # Rule 1: No Palindromic Sequences
    if sequence == sequence[::-1]:
        return False
    
    # Rule 2: No more than three repeating 3-character Sequences
    if not no_more_than_three_repeating(sequence):
        return False
    
    # Rule 3: No Repeating Cycles
    if has_repeating_abc_cycle(sequence):
       return False
    
   # Rule 4: First and Last Character Must Be Different
       if sequence[0] == sequence[-1]:
        return False
    
    # Rule 5: Avoid Ascending or Descending Numerical Order
    if has_consecutive_order(sequence):
        return False
    
  # #   # Rule 6: No More Than 3 Consecutive Identical Characters
    if not no_more_than_three_consecutive_identical_chars(sequence):
        return False
    
  #   # Rule 7: Exclude Diagonal Patterns
   
    
  #   # Rule 8: No Common Keyboard Sequences
    if has_common_keyboard_sequences(sequence):
     return False
    
  #    # Rule 9: No Sequences Like "112233"
    if has_group_repeats(sequence):
     return False
    
  #   # Rule 10: No More Than Two Instances of the Same Character
    count = Counter(sequence)
    if any(v > 5 for v in count.values()):
     return False
    
  #   # Rule 11: 
    
  #   # Rule 12: No More Than 3 Consecutive Identical Digits
    for i in range(len(sequence)-3):
      if sequence[i] == sequence[i+1] == sequence[i+2] == sequence[i+3]:
           return False
    
  #   # Rule 13: No Repeated 6 -Character Sequences
      if has_repeated_six_char_sequence(sequence):
       return False
    
  #  # Rule 14: No More Than Five Consecutive Odd or Even Numbers
      if has_five_consecutive_odd_even(sequence):
        return False
      

    
    return True

def get_input():
    global abort
    while True:
        s = input("Press 'a' to abort: ")
        if s == 'a':
            abort = True
            break

def main():
    global abort
    abort = False
    
    total_count = 100000000000  # How many numbers do you want to generate?
    chunk_size = 50000000000  # How many numbers per file?
    count = 0
    f = None

    # Start the input thread
    input_thread = threading.Thread(target=get_input)
    input_thread.daemon = True
    input_thread.start()

    pbar = tqdm(total=total_count, desc="Writing Numbers")

    try:
        while count < total_count:
            if abort:
                print("Operation aborted by user.")
                break
                
            num = f"{random.randint(10**19, 10**20 - 1)}"

            if check_sequence(num):
                tmp_filename = f"wlist/fritz{count // chunk_size}.txt"
                dir_name = os.path.dirname(tmp_filename)
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                
                if f:
                    f.close()
                f = open(tmp_filename, "a")
                f.write(f"{num}\n")
                count += 1
                pbar.update(1)  # Manually update tqdm progress

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if f:
            f.close()
        pbar.close()
    
    print(f"Operation complete. {count} numbers written to files in 'wlist' directory.")

if __name__ == '__main__':
    main()
