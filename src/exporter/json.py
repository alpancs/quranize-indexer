import json

from harf import Harf


def export(harf: Harf, dst_path: str) -> None:
    with open(dst_path, 'w') as dst_file:
        json.dump(
            obj=harf,
            fp=dst_file,
            ensure_ascii=False,
            check_circular=False,
            separators=(',', ':'),
            default=vars,
        )
