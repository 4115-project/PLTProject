import sys
import json
import numpy as np

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
    for _ in range(max_iter):
        f0, f1, f2 = func(x0), func(x1), func(x2)
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

def deflate_polynomial(func, root, tol=1e-6):
    def new_func(x):
        try:
            return func(x) / (x - root)
        except ZeroDivisionError:
            return 0
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




'''import sys
import json
import numpy as np

    
def parse_ast(node):
    """Recursively parse the AST and build the equation."""
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
    """Find a root using Muller's method."""
    for _ in range(max_iter):
        f0, f1, f2 = func(x0), func(x1), func(x2)
        h1, h2 = x1 - x0, x2 - x1
        delta1, delta2 = (f1 - f0) / h1, (f2 - f1) / h2
        a = (delta2 - delta1) / (h2 + h1)
        b = a * h2 + delta2
        c = f2

        discriminant = np.sqrt(b**2 - 4 * a * c)
        if discriminant < 0:
            discriminant = complex(discriminant)  
        discriminant = np.sqrt(discriminant)

        denom = b + discriminant if abs(b + discriminant) > abs(b - discriminant) else b - discriminant
        if denom == 0:
            raise ZeroDivisionError("Muller's method failed due to zero denominator.")
        dx = -2 * c / denom
        x3 = x2 + dx

        if abs(dx) < tol:
            return x3

        x0, x1, x2 = x1, x2, x3

    raise ValueError("Muller's method did not converge.")

def deflate_polynomial(func, root, tol=1e-6):
    """Deflate the polynomial after finding a root."""
    def new_func(x):
        return func(x) / (x - root) if abs(x - root) > tol else 0
    return new_func

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            ast = json.loads(sys.argv[1])
      
            equation = parse_ast(ast)

            # Convert equation into a callable function
            f = equation
            all_roots = []
            guesses = [0, 1, -1]  # Initial guesses for Muller's method

            while len(all_roots) < 6:  # Up to 6 roots for a degree-6 polynomial
                try:
                    root = muller_method(f, *guesses)
                    if all(abs(root - r) > 1e-6 for r in all_roots):  # Avoid duplicate roots
                        all_roots.append(root)
                        f = deflate_polynomial(f, root)  # Deflate the polynomial
                except Exception as e:
                    break  # Stop if no more roots can be found

            # Separate real and complex roots for clarity
            real_roots = [r for r in all_roots if abs(r.imag) < 1e-6]
            complex_roots = [r for r in all_roots if abs(r.imag) >= 1e-6]

            print("Solutions:")
            print(f"Real Roots: {real_roots}")
            print(f"Complex Roots: {complex_roots}")

        except Exception as e:
            print(f"Error solving equation: {e}")
    else:
        print("No AST provided. Exiting...")
'''

'''
import sys
import json

def parse_ast(node):
    """Recursively parse the AST and build the equation."""
    node_type = node["type"]
    children = node.get("children", [])
    
    if node_type == "VAL":
        return lambda x: int(node["value"])
    elif node_type == "ID":
        return lambda x: x  # Variable 'x'
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
        return lambda x: lhs(x) - rhs(x)  # Return the difference for equality
    else:
        raise ValueError(f"Unsupported node type: {node_type}")

def newton_method(func, func_derivative, x0, max_iter=100, tol=1e-6):
    x = x0
    for _ in range(max_iter):
        f_value = func(x)
        f_prime_value = func_derivative(x)
        
        # Check if the derivative is close to zero
        if abs(f_prime_value) < tol:
            print("Warning: Derivative is close to zero. Trying a different guess.")
            return None  # or return a new guess or handle it differently
        
        x_new = x - f_value / f_prime_value
        
        if abs(x_new - x) < tol:
            return x_new
        
        x = x_new
    return x

# You could call this method in your solver, with appropriate functions for the equation and its derivative

def differentiate(f):
    """Numerically differentiate the function f."""
    h = 1e-6
    return lambda x: (f(x + h) - f(x - h)) / (2 * h)

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