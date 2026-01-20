import pathlib, re

root = pathlib.Path(__file__).resolve().parent
app_dir = root / "app"

# 1) 把 "T | None" / "None | T" 替换成 Optional[T]
pat_t_none = re.compile(r"\b([A-Za-z_][A-Za-z0-9_\.]*)\s*\|\s*None\b")
pat_none_t = re.compile(r"\bNone\s*\|\s*([A-Za-z_][A-Za-z0-9_\.]*)\b")

# 2) 把 Python 3.9+ 的内置泛型 list[...] dict[...] 等替换为 typing 的 List[...] Dict[...]
builtin_generics = [
    (re.compile(r"\blist\["), "List["),
    (re.compile(r"\bdict\["), "Dict["),
    (re.compile(r"\bset\["), "Set["),
    (re.compile(r"\btuple\["), "Tuple["),
]

def ensure_header(text: str, need_typing: bool) -> str:
    lines = text.splitlines()

    # 确保 future annotations 在最顶部
    if not any(l.strip() == "from __future__ import annotations" for l in lines[:5]):
        lines.insert(0, "from __future__ import annotations")

    if need_typing:
        # 确保 typing 导入
        has_optional = any("from typing import" in l and "Optional" in l for l in lines[:20])
        has_any_typing = any(l.strip().startswith("from typing import") for l in lines[:20])

        if not has_optional:
            ins = "from typing import Optional, List, Dict, Set, Tuple, Any"
            # 插在 future annotations 后面
            for i, l in enumerate(lines[:10]):
                if l.strip() == "from __future__ import annotations":
                    lines.insert(i + 1, ins)
                    break
            else:
                lines.insert(0, ins)

        # 如果已有 from typing import 但不含 Optional，也不重复合并（简单处理即可）

    return "\n".join(lines) + ("\n" if not text.endswith("\n") else "")

patched_files = 0

for f in app_dir.rglob("*.py"):
    text = f.read_text(encoding="utf-8")

    changed = False
    new = text

    if "| None" in new or "None |" in new:
        new2 = pat_t_none.sub(r"Optional[\1]", new)
        new2 = pat_none_t.sub(r"Optional[\1]", new2)
        if new2 != new:
            new = new2
            changed = True

    # builtin generics -> typing generics
    need_typing = False
    for rgx, rep in builtin_generics:
        if rgx.search(new):
            new2 = rgx.sub(rep, new)
            if new2 != new:
                new = new2
                changed = True
                need_typing = True

    # 如果出现 Optional[...] 也需要 typing 导入
    if "Optional[" in new:
        need_typing = True

    if changed:
        new = ensure_header(new, need_typing=need_typing)
        f.write_text(new, encoding="utf-8")
        print("patched:", f.relative_to(root))
        patched_files += 1

print("done. files patched =", patched_files)
