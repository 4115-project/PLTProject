import json
import sys
import subprocess
import os

def constant_folding_and_simplification(node):
    if not node or not isinstance(node, dict):
        return node

    node_type = node.get("type")
    children = node.get("children", [])

    # Recursively optimize children
    optimized_children = [constant_folding_and_simplification(child) for child in children]
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
