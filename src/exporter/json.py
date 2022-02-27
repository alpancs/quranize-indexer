import json
import sys

from harf import Harf


def export(harf: Harf, dst_path: str) -> None:
    default_recursion_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(10111)
    with open(dst_path, 'w') as dst_file:
        json.dump(
            obj=harf,
            fp=dst_file,
            ensure_ascii=False,
            check_circular=False,
            separators=(',', ':'),
            default=vars,
        )
    sys.setrecursionlimit(default_recursion_limit)
