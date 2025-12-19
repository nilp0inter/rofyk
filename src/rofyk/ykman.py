from subprocess import run
from typing import List

from .models.entry import Entry


class Ykman:
    def __init__(self, device=None):
        self.device = device

    def get_args(self, binary = "ykman", extra_options: List[str] | None = None, command: List[str] | None = None) -> List[str]:
        options = []
        if self.device is not None:
            options.extend(["--device", self.device])
        if extra_options is not None:
            options.extend(extra_options)

        if command is None:
            command = []

        return [binary] + options + command

    def list_entries(self) -> List[Entry]:
        args = self.get_args(command=["oath", "accounts", "list"])
        rbw = run(args, encoding="utf-8", capture_output=True)

        if rbw.returncode != 0:
            print("There was a problem calling ykman. Is it installed?")
            print(rbw.stderr)
            exit(12)

        return [self.__parse_ykman_output(it) for it in (rbw.stdout.strip("\n").split("\n"))]

    def __parse_ykman_output(self, entry_string: str) -> Entry:
        fields = entry_string.split(":")

        return Entry(fields[0], fields[1] if len(fields) > 1 else "")

    def fetch_credentials(self, entry: Entry) -> str:
        args = self.get_args(command=["oath", "accounts", "code", "--single", f"{entry.name}:{entry.username}"])
        return run(
            args,
            capture_output=True,
            encoding="utf-8",
        ).stdout.strip("\n")
