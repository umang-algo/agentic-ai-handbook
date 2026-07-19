"""
Myers Diff Algorithm

Implements the standard Myers Diff algorithm used by modern git engines and AI IDEs
to compare two files and produce line-level edits (inserts/deletes).
"""

from typing import List, Tuple

def myers_diff(a: List[str], b: List[str]) -> List[Tuple[str, str]]:
    """
    Computes Myers Diff path.
    Returns list of tuples: (operation, line_content)
    where operation is: "keep", "insert", "delete"
    """
    N = len(a)
    M = len(b)
    MAX = N + M
    
    # DP array to track furthest reaching path for each diagonal d = x - y
    v = {1: 0}
    trace = []
    
    # Find edit distance path
    for d in range(0, MAX + 1):
        v = v.copy()
        trace.append(v)
        for k in range(-d, d + 1, 2):
            if k == -d or (k != d and v.get(k-1, -1) < v.get(k+1, -1)):
                x = v.get(k+1, -1) # Down
            else:
                x = v.get(k-1, -1) + 1 # Right
            
            y = x - k
            while x < N and y < M and a[x] == b[y]:
                x += 1
                y += 1
            v[k] = x
            if x >= N and y >= M:
                break
        else:
            continue
        break
        
    # Backtrack path
    x, y = N, M
    diff = []
    
    for d in range(len(trace) - 1, 0, -1):
        v = trace[d]
        v_prev = trace[d-1]
        k = x - y
        
        # Decide direction
        if k == -d or (k != d and v_prev.get(k-1, -1) < v_prev.get(k+1, -1)):
            k_prev = k + 1
        else:
            k_prev = k - 1
            
        x_prev = v_prev[k_prev]
        y_prev = x_prev - k_prev
        
        while x > x_prev and y > y_prev:
            diff.append(("keep", a[x-1]))
            x -= 1
            y -= 1
            
        if x > x_prev:
            diff.append(("delete", a[x-1]))
            x -= 1
        elif y > y_prev:
            diff.append(("insert", b[y-1]))
            y -= 1
            
    # Add remaining keeps at start
    while x > 0 and y > 0:
        diff.append(("keep", a[x-1]))
        x -= 1
        y -= 1
        
    diff.reverse()
    return diff

if __name__ == "__main__":
    file_a = ["import sys", "print('hello')", "sys.exit(0)"]
    file_b = ["import sys", "print('world')", "print('done')", "sys.exit(0)"]
    
    result = myers_diff(file_a, file_b)
    print("Diff:")
    for op, line in result:
        if op == "keep":
            print(f"  {line}")
        elif op == "insert":
            print(f"+ {line}")
        elif op == "delete":
            print(f"- {line}")
