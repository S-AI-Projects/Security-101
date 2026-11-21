"""
Client Configuration Validator and Redaction Reporter (Task R34-T009)
Validates server-launch configuration (command, args array, env dict)
and produces a redacted summary report without launching the process.
"""
import sys
import json
import time
import argparse

def validate_and_redact_config(config):
    """
    Validates server configuration:
      - command: must be non-empty string
      - args: must be a list of strings
      - env: optional dict with environment key/values
    Produces a safe redacted summary. Never launches the process.
    """
    if not isinstance(config, dict):
        return {"status": "FAIL", "error": "Configuration must be a dictionary object."}

    # Check command
    command = config.get("command")
    if not command or not isinstance(command, str) or not command.strip():
        return {"status": "FAIL", "error": "Missing or invalid 'command' field."}

    # Check args (must be list, not a single string)
    args = config.get("args")
    if args is None or not isinstance(args, list):
        return {
            "status": "FAIL",
            "error": "Argument array required: 'args' must be a list of strings, not a single string or missing."
        }

    for arg in args:
        if not isinstance(arg, str):
            return {"status": "FAIL", "error": "All items in 'args' must be strings."}

    # Process and redact environment variables
    env = config.get("env", {})
    if not isinstance(env, dict):
        return {"status": "FAIL", "error": "'env' must be a dictionary."}

    redacted_env = {}
    for key, val in env.items():
        redacted_env[key] = "[REDACTED]"

    return {
        "status": "PASS",
        "validated_configuration": {
            "command": command.strip(),
            "args": args,
            "environment_keys": list(env.keys()),
            "redacted_env": redacted_env
        },
        "process_launched": False
    }

def run_evaluation_experiment():
    """
    Compares three small controlled configurations using validation time and status.
    """
    configs = {
        "small": {"command": "python3", "args": ["-m", "http.server"], "env": {"PORT": "8080"}},
        "medium": {"command": "node", "args": ["server.js", "--prod"], "env": {"PORT": "3000", "SECRET_KEY": "abc", "DB": "mysql"}},
        "large": {"command": "app_server", "args": ["--workers", "4", "--timeout", "30"], "env": {f"VAR_{i}": f"val_{i}" for i in range(15)}}
    }
    
    experiment_results = {}
    for name, cfg in configs.items():
        t0 = time.perf_counter()
        res = validate_and_redact_config(cfg)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        experiment_results[name] = {
            "status": res["status"],
            "env_key_count": len(cfg["env"]),
            "process_launched": res["process_launched"],
            "validation_time_ms": round(elapsed_ms, 4)
        }
    return experiment_results

def main():
    parser = argparse.ArgumentParser(description="Client Configuration Validator")
    parser.add_argument("--mode", choices=["valid", "missing_cmd", "string_args", "experiment"], default="valid")
    args = parser.parse_args()

    if args.mode == "experiment":
        print(json.dumps(run_evaluation_experiment(), indent=2))
    elif args.mode == "valid":
        cfg = {"command": "uvicorn", "args": ["main:app", "--port", "8000"], "env": {"API_TOKEN": "secret123", "ENV": "prod"}}
        print(json.dumps(validate_and_redact_config(cfg), indent=2))
    elif args.mode == "missing_cmd":
        cfg = {"command": "", "args": ["main.py"]}
        print(json.dumps(validate_and_redact_config(cfg), indent=2))
    elif args.mode == "string_args":
        cfg = {"command": "python3", "args": "main.py --port 8000"}  # Single string instead of array
        print(json.dumps(validate_and_redact_config(cfg), indent=2))

if __name__ == "__main__":
    main()
