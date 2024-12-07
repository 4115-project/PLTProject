import sys
import json
import numpy as np

class Muller:
    def __init__(self, func):
        self.func = func

    def find_root(self, x0, x1, x2, max_iter=100, tol=1e-6):
        for _ in range(max_iter):
            f0, f1, f2 = self.func(x0), self.func(x1), self.func(x2)
            h1, h2 = x1 - x0, x2 - x1
            delta1, delta2 = (f1 - f0) / h1, (f2 - f1) / h2
            a = (delta2 - delta1) / (h2 + h1)
            b = a * h2 + delta2
            c = f2

            discriminant = np.lib.scimath.sqrt(b**2 - 4 * a * c)
            discriminant = np.sqrt(discriminant) if discriminant >= 0 else np.sqrt(complex(discriminant))
        
            denom = b + discriminant if abs(b + discriminant) > abs(b - discriminant) else b - discriminant
            if denom == 0:
                raise ZeroDivisionError("Muller's method failed due to zero denominator.")
            dx = -2 * c / denom

            if np.isnan(dx) or np.isinf(dx):
                raise ValueError("Numerical instability detected.")
            
            x3 = x2 + dx
            
            if abs(dx) < tol:
                return x3

            x0, x1, x2 = x1, x2, x3

        raise ValueError("Muller's method did not converge.")

    def deflate_polynomial(self, root, tol=1e-6):
        def new_func(x):
            try:
                return self.func(x) / (x - root)
            except ZeroDivisionError:
                return 0
        return new_func

class Newton:
    def __init__(self, func, derivative):
        self.func = func
        self.derivative = derivative

    def find_root(self, x0, max_iter=100, tol=1e-6):
        x = x0
        for _ in range(max_iter):
            f_value = self.func(x)
            f_prime_value = self.derivative(x)

            if abs(f_prime_value) < tol:
                raise ZeroDivisionError("Newton's method failed due to derivative close to zero.")

            x_new = x - f_value / f_prime_value
            if abs(x_new - x) < tol:
                return x_new

            x = x_new

        raise ValueError("Newton's method did not converge.")
    
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
                    break  

            real_roots = sorted([r.real for r in all_roots if abs(r.imag) < 1e-6])
            complex_roots = sorted([r for r in all_roots if abs(r.imag) >= 1e-6], key=lambda z: (z.real, z.imag))

            print("Solutions:")
            print(f"Real Roots: {real_roots}")
            print(f"Complex Roots: {complex_roots}")

        except Exception as e:
            print(f"Error solving equation: {e}")
    else:
        print("No AST provided. Exiting...")

'''
def differentiate(func, h=1e-6):
    return lambda x: (func(x + h) - func(x - h)) / (2 * h)
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            ast = json.loads(sys.argv[1])
            equation = parse_ast(ast)
            # For demonstration, assume we have one variable 'x'
            
            # Define the function (polynomial) and its derivative
            f = equation
            f_prime = differentiate(f)

            # Use Newton's method to find the root
            root = newton_method(f, f_prime,1)
            print(f"Solution: x = {root}")
        except Exception as e:
            print(f"Error solving equation: {e}")
    else:
        print("No AST provided. Exiting...")

'''