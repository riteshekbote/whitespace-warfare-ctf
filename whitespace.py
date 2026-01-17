import random
import os

# Zero-width characters
zwsp = '\u200B'  # Zero Width Space
zwnj = '\u200C'  # Zero Width Non-Joiner

def generator(flag=''):
    """Generate steganographic text with hidden flag"""
    key = [zwsp, zwnj]
    randomSelect = random.choice(key)
    cover = "An old intelligence officer used to hide secrets in plain sight - not with ciphers, but with silence. His final message looks ordinary, but those who know how to look can see patterns between the letters… invisible marks that speak louder than words."
    plain = flag
    
    if randomSelect == zwsp:
        binary = ''.join(format(ord(c), '08b') for c in plain).replace('0', zwsp).replace('1', zwnj)
    else:
        binary = ''.join(format(ord(c), '08b') for c in plain).replace('1', zwsp).replace('0', zwnj)
    
    third = int(len(cover) / 3)
    half = int(len(binary) / 2)
    result = cover[:third] + binary[:half] + cover[third:2 * third] + binary[half:] + cover[2 * third:]
    
    return result

def decoder(text):
    """Decode hidden message from steganographic text"""
    # Extract zero-width characters
    hidden = ''
    for char in text:
        if char in [zwsp, zwnj]:
            hidden += char
    
    print(f"Found {len(hidden)} zero-width characters")
    
    # Try decoding with zwsp=0, zwnj=1
    binary1 = hidden.replace(zwsp, '0').replace(zwnj, '1')
    result1 = ''
    for i in range(0, len(binary1), 8):
        byte = binary1[i:i+8]
        if len(byte) == 8:
            result1 += chr(int(byte, 2))
    
    # Try decoding with zwsp=1, zwnj=0 (opposite mapping)
    binary2 = hidden.replace(zwsp, '1').replace(zwnj, '0')
    result2 = ''
    for i in range(0, len(binary2), 8):
        byte = binary2[i:i+8]
        if len(byte) == 8:
            result2 += chr(int(byte, 2))
    
    print("\n=== Decoding Method 1 (zwsp=0, zwnj=1) ===")
    print(f"Binary: {binary1[:64]}...")
    print(f"Result: {result1}")
    
    print("\n=== Decoding Method 2 (zwsp=1, zwnj=0) ===")
    print(f"Binary: {binary2[:64]}...")
    print(f"Result: {result2}")
    
    return result1, result2

# Read the file
def decode_file(filename):
    """Decode a file containing steganographic text"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        
        print(f"File loaded: {len(text)} characters")
        print(f"First 100 chars: {text[:100]}")
        
        result1, result2 = decoder(text)
        
        # Determine which result looks like a flag
        if result1.startswith('ICS{') or 'ICS{' in result1:
            print(f"\n🚩 FLAG FOUND: {result1}")
            return result1
        elif result2.startswith('ICS{') or 'ICS{' in result2:
            print(f"\n🚩 FLAG FOUND: {result2}")
            return result2
        else:
            print("\n⚠️ No clear flag format found. Check both results above.")
            return None
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Direct text decoding
def decode_text(text):
    """Decode steganographic text directly"""
    print(f"Text loaded: {len(text)} characters")
    result1, result2 = decoder(text)
    
    if result1.startswith('ICS{') or 'ICS{' in result1:
        print(f"\n🚩 FLAG FOUND: {result1}")
        return result1
    elif result2.startswith('ICS{') or 'ICS{' in result2:
        print(f"\n🚩 FLAG FOUND: {result2}")
        return result2
    else:
        print("\n⚠️ No clear flag format found. Check both results above.")
        return None

# Main execution
if __name__ == "__main__":
    # Option 1: Decode from file
    print("="*60)
    print("Zero-Width Steganography Decoder")
    print("="*60)
    
    filename = "A5DD926E3f.txt"
    
    if os.path.exists(filename):
        decode_file(filename)
    else:
        # Option 2: Paste the text directly here
        text = """An old intelligence officer used to hide secrets in plain sight - not with ciphers,‌​‌‌​‌‌‌‌​‌​‌‌‌​‌​‌​​‌‌‌‌​​​​‌​​‌​​‌‌​‌​‌​​‌‌‌​​‌​​‌‌​‌​‌‌​​‌‌​‌‌​​‌‌​‌‌‌‌​​​‌‌​‌‌​​​‌‌​‌‌​​‌​‌‌‌‌​​‌​​‌‌​​‌‌‌​​‌‌​​‌​‌​‌‌​​‌​‌‌‌‌​​​‌‌‌‌‌​​‌​‌‌‌‌​​ but with silence. His final message looks ordinary, but those who know how to look‌‌​​‌​​‌‌‌​​‌‌​​‌​​‌‌‌​​​‌‌​‌​​‌‌​​‌‌‌​​‌‌​​‌‌​​‌‌‌‌‌‌​​‌‌​​‌​​‌‌​‌‌‌​​‌‌‌‌​‌​​‌‌​‌​‌‌​​‌‌​​‌‌​​‌​​​‌‌​​‌‌​​‌‌​​‌​‌​‌‌​​​‌‌‌‌​​‌‌‌​‌‌​​‌‌‌​‌‌​​​​​‌​ can see patterns between the letters… invisible marks that speak louder than words."""
        
        decode_text(text)
