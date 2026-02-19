from typing import TypedDict


class LanguageMeta(TypedDict):
    extension: str
    template: str
    cf_keywords: list[str]


LANGUAGES: dict[str, LanguageMeta] = {
    "cpp": {
        "extension": "cpp",
        "template": "#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    return 0;\n}\n",
        "cf_keywords": ["GNU G++20", "GNU G++17", "GNU C++20", "GNU C++17", "GNU C++"],
    },
    "c": {
        "extension": "c",
        "template": "#include <stdio.h>\n\nint main() {\n\n    return 0;\n}\n",
        "cf_keywords": ["GNU C11", "GNU C17", "GNU C"],
    },
    "java": {
        "extension": "java",
        "template": "import java.io.*;\nimport java.util.*;\n\npublic class Main {\n    public static void main(String[] args) throws Exception {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n        PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));\n\n        out.flush();\n    }\n}\n",
        "cf_keywords": ["Java 21", "Java 17", "Java 11", "Java 8", "Java"],
    },
    "python": {
        "extension": "py",
        "template": "import sys\n\n\ndef solve() -> None:\n    pass\n\n\nif __name__ == \"__main__\":\n    solve()\n",
        "cf_keywords": ["PyPy 3", "Python 3", "PyPy"],
    },
}


EXTENSION_TO_LANGUAGE = {
    ".cpp": "cpp",
    ".c": "c",
    ".java": "java",
    ".py": "python",
}
