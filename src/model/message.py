from typing import LiteralString
from pandas import DataFrame

from .occurrence import Occurrence

class Message:
    limit = 51
    
    @staticmethod
    def getMessage(df: DataFrame) -> LiteralString:
        _template: str = "⚠️ Atenção ⚠️\nSegue a lista de clientes com interrupção no momento\n{occurrences}\nDados atualizados."
        occurrences = "\n"
        lines = []
        for _, row in df.iterrows():
            lines.append(("-"*Message.limit))
            occurrence = Occurrence(row)
            lines.append(str(occurrence))
        occurrences = occurrences.join(lines)
        return _template.format(occurrences=occurrences)