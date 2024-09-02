import os
import fnmatch

api_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'build/sdk_client/ivcap_client/api')
model_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'build/sdk_client/ivcap_client/models')

def fix_file(orig, newn, fix_line_f):
    #print(f"{orig} -> {newn} ")
    f = open(orig, "r")
    copy = open(newn, "w")
    for line in f:
        line = fix_line_f(line)
        # line = line.replace("json_body: File", "json_body: Dict")
        # line = line.replace("json_json_body = json_body.to_tuple()", "json_json_body = json_body")
        # line = line.replace("json_body (File):", "json_body (Dict):")
        copy.write(line)
    f.close()
    copy.close()
    os.unlink(orig)

def fix_api(line):
    line = line.replace("json_body: File", "json_body: Dict")
    line = line.replace("json_json_body = json_body.to_tuple()", "json_json_body = json_body")
    line = line.replace("json_body (File):", "json_body (Dict):")
    return line

for root, dir, files in os.walk(api_dir):
    svc = root.split("/")[-1]
    #print(f"dir: {svc}:{root}")
    for el in fnmatch.filter(files, f"{svc}*.py"):
        orig = f"{root}/{el}"
        newn = f"{root}/{svc}_{el[len(svc):]}"
        fix_file(orig, newn, fix_api)

# search_list_rt.py
def fix_search(line):
    return line.replace("items_item = File(payload=BytesIO(items_item_data))", "items_item = items_item_data")

search_f = f"{model_dir}/search_list_rt.py"
tmp_f = f"{model_dir}/search_list_rt2.py"
fix_file(search_f, tmp_f, fix_search)
os.rename(tmp_f, search_f)