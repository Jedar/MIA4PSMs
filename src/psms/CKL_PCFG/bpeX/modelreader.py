import os
import re
import sys
from collections import defaultdict
from typing import Dict, Tuple, Any


def check_path_exists(_path: str):
    if not os.path.exists(_path):
        print(f"{_path} not exists, exit.", file=sys.stderr)
        sys.exit(-1)
    pass


def read_tag(tag_path: str, tag: str) -> Dict[Tuple[str, int], Dict[str, float]]:
    check_path_exists(tag_path)
    tag_dict = defaultdict(lambda: defaultdict(float))
    for root, dirs, files in os.walk(tag_path):
        for file in files:
            dot_idx = file.find(".")
            tag_len = (tag, int(file[:dot_idx]))
            fd = open(os.path.join(root, file))
            for line in fd:
                _tag, prob = line.strip("\r\n").split("\t")
                tag_dict[tag_len][_tag] = float(prob)
            fd.close()
    return tag_dict


def read_grammars(gram_path: str):
    fd = open(gram_path)
    structure_prob_dict = {}
    re_tag_len = re.compile(r"([A-Z]+[0-9]+)")
    re_tag = re.compile(r"[A-Z]+")
    re_len = re.compile(r"[0-9]+")
    for line in fd:
        raw_structure, prob = line.strip("\r\n").split("\t")
        structure = tuple(
            [(re_tag.search(t).group(), int(re_len.search(t).group())) for t in re_tag_len.split(raw_structure) if
             len(t) > 0])
        structure_prob_dict[structure] = float(prob)

    fd.close()
    return structure_prob_dict


def read_bpe(model_path: str) -> Tuple[Dict[Any, float], Dict[Tuple[str, int], Dict[Any, float]]]:
    """

    :param model_path:
    :return: (grammars, terminals)
        the grammars is a dict of structures and corresponding probabilities, such as
        ((D, 10), (D, 1), (L, 3)): 1.556e-7
        the terminals is a dict of tag (such as (D, 10)) and corresponding replacements
        and probabilities, such as (D, 10): {1234567890, 1.556e-7}
    """
    check_path_exists(model_path)
    grammars = read_grammars(os.path.join(model_path, "grammar", "structures.txt"))
    _dicts = []
    lower = read_tag(os.path.join(model_path, "lower"), "L")
    upper = read_tag(os.path.join(model_path, "upper"), "U")
    double_m = read_tag(os.path.join(model_path, "mixed_2"), "DM")
    triple_m = read_tag(os.path.join(model_path, "mixed_3"), "TM")
    four_m = read_tag(os.path.join(model_path, "mixed_4"), "FM")
    digits = read_tag(os.path.join(model_path, "digits"), "D")
    special = read_tag(os.path.join(model_path, "special"), "S")
    terminals = {**lower, **upper, **double_m, **triple_m, **four_m, **digits, **special}
    return grammars, terminals


def test():
    grammars, terminals = read_bpe("/home/cw/Documents/tmp/model")
    print(grammars)
    print(terminals.keys())
    pass


if __name__ == '__main__':
    test()
