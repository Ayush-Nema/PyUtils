import filecmp
import hashlib
from deepdiff import DeepDiff
import difflib
import json

f1 = "logging_0.json"
f2 = "logging_1.json"

# ====================== 1st way to compare the files: `filecmp` library ======================
# shallow comparison
result = filecmp.cmp(f1, f2)
print(result)
# deep comparison
result = filecmp.cmp(f1, f2, shallow=False)
print(result)


# ====================== 2nd way of comparing the files: Generating MD5 hash ======================
# Ref:
# Apply MD5 hashing: https://debugpointer.com/python/create-md5-hash-of-a-file-in-python
# Primer about hashing algos: https://kinsta.com/blog/python-hashing/
def read_json(file_path):
    with open(file_path, "r") as fp:
        data = json.load(fp)
    return data


f1_data, f2_data = read_json(f1), read_json(f2)

# Convert dictionaries to JSON strings and then encode as bytes
f1_data_bytes = json.dumps(f1_data, sort_keys=True).encode('utf-8')
f2_data_bytes = json.dumps(f2_data, sort_keys=True).encode('utf-8')

f1_data_md5hash = hashlib.md5(f1_data_bytes).hexdigest()
f2_data_md5hash = hashlib.md5(f2_data_bytes).hexdigest()
print(f"Hash for f1: {f1_data_md5hash} \nHash for f2: {f2_data_md5hash}")

if f1_data_md5hash == f2_data_md5hash:
    print("Both the files are same")
else:
    print("Files are different")


# ========================= Identifying the location of change ===============================
def compare_json_files(file1, file2):
    json_data1 = read_json(file1)
    json_data2 = read_json(file2)

    # Use DeepDiff to find differences
    diff = DeepDiff(json_data1, json_data2)

    if not diff:
        print("JSON files are identical.")
    else:
        print("Differences found:")
        print(diff)


compare_json_files(f1, f2)


# ============== other approach for locating the changes ================
lines1 = json.dumps(f1_data).split(",")
lines2 = json.dumps(f2_data).split(",")

a = list(difflib.unified_diff(lines1, lines2, fromfile='file1', tofile='file2', lineterm=''))
print(a)
print(len(a))

# for line in difflib.unified_diff(lines1, lines2, fromfile='file1', tofile='file2', lineterm=''):
#     print(line)
#     print("---------")
