"""The versioned, human-editable shelf contract.

This module only turns text into typed data and typed data into text. The terminal, and later a server,
decide where the text comes from and whether to write it. All validation lives in `parse_shelf`.
"""

import re
from dataclasses import dataclass, field

import yaml
from yaml.nodes import MappingNode, Node, ScalarNode, SequenceNode

_STR = "tag:yaml.org,2002:str"
_INT = "tag:yaml.org,2002:int"
_BOOL = "tag:yaml.org,2002:bool"


class _ShelfLoader(yaml.SafeLoader):
    """YAML 1.2-like booleans: words such as `on`, `off`, `yes` and `no` stay text."""


# Copy before changing the subclass: PyYAML otherwise shares and mutates SafeLoader's resolver lists.
_ShelfLoader.yaml_implicit_resolvers = {
    first: list(resolvers) for first, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
for first, resolvers in _ShelfLoader.yaml_implicit_resolvers.items():
    _ShelfLoader.yaml_implicit_resolvers[first] = [
        (tag, pattern) for tag, pattern in resolvers if tag != _BOOL
    ]
_ShelfLoader.add_implicit_resolver(_BOOL, re.compile(r"^(?:true|false)$", re.IGNORECASE), list("tTfF"))


@dataclass
class ShelfBook:
    title: str
    authors: list[str] = field(default_factory=list)
    known_as: str | None = None
    hidden: bool | None = None
    face: bool | None = None
    cover: str | None = None
    read_as: str | None = None
    source: str | None = None
    photo: str | None = None
    work: str | None = None


@dataclass
class ShelfSection:
    title: str
    books: list[ShelfBook] = field(default_factory=list)
    text: str = ""


@dataclass
class LeftOutBook:
    title: str
    reason: str


@dataclass
class ShelfFile:
    cover_photo: str
    lens: str
    shelves: list[ShelfSection] = field(default_factory=list)
    name: str | None = None
    left_out: list[LeftOutBook] = field(default_factory=list)
    version: int = 1


@dataclass(frozen=True)
class ShelfYamlIssue:
    line: int
    path: str
    message: str

    def __str__(self) -> str:
        return f"line {self.line}: {self.path}: {self.message}"


class ShelfYamlError(ValueError):
    def __init__(self, issues: list[ShelfYamlIssue]):
        # Sorting only by line keeps the meaningful discovery order for two errors on the same field.
        self.issues = tuple(sorted(issues, key=lambda issue: issue.line))
        super().__init__("\n".join(str(issue) for issue in self.issues))


_ROOT_FIELDS = {"version", "name", "cover_photo", "lens", "shelves", "left_out"}
_SECTION_FIELDS = {"title", "text", "books"}
_BOOK_FIELDS = {
    "title",
    "authors",
    "known_as",
    "hidden",
    "face",
    "cover",
    "read_as",
    "source",
    "photo",
    "work",
}
_LEFT_OUT_FIELDS = {"title", "reason"}


class _Reader:
    def __init__(self) -> None:
        self.issues: list[ShelfYamlIssue] = []

    def issue(self, node: Node | None, path: str, message: str) -> None:
        line = node.start_mark.line + 1 if node is not None else 1
        self.issues.append(ShelfYamlIssue(line, path, message))

    def mapping(
        self,
        node: Node,
        path: str,
        allowed: set[str],
        required: tuple[str, ...] = (),
    ) -> dict[str, Node] | None:
        if not isinstance(node, MappingNode):
            self.issue(node, path, "must be a mapping")
            return None
        values: dict[str, Node] = {}
        seen: set[str] = set()
        for key_node, value_node in node.value:
            if not isinstance(key_node, ScalarNode) or key_node.tag != _STR:
                self.issue(key_node, path, "field name must be text")
                continue
            name = key_node.value
            field_path = _field(path, name)
            if name in seen:
                self.issue(key_node, field_path, "duplicate field")
                continue
            seen.add(name)
            if name not in allowed:
                self.issue(key_node, field_path, "unknown field in version 1")
                continue
            values[name] = value_node
        for name in required:
            if name not in values:
                self.issue(node, _field(path, name), "required field is missing")
        return values

    def sequence(self, node: Node, path: str) -> list[Node] | None:
        if not isinstance(node, SequenceNode):
            self.issue(node, path, "must be a list")
            return None
        return node.value

    def text(self, node: Node, path: str, *, nonempty: bool = False) -> str | None:
        if not isinstance(node, ScalarNode) or node.tag != _STR:
            self.issue(node, path, "must be text")
            return None
        if nonempty and not node.value.strip():
            self.issue(node, path, "must not be empty")
            return None
        return node.value

    def boolean(self, node: Node, path: str) -> bool | None:
        if (
            not isinstance(node, ScalarNode)
            or node.tag != _BOOL
            or node.value.lower() not in {"true", "false"}
        ):
            self.issue(node, path, "must be true or false")
            return None
        return node.value.lower() == "true"

    def integer(self, node: Node, path: str) -> int | None:
        if not isinstance(node, ScalarNode) or node.tag != _INT:
            self.issue(node, path, "must be an integer")
            return None
        return yaml.safe_load(node.value)

    def texts(self, node: Node, path: str) -> list[str]:
        nodes = self.sequence(node, path)
        if nodes is None:
            return []
        values = []
        for index, item in enumerate(nodes):
            value = self.text(item, f"{path}[{index}]", nonempty=True)
            if value is not None:
                values.append(value)
        return values

    def shelf(self, root: Node) -> ShelfFile | None:
        values = self.mapping(
            root,
            "$",
            _ROOT_FIELDS,
            required=("version", "cover_photo", "lens", "shelves"),
        )
        if values is None:
            return None

        version = self.integer(values["version"], "version") if "version" in values else None
        if version is not None and version != 1:
            self.issue(values["version"], "version", f"unsupported version {version}; expected version 1")

        name = self.text(values["name"], "name") if "name" in values else None
        cover_photo = (
            self.text(values["cover_photo"], "cover_photo", nonempty=True)
            if "cover_photo" in values
            else None
        )
        lens = self.text(values["lens"], "lens") if "lens" in values else None
        shelves = self._shelves(values["shelves"], "shelves") if "shelves" in values else []
        left_out = self._left_out(values["left_out"], "left_out") if "left_out" in values else []

        if version is None or cover_photo is None or lens is None:
            return None
        return ShelfFile(
            version=version,
            name=name,
            cover_photo=cover_photo,
            lens=lens,
            shelves=shelves,
            left_out=left_out,
        )

    def _shelves(self, node: Node, path: str) -> list[ShelfSection]:
        nodes = self.sequence(node, path)
        if nodes is None:
            return []
        shelves = []
        for index, item in enumerate(nodes):
            item_path = f"{path}[{index}]"
            values = self.mapping(item, item_path, _SECTION_FIELDS, required=("title", "books"))
            if values is None:
                continue
            title = (
                self.text(values["title"], f"{item_path}.title", nonempty=True) if "title" in values else None
            )
            text = self.text(values["text"], f"{item_path}.text") if "text" in values else ""
            books = self._books(values["books"], f"{item_path}.books") if "books" in values else []
            if title is not None and text is not None:
                shelves.append(ShelfSection(title=title, text=text, books=books))
        return shelves

    def _books(self, node: Node, path: str) -> list[ShelfBook]:
        nodes = self.sequence(node, path)
        if nodes is None:
            return []
        books = []
        for index, item in enumerate(nodes):
            item_path = f"{path}[{index}]"
            values = self.mapping(item, item_path, _BOOK_FIELDS, required=("title",))
            if values is None:
                continue
            title = (
                self.text(values["title"], f"{item_path}.title", nonempty=True) if "title" in values else None
            )
            authors = self.texts(values["authors"], f"{item_path}.authors") if "authors" in values else []
            optional_text = {
                key: self.text(values[key], f"{item_path}.{key}") if key in values else None
                for key in ("known_as", "cover", "read_as", "source", "photo", "work")
            }
            hidden = self.boolean(values["hidden"], f"{item_path}.hidden") if "hidden" in values else None
            face = self.boolean(values["face"], f"{item_path}.face") if "face" in values else None
            if title is not None:
                books.append(
                    ShelfBook(
                        title=title,
                        authors=authors,
                        hidden=hidden,
                        face=face,
                        **optional_text,
                    )
                )
        return books

    def _left_out(self, node: Node, path: str) -> list[LeftOutBook]:
        nodes = self.sequence(node, path)
        if nodes is None:
            return []
        left_out = []
        for index, item in enumerate(nodes):
            item_path = f"{path}[{index}]"
            values = self.mapping(item, item_path, _LEFT_OUT_FIELDS, required=("title", "reason"))
            if values is None:
                continue
            title = (
                self.text(values["title"], f"{item_path}.title", nonempty=True) if "title" in values else None
            )
            reason = (
                self.text(values["reason"], f"{item_path}.reason", nonempty=True)
                if "reason" in values
                else None
            )
            if title is not None and reason is not None:
                left_out.append(LeftOutBook(title, reason))
        return left_out


def parse_shelf(text: str) -> ShelfFile:
    """Validates all of shelf.yaml version 1 and returns it as typed data.

    Syntax and structural problems are reported together when possible. This function never returns a
    partial shelf: callers either receive a valid `ShelfFile` or a `ShelfYamlError` with line-numbered issues.
    """
    try:
        root = yaml.compose(text, Loader=_ShelfLoader)
    except yaml.YAMLError as error:
        mark = getattr(error, "problem_mark", None)
        line = mark.line + 1 if mark is not None else 1
        problem = getattr(error, "problem", None) or str(error).splitlines()[0]
        raise ShelfYamlError([ShelfYamlIssue(line, "$", f"YAML syntax error: {problem}")]) from error
    if root is None:
        raise ShelfYamlError([ShelfYamlIssue(1, "$", "document must be a mapping")])

    reader = _Reader()
    shelf = reader.shelf(root)
    if reader.issues:
        raise ShelfYamlError(reader.issues)
    if shelf is None:  # all invalid paths above add an issue; this is an invariant guard
        raise ShelfYamlError([ShelfYamlIssue(1, "$", "document is invalid")])
    return shelf


class _ShelfDumper(yaml.SafeDumper):
    pass


def _represent_text(dumper: yaml.SafeDumper, value: str):
    style = "|" if "\n" in value else None
    return dumper.represent_scalar(_STR, value, style=style)


_ShelfDumper.add_representer(str, _represent_text)


def dump_shelf(shelf: ShelfFile) -> str:
    """Returns stable, human-readable version 1 YAML without opening or writing a file."""
    data = {
        "version": shelf.version,
        **({"name": shelf.name} if shelf.name is not None else {}),
        "cover_photo": shelf.cover_photo,
        "lens": shelf.lens,
        "shelves": [_section_data(section) for section in shelf.shelves],
        **({"left_out": [_left_out_data(book) for book in shelf.left_out]} if shelf.left_out else {}),
    }
    return yaml.dump(
        data,
        Dumper=_ShelfDumper,
        allow_unicode=True,
        sort_keys=False,
        width=100,
    )


def _section_data(section: ShelfSection) -> dict:
    return {
        "title": section.title,
        **({"text": section.text} if section.text else {}),
        "books": [_book_data(book) for book in section.books],
    }


def _book_data(book: ShelfBook) -> dict:
    return {
        "title": book.title,
        **({"authors": book.authors} if book.authors else {}),
        **({"known_as": book.known_as} if book.known_as is not None else {}),
        **({"hidden": book.hidden} if book.hidden is not None else {}),
        **({"face": book.face} if book.face is not None else {}),
        **({"cover": book.cover} if book.cover is not None else {}),
        **({"read_as": book.read_as} if book.read_as is not None else {}),
        **({"source": book.source} if book.source is not None else {}),
        **({"photo": book.photo} if book.photo is not None else {}),
        **({"work": book.work} if book.work is not None else {}),
    }


def _left_out_data(book: LeftOutBook) -> dict:
    return {"title": book.title, "reason": book.reason}


def _field(path: str, name: str) -> str:
    return name if path == "$" else f"{path}.{name}"
