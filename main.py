import sys
import argparse
import os
import json

CACHE_FILE = "scene_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

def get_cache_key(command, **params):
    return f"{command}_{json.dumps(params, sort_keys=True)}"

def get_predicted_path(command, **params):
    """Predicts the output file path based on command parameters."""
    animate = params.get("animate", True)
    if command == "convert":
        number = params.get("number")
        base = params.get("base")
        target_base = params.get("target_base")
        if animate:
            # ManimGL default output for video
            return os.path.join("videos", "main", "1080p30", f"{number}-B{base}_to_B{target_base}.mp4")
        else:
            # Custom image output path in base10.py and binarybases.py
            return os.path.join("images", f"{number}-B{base}_to_B{target_base}.png")
    elif command == "logic":
        a = params.get("a")
        b = params.get("b")
        base = params.get("base")
        op = params.get("operation")
        if animate:
            # OR vs XOR vs AND in logic.py use different name formats
            fname = f"{op}_{a}_{b}_B{base}" if op != "AND" else f"AND-{a}-{b}-B{base}"
            return os.path.join("videos", "main", "1080p30", f"{fname}.mp4")
        else:
            fname = f"{op}{a}-{b}-B{base}"
            return os.path.join("images", f"{fname}.png")
    return None

# We define the functions but delay imports to avoid CLI hijacking by ManimGL
def convert(number, base, target_base, animate=True, show_table=True):
    params = {"number": str(number), "base": base, "target_base": target_base, "animate": animate, "show_table": show_table}
    cache = load_cache()
    key = get_cache_key("convert", **params)
    
    if key in cache:
        path = cache[key]
        if os.path.exists(path):
            print(f"Using cached result: {path}")
            return path
    
    from base10 import convert_base10_to_n, convert_n_to_base10
    from binarybases import (
        convert_base2_to_n,
        convert_base_n_to_2,
        convert_base_n_to_n,
    )
    
    if base == 10:
        convert_base10_to_n(number, target_base, animation=animate)
    elif target_base == 10:
        convert_n_to_base10(number, base, animation=animate)
    elif base == 2:
        convert_base2_to_n(number, target_base, animation=animate, show_table=show_table)
    elif target_base == 2:
        convert_base_n_to_2(number, base, animation=animate, show_table=show_table)
    elif base in [2, 4, 8, 16] and target_base in [2, 4, 8, 16]:
        convert_base_n_to_n(number, base, target_base, animation=animate, show_table=show_table)
    else:
        raise ValueError("conversion between the specified bases is not supported.")

    path = get_predicted_path("convert", **params)
    if path:
        cache[key] = path
        save_cache(cache)
    return path

def logic_operation(a, b, base, operation, animate=True, show_table=True):
    params = {"a": str(a), "b": str(b), "base": base, "operation": operation, "animate": animate, "show_table": show_table}
    cache = load_cache()
    key = get_cache_key("logic", **params)

    if key in cache:
        path = cache[key]
        if os.path.exists(path):
            print(f"Using cached result: {path}")
            return path

    from logic import and_logic, or_logic, xor_logic
    
    if operation == "AND":
        and_logic(a, b, base, animation=animate, show_table=show_table)
    elif operation == "OR":
        or_logic(a, b, base, animation=animate, show_table=show_table)
    elif operation == "XOR":
        xor_logic(a, b, base, animation=animate, show_table=show_table)
    else:
        raise ValueError("Unsupported operation. Use 'AND', 'OR', or 'XOR'.")

    path = get_predicted_path("logic", **params)
    if path:
        cache[key] = path
        save_cache(cache)
    return path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Base Converter and Logic Operations CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: convert
    convert_parser = subparsers.add_parser("convert", help="Convert numbers between bases")
    convert_parser.add_argument("number", help="The number to convert")
    convert_parser.add_argument("base", type=int, help="Source base")
    convert_parser.add_argument("target_base", type=int, help="Target base")
    convert_parser.add_argument("--no-animate", action="store_false", dest="animate", help="Disable animation")
    convert_parser.add_argument("--no-table", action="store_false", dest="show_table", help="Disable table display")
    convert_parser.set_defaults(animate=True, show_table=True)

    # Command: logic
    logic_parser = subparsers.add_parser("logic", help="Perform logic operations")
    logic_parser.add_argument("a", help="First number")
    logic_parser.add_argument("b", help="Second number")
    logic_parser.add_argument("base", type=int, help="Base of the numbers")
    logic_parser.add_argument("operation", choices=["AND", "OR", "XOR"], help="Logic operation")
    logic_parser.add_argument("--no-animate", action="store_false", dest="animate", help="Disable animation")
    logic_parser.add_argument("--no-table", action="store_false", dest="show_table", help="Disable table display")
    logic_parser.set_defaults(animate=True, show_table=True)

    # We need to parse our arguments and THEN clear sys.argv so ManimGL doesn't complain
    args = parser.parse_args()
    
    # Store original argv if needed, but for now just clear it for Manim
    sys.argv = [sys.argv[0]]

    if args.command == "convert":
        convert(args.number, args.base, args.target_base, animate=args.animate, show_table=args.show_table)
    elif args.command == "logic":
        logic_operation(args.a, args.b, args.base, args.operation, animate=args.animate, show_table=args.show_table)
    else:
        parser.print_help()
