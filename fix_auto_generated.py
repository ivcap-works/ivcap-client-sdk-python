import os
import fnmatch

def fix_file(orig, newn):
    #print(f"{orig} -> {newn} ")
    f = open(orig, "r")
    copy = open(newn, "w")
    for line in f:
        line = line.replace("json_body: File", "json_body: Dict")
        line = line.replace("json_json_body = json_body.to_tuple()", "json_json_body = json_body")
        line = line.replace("json_body (File):", "json_body (Dict):")
        copy.write(line)
    f.close()
    copy.close()
    os.unlink(orig)

api_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'build/sdk_client/ivcap_client/api')
for root, dir, files in os.walk(api_dir):
    svc = root.split("/")[-1]
    #print(f"dir: {svc}:{root}")
    for el in fnmatch.filter(files, f"{svc}*.py"):
        orig = f"{root}/{el}"
        newn = f"{root}/{svc}_{el[len(svc):]}"
        fix_file(orig, newn)
        