from dataclasses import dataclass, field


@dataclass
class ScriptResultsTableModel:
    script_id: int
    result: str

    def __iter__(self):
        yield self.script_id
        yield self.result
