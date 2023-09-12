import csv
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt


def normalize(str):
    return str.replace('-', '-').replace('‐', '-')


sciscore_hashes = []  # "hash" here means a string that combines the PMCID and tool name
for row in csv.reader(open('sciscore_software_tools.csv', 'r')):
    if row[0] != 'PMCID':
        sciscore_hashes.append(row[0] + normalize(row[1]))
softcite_hashes = []
for row in csv.reader(open('softcite_software_tools.csv', 'r')):
    if row[0] != 'article_pmcid' and row[1].strip() != '':
        softcite_hashes.append(row[0] + normalize(row[1]))
full_list = list(set(sciscore_hashes + softcite_hashes))
agreements = set(sciscore_hashes).intersection(softcite_hashes)
disagreements = set(sciscore_hashes).symmetric_difference(softcite_hashes)
hash_to_decision = {}
for row in csv.reader(open('software_disagreements.csv', 'r')):
    if row[3] == '' or row[3] == 'Undecidable ':
        try:
            full_list.remove(row[0] + normalize(row[1]))
            disagreements.remove(row[0] + normalize(row[1]))
            continue
        except:
            continue
    hash_to_decision[row[0] + normalize(row[1])] = row[3] == 'Yes'
print(len(agreements), len(disagreements), len(full_list))
real = []
sciscore = []
softcite = []
for h in full_list:
    if h in agreements:
        real.append(True)
    elif h in disagreements:
        real.append(hash_to_decision[h])
        # uncomment to look at individual examples
        # if hash_to_decision[h] and h not in softcite_hashes:
        #     print(h)
    sciscore.append(h in sciscore_hashes)
    softcite.append(h in softcite_hashes)
real = np.array(real)
sciscore = np.array(sciscore)
softcite = np.array(softcite)


from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

print(accuracy_score(real, softcite))
print(precision_score(real, softcite))
print(recall_score(real, softcite))
print(f1_score(real, softcite))

cm = confusion_matrix(real, softcite)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
# plt.show()