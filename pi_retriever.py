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
                if ('PERFORMANCE INDICATORS' in line and 'GENERAL' not in line) or ('SPECIFIC' in line):
                    begin_detection = True
                elif begin_detection:
                    if line.strip() == '':
                        strikes += 1
                    if strikes == 6:
                        break
                    while True:
                        try:
                            if line != '':
                                if line[0].isnumeric():
                                    line = line[3:]
                                pi_list.write(line.strip() + '\n')
                        except:
                            line = line[1:]
                        else:
                            break
        else:
            if file not in ['pi_retriever.py', 'performance_indicators.txt']:
                print('Error: file could not be read. Proceeding to next file.')

# Normalize data
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
    for i, count in popular:
        print(f'{i[:-2]}: {count} occurrences')
    print('----------------')

# Created by Ethan Ali