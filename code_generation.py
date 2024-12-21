import json
import sys
import subprocess
import os
from optimization import constant_folding_and_simplification

def write_generated_code(generated_code, file_name="generated_script.py"):
    with open(file_name, "w") as f:
        f.write(generated_code)

def execute_generated_code(file_name="generated_script.py"):
    try:
        result = subprocess.run(
            ["python", file_name],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing generated code:\n{e.stderr}"

def cleanup_generated_file(file_name="generated_script.py"):
    if os.path.exists(file_name):
        os.remove(file_name)

def generate_code_from_ast(node):
    node_type = node.get("type")
    if not node_type:
        raise ValueError("Node is missing a 'type' key.")
    
    children = node.get("children", [])
    
    if node_type == "VAL":
        return str(node.get("value", 0))  
    elif node_type == "ID":
        return node.get("value", "x") 
    elif node_type in {"MULTIPLY", "PLUS", "MINUS", "POWER", "EQUAL"}:
        if len(children) != 2:
            raise ValueError(f"Node type '{node_type}' must have exactly two children.")
        left = generate_code_from_ast(children[0])
        right = generate_code_from_ast(children[1])
        operator = {
            "MULTIPLY": "*",
            "PLUS": "+",
            "MINUS": "-",
            "POWER": "**",
            "EQUAL": "-"
        }[node_type]
        return f"({left} {operator} {right})"
    else:
        raise ValueError(f"Unsupported node type: {node_type}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            ast_array = json.loads(sys.argv[1])
            if not isinstance(ast_array, list):
                raise ValueError("Expected an array of ASTs.")
        
            all_generated_code = []
            for i, ast in enumerate(ast_array):
                print(ast)
                optimized = constant_folding_and_simplification(ast)
                python_expression = generate_code_from_ast(optimized)

                generated_code = f"""
from solver import solve_equation

if __name__ == "__main__":
    python_expression = "{python_expression}"
    result = solve_equation(python_expression)

    print(f"Solution: {{result}}")
                """

                print("Generated Python Code:")
                print(generated_code)
                
                file_name = "generated_script.py"
                write_generated_code(generated_code, file_name)

                output = execute_generated_code(file_name)
                cleanup_generated_file(file_name)
                print("Execution Output:")
                print(output)

        except Exception as e:
            print(f"Error generating code: {e}")
    else:
        print("No AST provided. Exiting...")
