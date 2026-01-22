import sys
import argparse

# We define the functions but delay imports to avoid CLI hijacking by ManimGL
def convert(number, base, target_base, animate=True, show_table=True):
    from base10 import convert_base10_to_n, convert_n_to_base10
    from binarybases import (
        convert_base2_to_n,
        convert_base_n_to_2,
        convert_base_n_to_n,
    )
    
    if base == 10:
        return convert_base10_to_n(number, target_base, animation=animate)
       
    if target_base == 10:
       return convert_n_to_base10(number, base, animation=animate)
        
    if base == 2:
        return convert_base2_to_n(number, target_base, animation=animate, show_table=show_table)

    if target_base == 2:
        return convert_base_n_to_2(number, base, animation=animate, show_table=show_table)

    if base in [2, 4, 8, 16] and target_base in [2, 4, 8, 16]:
        return convert_base_n_to_n(number, base, target_base, animation=animate, show_table=show_table)

    raise ValueError("conversion between the specified bases is not supported.")

def logic_operation(a, b, base, operation, animate=True, show_table=True):
    from logic import and_logic, or_logic, xor_logic
    
    if operation == "AND":
        return and_logic(a, b, base, animation=animate, show_table=show_table)
    elif operation == "OR":
        return or_logic(a, b, base, animation=animate, show_table=show_table)
    elif operation == "XOR":
        return xor_logic(a, b, base, animation=animate, show_table=show_table)
    else:
        raise ValueError("Unsupported operation. Use 'AND', 'OR', or 'XOR'.")

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
