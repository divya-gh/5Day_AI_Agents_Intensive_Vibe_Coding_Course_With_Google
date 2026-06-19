import yaml
import json
import traceback

def run_debug():
    config_path = "tests/eval/eval_config.yaml"
    traces_path = "artifacts/traces/generated_traces.json"
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    with open(traces_path, "r", encoding="utf-8") as f:
        traces = json.load(f)
        
    custom_metrics = {m["name"]: m["custom_function"] for m in config.get("custom_metrics", []) if "custom_function" in m}
    
    for metric_name, code in custom_metrics.items():
        print(f"\n======================================")
        print(f"Debugging Custom Metric: {metric_name}")
        print(f"======================================")
        
        # Compile the custom function
        namespace = {}
        try:
            exec(code, namespace)
            evaluate_fn = namespace["evaluate"]
        except Exception as e:
            print(f"Compilation error for {metric_name}:")
            traceback.print_exc()
            continue
            
        # Run on each case
        for case in traces["eval_cases"]:
            case_id = case["eval_case_id"]
            print(f"Running on case {case_id}...")
            try:
                res = evaluate_fn(case)
                print(f"  Result: {res}")
            except Exception as e:
                print(f"  Error on case {case_id}:")
                traceback.print_exc()

if __name__ == "__main__":
    run_debug()
