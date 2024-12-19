import json
import sys
import subprocess
import os

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

def optimize_ast(node):
    if not node or not isinstance(node, dict):
        return node

    node_type = node.get("type")
    children = node.get("children", [])

    # Recursively optimize children
    optimized_children = [optimize_ast(child) for child in children]
    node["children"] = optimized_children

    if node_type == "PLUS":
        if optimized_children[0]["type"] == "VAL" and optimized_children[0]["value"] == "0":
            return optimized_children[1]  # 0 + x -> x
        if optimized_children[1]["type"] == "VAL" and optimized_children[1]["value"] == "0":
            return optimized_children[0]  # x + 0 -> x
        if optimized_children[0]["type"] == "VAL" and optimized_children[1]["type"] == "VAL":
            left = int(optimized_children[0]["value"])
            right = int(optimized_children[1]["value"])
            return {"type": "VAL", "value": str(left + right), "children": []}

    elif node_type == "MULTIPLY":
        if optimized_children[0]["type"] == "VAL" and optimized_children[0]["value"] == "1":
            return optimized_children[1]  # 1 * x -> x
        if optimized_children[1]["type"] == "VAL" and optimized_children[1]["value"] == "1":
            return optimized_children[0]  # x * 1 -> x
        if optimized_children[0]["type"] == "VAL" and optimized_children[0]["value"] == "0":
            return {"type": "VAL", "value": "0", "children": []}  # x * 0 -> 0
        if optimized_children[1]["type"] == "VAL" and optimized_children[1]["value"] == "0":
            return {"type": "VAL", "value": "0", "children": []}  # 0 * x -> 0
        if optimized_children[0]["type"] == "VAL" and optimized_children[1]["type"] == "VAL":
            left = int(optimized_children[0]["value"])
            right = int(optimized_children[1]["value"])
            return {"type": "VAL", "value": str(left * right), "children": []}

    elif node_type == "MINUS":
        if optimized_children[1]["type"] == "VAL" and optimized_children[1]["value"] == "0":
            return optimized_children[0]  # x - 0 -> x
        if optimized_children[0]["type"] == "VAL" and optimized_children[1]["type"] == "VAL":
            left = int(optimized_children[0]["value"])
            right = int(optimized_children[1]["value"])
            return {"type": "VAL", "value": str(left - right), "children": []}
    
    elif node_type == "POWER":
        if optimized_children[0]["type"] == "VAL" and optimized_children[0]["value"] == "1":
            return {"type": "VAL", "value": "1", "children": []}  # 1 ^ x -> 1
        if optimized_children[1]["type"] == "VAL" and optimized_children[1]["value"] == "1":
            return optimized_children[1]  # x ^ 1 -> x
        if optimized_children[0]["type"] == "VAL" and optimized_children[0]["value"] == "0":
            return {"type": "VAL", "value": "0", "children": []}  # 0 ^ x -> 0
        if optimized_children[1]["type"] == "VAL" and optimized_children[1]["value"] == "0":
            return {"type": "VAL", "value": "1", "children": []}  # x ^ 0 -> 1
        if optimized_children[0]["type"] == "VAL" and optimized_children[1]["type"] == "VAL":
            left = int(optimized_children[0]["value"])
            right = int(optimized_children[1]["value"])
            return {"type": "VAL", "value": str(left ** right), "children": []}

    elif node_type == "DIVIDE":
        if optimized_children[1]["type"] == "VAL" and optimized_children[1]["value"] == "1":
            return optimized_children[0]  # x / 1 -> x
        if optimized_children[0]["type"] == "VAL" and optimized_children[1]["type"] == "VAL":
            left = int(optimized_children[0]["value"])
            right = int(optimized_children[1]["value"])
            return {"type": "VAL", "value": str(left // right), "children": []}  

    elif node_type == "MODULO":
        if optimized_children[1]["type"] == "VAL" and optimized_children[1]["value"] == "1":
            return {"type": "VAL", "value": "0", "children": []} 
        if optimized_children[0]["type"] == "VAL" and optimized_children[1]["type"] == "VAL":
            left = int(optimized_children[0]["value"])
            right = int(optimized_children[1]["value"])
            return {"type": "VAL", "value": str(left % right), "children": []}
    
    elif node_type == "EQUAL":
        return {"type": "EQUAL", "children": optimized_children}

    elif node_type == "VAL":
        return node
    
    return node

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
            ast = json.loads(sys.argv[1])
            optimized = optimize_ast(ast)
            python_expression = generate_code_from_ast(optimized)

            generated_code = f"""
from solver import solve_equation

if __name__ == "__main__":
    python_expression = "{python_expression}"
    real_roots, complex_roots = solve_equation(python_expression)

    print("Solutions:")
    print(f"Real Roots: {{real_roots}}")
    print(f"Complex Roots: {{complex_roots}}")
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
