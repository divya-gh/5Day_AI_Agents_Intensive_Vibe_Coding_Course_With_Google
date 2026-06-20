import json
import sys


def main():
    try:
        # Read the hook input from stdin
        raw_input = sys.stdin.read()

        # Try to parse as JSON first (ADK hook payloads are usually JSON structures)
        try:
            payload = json.loads(raw_input)
            command = (
                payload.get("command", "")
                or payload.get("CommandLine", "")
                or payload.get("cmd", "")
                or str(payload)
            )
        except json.JSONDecodeError:
            command = raw_input

        # Check for destructive patterns
        destructive_patterns = [
            "rm -rf /",
            "rm -rf *",
            "format ",
            "del /f",
            "rd /s",
        ]

        normalized_command = command.strip().lower()
        for pattern in destructive_patterns:
            if pattern in normalized_command:
                print(
                    f"[PRE-TOOL GATE ERROR] Destructive command detected and blocked: '{command}'"
                )
                sys.exit(1)

        # All checks passed
        sys.exit(0)
    except Exception as e:
        # Fail closed for security
        print(f"[PRE-TOOL GATE ERROR] Exception in validation script: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
