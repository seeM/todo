from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Iterable, List, Union

from fastcore.basics import patch
from sqlite_minutils.db import DEFAULT, Database, Default, Table, View

opt_bool = Union[bool, Default, None]


@patch
def insert(
    self:Table,
    record: Dict[str, Any]=None, pk=DEFAULT, foreign_keys=DEFAULT,
    column_order: Union[List[str], Default, None]=DEFAULT,
    not_null: Union[Iterable[str], Default, None]=DEFAULT,
    defaults: Union[Dict[str, Any], Default, None]=DEFAULT,
    hash_id: Union[str, Default, None]=DEFAULT,
    hash_id_columns: Union[Iterable[str], Default, None]=DEFAULT,
    alter: opt_bool=DEFAULT,
    ignore: opt_bool=DEFAULT,
    replace: opt_bool=DEFAULT,
    extracts: Union[Dict[str, str], List[str], Default, None]=DEFAULT,
    conversions: Union[Dict[str, str], Default, None]=DEFAULT,
    columns: Union[Dict[str, Any], Default, None]=DEFAULT,
    strict: opt_bool=DEFAULT,
    **kwargs) -> Table:
    if not record: record={}
    if is_dataclass(record):
        columns = {} if columns is DEFAULT else dict(columns)
        columns.update((k, v.type) for k, v in record.__dataclass_fields__.items())
        record = asdict(record)
    record = {**record, **kwargs}
    self._orig_insert(
        record=record, pk=pk, foreign_keys=foreign_keys, column_order=column_order, not_null=not_null,
        defaults=defaults, hash_id=hash_id, hash_id_columns=hash_id_columns, alter=alter, ignore=ignore,
        replace=replace, extracts=extracts, conversions=conversions, columns=columns, strict=strict)
    return self.get_last()

@patch
def table(self:Database, table_name: str, cls=None, **kwargs) -> Union["Table", "View"]:
    result = self._orig_table(table_name, **kwargs)
    if cls: result.cls = cls
    return result
