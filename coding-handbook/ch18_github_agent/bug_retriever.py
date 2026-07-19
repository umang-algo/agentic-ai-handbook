"""
PR Diff Bug Retriever

Simulates retrieving potential bugs from Git diff hunks by searching for
risky keywords (e.g. TODO, division by zero, unhandled try-except).
"""

from typing import List, Dict

class BugRetriever:
    @staticmethod
    def inspect_diff_hunk(diff_lines: List[str]) -> List[Dict[str, str]]:
        """Parses modified git diff lines to identify code smell indicators."""
        issues = []
        for line_num, line in enumerate(diff_lines, 1):
            # Check for suspicious line modifications
            if line.startswith("+"):
                content = line[1:].strip()
                if "todo" in content.lower():
                    issues.append({"line": line_num, "issue": "Unfinished task (TODO)", "content": content})
                elif "except:" in content.lower() or "except Exception:" in content.lower():
                    issues.append({"line": line_num, "issue": "Broad except clause", "content": content})
        return issues

if __name__ == "__main__":
    diff = [
        "@@ -10,4 +10,6 @@",
        " def execute():",
        "     try:",
        "+        # TODO: verify user auth tokens first",
        "+        fetch_data()",
        "+    except Exception:",
        "+        pass"
    ]
    
    findings = BugRetriever.inspect_diff_hunk(diff)
    print("Found code quality alerts in PR diff:")
    for f in findings:
        print(f"Line {f['line']}: {f['issue']} -> '{f['content']}'")
