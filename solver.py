import numpy as np
import cmath
import json
import sys

def parse_ast(node):
    node_type = node["type"]
    children = node.get("children", [])
    
    if node_type == "VAL":
        return lambda x: float(node["value"])
    elif node_type == "ID":
        return lambda x: x
    elif node_type == "MULTIPLY":
        return lambda x: parse_ast(children[0])(x) * parse_ast(children[1])(x)
    elif node_type == "PLUS":
        return lambda x: parse_ast(children[0])(x) + parse_ast(children[1])(x)
    elif node_type == "MINUS":
        return lambda x: parse_ast(children[0])(x) - parse_ast(children[1])(x)
    elif node_type == "POWER":
        return lambda x: parse_ast(children[0])(x) ** parse_ast(children[1])(x)
    elif node_type == "EQUAL":
        lhs = parse_ast(children[0])
        rhs = parse_ast(children[1])
        return lambda x: lhs(x) - rhs(x)
    else:
        raise ValueError(f"Unsupported node type: {node_type}")


def muller_method(func, x0, x1, x2, max_iter=100, tol=1e-6):
    for iteration in range(max_iter):
        f0, f1, f2 = func(x0), func(x1), func(x2)
        if abs(f2) < tol: return x2
        
        h1, h2 = x1 - x0, x2 - x1
        delta1, delta2 = (f1 - f0) / h1, (f2 - f1) / h2
        a = (delta2 - delta1) / (h2 + h1)
        b = a * h2 + delta2
        c = f2

        discriminant = np.lib.scimath.sqrt(b**2 - 4 * a * c) 
        denom = b + discriminant if abs(b + discriminant) > abs(b - discriminant) else b - discriminant
        if abs(denom) < 1e-12:  
            x2 += 1e-6
            continue
        
        dx = -2 * c / denom
        x3 = x2 + dx

        if abs(dx) < tol:
            return x3

        x0, x1, x2 = x1, x2, x3

    raise ValueError("Muller's method did not converge.")


def deflate_polynomial(func, root, tol=1e-6):
    def new_func(x):
        value = func(x)
        correction = x - root
        if abs(correction) < tol:
            return 0
        return value / correction
    return new_func

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            ast = json.loads(sys.argv[1])
            equation = parse_ast(ast)
            f = equation
            all_roots = []
            guesses = [0, 1, -1]  
            max_degree = 10  

            while len(all_roots) < max_degree:
                try:
                    root = muller_method(f, *guesses)
                    if all(abs(root - r) > 1e-6 for r in all_roots):
                        all_roots.append(root)
                        f = deflate_polynomial(f, root)
                    else:
                        break
                except Exception as e:
                    print(f"Stopping root finding: {e}")
                    break

            real_roots = sorted([r.real for r in all_roots if abs(r.imag) < 1e-6])
            complex_roots = sorted(
                [r for r in all_roots if abs(r.imag) >= 1e-6], key=lambda z: (z.real, z.imag)
            )

            print("Solutions:")
            print(f"Real Roots: {real_roots}")
            print(f"Complex Roots: {complex_roots}")

        except Exception as e:
            print(f"Error solving equation: {e}")
    else:
        print("No AST provided. Exiting...")
