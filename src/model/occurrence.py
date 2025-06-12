from datetime import datetime
from pandas import Series

class Occurrence:
    _uc: int
    _name: str
    _locality: int|str
    _equipment: str
    _date: datetime
    _reg: str
    _city: str
    _substation: str
    _power_feeder: str
    _power_transformer: str
    _id: str
    limit = 51

    def __init__(self, row: Series) -> None:
        self._id = row.OCORRENCIA
        self._uc = row.CONTA
        self._name = self._resume_name(row.NOME)
        self._locality = row.LOCALIDADE
        self._equipment = row.DEFEITO_FALHA
        self._date = row.DH_INICIAL_INT
        self._reg = row.REGIONAL
        self._city = row.MUNICIPIO
        self._substation = row.SUBESTACAO
        self._power_feeder = row.ALIMENTADOR
        self._power_transformer = row.TRANSFORMADOR
        
    def __str__(self) -> str:
        values = (
            f'UC: {self._uc}',f'Local: {self._locality}',
            f"Nome: {self._name}", f"Equipamento: {self._equipment}",
            f"Data: {self._date}", f"Regional: {self._reg}",
            f"Município: {self._city}", f"Subestação: {self._substation}",
            f"Alimentador: {self._power_feeder}", f"Transformador: {self._power_transformer}"
            )
        return "\n".join(values)

    def _resume_name(self, name: str) -> str:
        if len(name) <= self.limit:
            return name
        else:
            return f"{name[:self.limit-9]}{'.'*3}"