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

def fix_model(name, fix_f):
    f = f"{model_dir}/{name}.py"
    tmp_f = f"{model_dir}/{name}2.py"
    fix_file(f, tmp_f, fix_f)
    os.rename(tmp_f, f)

# search_list_rt.py
def fix_search(line):
    return line.replace("items_item = File(payload=BytesIO(items_item_data))", "items_item = items_item_data")

fix_model("search_list_rt", fix_search)
# search_f = f"{model_dir}/search_list_rt.py"
# tmp_f = f"{model_dir}/search_list_rt2.py"
# fix_file(search_f, tmp_f, fix_search)
# os.rename(tmp_f, search_f)

# service_status_rt.py
def fix_controller(line):
    line = line.replace('controller = File(payload=BytesIO(d.pop("controller")))', 'controller = d.pop("controller")')
    return line.replace('controller = self.controller.to_tuple()', 'controller = self.controller')

fix_model("service_status_rt", fix_controller)

def fix_job_status(line):
    line = line.replace('request_content: Union[Unset, File]', 'request_content: Union[Unset, Any]')
    line = line.replace('request_content = File(payload=BytesIO(_request_content))', 'request_content = _request_content')

    line = line.replace('result_content: Union[Unset, File]', 'result_content: Union[Unset, Any]')
    line = line.replace('result_content = File(payload=BytesIO(_result_content))', 'result_content = _result_content')

    line = line.replace('request_content: Union[Unset, FileJsonType] = UNSET', 'request_content: Union[Unset, Any] = UNSET')
    line = line.replace('request_content = self.request_content.to_tuple()', 'request_content = self.request_content')

    line = line.replace('result_content: Union[Unset, FileJsonType] = UNSET', 'result_content: Union[Unset, Any] = UNSET'
    line = line.replace('result_content = self.result_content.to_tuple()', 'result_content = self.result_content')
    return line

fix_model("job_status_rt", fix_job_status)