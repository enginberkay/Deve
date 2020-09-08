from dataclasses import dataclass, field


@dataclass
class ScriptsTableModel:
    deploy_id: int
    script_name: str

    def __iter__(self):
        yield self.deploy_id
        yield self.script_name
