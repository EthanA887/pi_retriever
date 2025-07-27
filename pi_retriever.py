import os
from pypdf import PdfReader
from collections import Counter

# Extract PIs from PDF
with open('performance_indicators.txt', 'w') as pi_list:
    for file in os.listdir():
        if file[-4:] == '.pdf':
            print(file)
            reader = PdfReader(file)
            page = reader.pages[0]
            text = page.extract_text().split('\n')
            begin_detection = False
            strikes = 0
            time = 0
            for line in text:
                """
                Start detecting only when the following phrases are seen:
                1. SPECIFIC COMPETENCIES EVALUATED
                2. SPECIFIC PERFORMANCE INDICATORS
                3. PERFORMANCE INDICATORS
                """
                if ('PERFORMANCE INDICATORS' in line and 'GENERAL' not in line) or ('SPECIFIC' in line):
                    begin_detection = True # List of PIs found
                elif begin_detection:
                    if line.strip() == '':
                        strikes += 1
                    if strikes == 5: # Max. 5 lines before the next section
                        break
                    while True:
                        try: # Attempt to parse line (the program throws an error if it detects unknown characters e.g. bullet points)
                            if line != '':
                                if line[0].isnumeric():
                                    line = line[3:]
                                pi_list.write(line.strip() + '\n')
                        except: # Remove first character
                            line = line[1:]
                        else:
                            break
        else:
            if file not in ['pi_retriever.py', 'performance_indicators.txt']:
                print('Error: file could not be read. Proceeding to next file.')

# Remove blank lines
with open('performance_indicators.txt', 'r') as file:
    lines = file.readlines()

lines = [l for l in lines if l != '\n']
with open('performance_indicators.txt', 'w') as file:
    file.writelines(lines)

# Display the most common
with open('performance_indicators.txt', 'r') as file:
    pis = file.readlines()
    print('----------------')
    print(f'Total number of PIs extracted: {len(pis)}')
    print('----------------')
    x = int(input('Number of most common PIs to display: '))
    popular = Counter(pis).most_common(x)
    print(f'Top {x} most common PIs:')
    for i, count in popular: # Enumerate over sorted results by frequency
        print(f'{i[:-2]}: {count} occurrences')
    print('----------------')
