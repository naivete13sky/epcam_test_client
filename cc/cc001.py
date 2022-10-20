import os
with open(r"C:\cc\share\temp_2063_1666246568\g_compare_result\w-sm2.txt", 'r') as f:
    comp_result_text = f.readlines()[0].split(" ")[-1].strip()
print(comp_result_text)
print(len(comp_result_text))

print("comp_result_text:", comp_result_text)
print("comp_result_text == 'no'?", comp_result_text == 'no')
assert comp_result_text == 'no'
