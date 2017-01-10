import re
import logging

logger = logging.getLogger("Parsing")


def create_node(data):
    tag_part = r"(?P<tag>\w+)"
    attr_part = r"(?P<q>\[(?P<attr>\w+)=(\"|\')(?P<val>.+?)(\"|\')\])?"
    selector_part = r"(\{(?P<selector>\d+)\})?"
    p = tag_part + attr_part + selector_part
    patt = re.compile(p)

    m = patt.match(data)
    tag = m.group("tag")

    if m.group("q"):
        q = {m.group("attr"): m.group("val")}
    else:
        q = None

    def selector(lst):
        s = m.group("selector")
        if s:
            sel = int(s)
            return [lst[sel]] if sel < len(lst) else []
        else:
            return lst

    def node(root):
        return selector(root.findAll(tag, q))

    return node


def parse(key, paths, context):
    path = paths.pop()
    results = []

    for node in context:
        for out in path(node):
            results.append(out)

    if len(paths) == 0:
        # End of line
        return [(key, result.text, result.attrs)
                for result in results]
    else:
        return parse(key, paths, results)
