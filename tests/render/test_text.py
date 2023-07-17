from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pipdeptree._render.text import render_text

if TYPE_CHECKING:
    from pipdeptree._models import PackageDAG


@pytest.mark.parametrize(
    ("list_all", "reverse", "unicode", "expected_output"),
    [
        (
            True,
            False,
            True,
            [
                "a==3.4.0",
                "├── b [required: >=2.0.0, installed: 2.3.1]",
                "│   └── d [required: >=2.30,<2.42, installed: 2.35]",
                "│       └── e [required: >=0.9.0, installed: 0.12.1]",
                "└── c [required: >=5.7.1, installed: 5.10.0]",
                "    ├── d [required: >=2.30, installed: 2.35]",
                "    │   └── e [required: >=0.9.0, installed: 0.12.1]",
                "    └── e [required: >=0.12.1, installed: 0.12.1]",
                "b==2.3.1",
                "└── d [required: >=2.30,<2.42, installed: 2.35]",
                "    └── e [required: >=0.9.0, installed: 0.12.1]",
                "c==5.10.0",
                "├── d [required: >=2.30, installed: 2.35]",
                "│   └── e [required: >=0.9.0, installed: 0.12.1]",
                "└── e [required: >=0.12.1, installed: 0.12.1]",
                "d==2.35",
                "└── e [required: >=0.9.0, installed: 0.12.1]",
                "e==0.12.1",
                "f==3.1",
                "└── b [required: >=2.1.0, installed: 2.3.1]",
                "    └── d [required: >=2.30,<2.42, installed: 2.35]",
                "        └── e [required: >=0.9.0, installed: 0.12.1]",
                "g==6.8.3rc1",
                "├── e [required: >=0.9.0, installed: 0.12.1]",
                "└── f [required: >=3.0.0, installed: 3.1]",
                "    └── b [required: >=2.1.0, installed: 2.3.1]",
                "        └── d [required: >=2.30,<2.42, installed: 2.35]",
                "            └── e [required: >=0.9.0, installed: 0.12.1]",
            ],
        ),
        (
            True,
            True,
            True,
            [
                "a==3.4.0",
                "b==2.3.1",
                "├── a==3.4.0 [requires: b>=2.0.0]",
                "└── f==3.1 [requires: b>=2.1.0]",
                "    └── g==6.8.3rc1 [requires: f>=3.0.0]",
                "c==5.10.0",
                "└── a==3.4.0 [requires: c>=5.7.1]",
                "d==2.35",
                "├── b==2.3.1 [requires: d>=2.30,<2.42]",
                "│   ├── a==3.4.0 [requires: b>=2.0.0]",
                "│   └── f==3.1 [requires: b>=2.1.0]",
                "│       └── g==6.8.3rc1 [requires: f>=3.0.0]",
                "└── c==5.10.0 [requires: d>=2.30]",
                "    └── a==3.4.0 [requires: c>=5.7.1]",
                "e==0.12.1",
                "├── c==5.10.0 [requires: e>=0.12.1]",
                "│   └── a==3.4.0 [requires: c>=5.7.1]",
                "├── d==2.35 [requires: e>=0.9.0]",
                "│   ├── b==2.3.1 [requires: d>=2.30,<2.42]",
                "│   │   ├── a==3.4.0 [requires: b>=2.0.0]",
                "│   │   └── f==3.1 [requires: b>=2.1.0]",
                "│   │       └── g==6.8.3rc1 [requires: f>=3.0.0]",
                "│   └── c==5.10.0 [requires: d>=2.30]",
                "│       └── a==3.4.0 [requires: c>=5.7.1]",
                "└── g==6.8.3rc1 [requires: e>=0.9.0]",
                "f==3.1",
                "└── g==6.8.3rc1 [requires: f>=3.0.0]",
                "g==6.8.3rc1",
            ],
        ),
        (
            False,
            False,
            True,
            [
                "a==3.4.0",
                "├── b [required: >=2.0.0, installed: 2.3.1]",
                "│   └── d [required: >=2.30,<2.42, installed: 2.35]",
                "│       └── e [required: >=0.9.0, installed: 0.12.1]",
                "└── c [required: >=5.7.1, installed: 5.10.0]",
                "    ├── d [required: >=2.30, installed: 2.35]",
                "    │   └── e [required: >=0.9.0, installed: 0.12.1]",
                "    └── e [required: >=0.12.1, installed: 0.12.1]",
                "g==6.8.3rc1",
                "├── e [required: >=0.9.0, installed: 0.12.1]",
                "└── f [required: >=3.0.0, installed: 3.1]",
                "    └── b [required: >=2.1.0, installed: 2.3.1]",
                "        └── d [required: >=2.30,<2.42, installed: 2.35]",
                "            └── e [required: >=0.9.0, installed: 0.12.1]",
            ],
        ),
        (
            False,
            True,
            True,
            [
                "e==0.12.1",
                "├── c==5.10.0 [requires: e>=0.12.1]",
                "│   └── a==3.4.0 [requires: c>=5.7.1]",
                "├── d==2.35 [requires: e>=0.9.0]",
                "│   ├── b==2.3.1 [requires: d>=2.30,<2.42]",
                "│   │   ├── a==3.4.0 [requires: b>=2.0.0]",
                "│   │   └── f==3.1 [requires: b>=2.1.0]",
                "│   │       └── g==6.8.3rc1 [requires: f>=3.0.0]",
                "│   └── c==5.10.0 [requires: d>=2.30]",
                "│       └── a==3.4.0 [requires: c>=5.7.1]",
                "└── g==6.8.3rc1 [requires: e>=0.9.0]",
            ],
        ),
        (
            True,
            False,
            False,
            [
                "a==3.4.0",
                "  - b [required: >=2.0.0, installed: 2.3.1]",
                "    - d [required: >=2.30,<2.42, installed: 2.35]",
                "      - e [required: >=0.9.0, installed: 0.12.1]",
                "  - c [required: >=5.7.1, installed: 5.10.0]",
                "    - d [required: >=2.30, installed: 2.35]",
                "      - e [required: >=0.9.0, installed: 0.12.1]",
                "    - e [required: >=0.12.1, installed: 0.12.1]",
                "b==2.3.1",
                "  - d [required: >=2.30,<2.42, installed: 2.35]",
                "    - e [required: >=0.9.0, installed: 0.12.1]",
                "c==5.10.0",
                "  - d [required: >=2.30, installed: 2.35]",
                "    - e [required: >=0.9.0, installed: 0.12.1]",
                "  - e [required: >=0.12.1, installed: 0.12.1]",
                "d==2.35",
                "  - e [required: >=0.9.0, installed: 0.12.1]",
                "e==0.12.1",
                "f==3.1",
                "  - b [required: >=2.1.0, installed: 2.3.1]",
                "    - d [required: >=2.30,<2.42, installed: 2.35]",
                "      - e [required: >=0.9.0, installed: 0.12.1]",
                "g==6.8.3rc1",
                "  - e [required: >=0.9.0, installed: 0.12.1]",
                "  - f [required: >=3.0.0, installed: 3.1]",
                "    - b [required: >=2.1.0, installed: 2.3.1]",
                "      - d [required: >=2.30,<2.42, installed: 2.35]",
                "        - e [required: >=0.9.0, installed: 0.12.1]",
            ],
        ),
        (
            True,
            True,
            False,
            [
                "a==3.4.0",
                "b==2.3.1",
                "  - a==3.4.0 [requires: b>=2.0.0]",
                "  - f==3.1 [requires: b>=2.1.0]",
                "    - g==6.8.3rc1 [requires: f>=3.0.0]",
                "c==5.10.0",
                "  - a==3.4.0 [requires: c>=5.7.1]",
                "d==2.35",
                "  - b==2.3.1 [requires: d>=2.30,<2.42]",
                "    - a==3.4.0 [requires: b>=2.0.0]",
                "    - f==3.1 [requires: b>=2.1.0]",
                "      - g==6.8.3rc1 [requires: f>=3.0.0]",
                "  - c==5.10.0 [requires: d>=2.30]",
                "    - a==3.4.0 [requires: c>=5.7.1]",
                "e==0.12.1",
                "  - c==5.10.0 [requires: e>=0.12.1]",
                "    - a==3.4.0 [requires: c>=5.7.1]",
                "  - d==2.35 [requires: e>=0.9.0]",
                "    - b==2.3.1 [requires: d>=2.30,<2.42]",
                "      - a==3.4.0 [requires: b>=2.0.0]",
                "      - f==3.1 [requires: b>=2.1.0]",
                "        - g==6.8.3rc1 [requires: f>=3.0.0]",
                "    - c==5.10.0 [requires: d>=2.30]",
                "      - a==3.4.0 [requires: c>=5.7.1]",
                "  - g==6.8.3rc1 [requires: e>=0.9.0]",
                "f==3.1",
                "  - g==6.8.3rc1 [requires: f>=3.0.0]",
                "g==6.8.3rc1",
            ],
        ),
        (
            False,
            False,
            False,
            [
                "a==3.4.0",
                "  - b [required: >=2.0.0, installed: 2.3.1]",
                "    - d [required: >=2.30,<2.42, installed: 2.35]",
                "      - e [required: >=0.9.0, installed: 0.12.1]",
                "  - c [required: >=5.7.1, installed: 5.10.0]",
                "    - d [required: >=2.30, installed: 2.35]",
                "      - e [required: >=0.9.0, installed: 0.12.1]",
                "    - e [required: >=0.12.1, installed: 0.12.1]",
                "g==6.8.3rc1",
                "  - e [required: >=0.9.0, installed: 0.12.1]",
                "  - f [required: >=3.0.0, installed: 3.1]",
                "    - b [required: >=2.1.0, installed: 2.3.1]",
                "      - d [required: >=2.30,<2.42, installed: 2.35]",
                "        - e [required: >=0.9.0, installed: 0.12.1]",
            ],
        ),
        (
            False,
            True,
            False,
            [
                "e==0.12.1",
                "  - c==5.10.0 [requires: e>=0.12.1]",
                "    - a==3.4.0 [requires: c>=5.7.1]",
                "  - d==2.35 [requires: e>=0.9.0]",
                "    - b==2.3.1 [requires: d>=2.30,<2.42]",
                "      - a==3.4.0 [requires: b>=2.0.0]",
                "      - f==3.1 [requires: b>=2.1.0]",
                "        - g==6.8.3rc1 [requires: f>=3.0.0]",
                "    - c==5.10.0 [requires: d>=2.30]",
                "      - a==3.4.0 [requires: c>=5.7.1]",
                "  - g==6.8.3rc1 [requires: e>=0.9.0]",
            ],
        ),
    ],
)
def test_render_text(  # noqa: PLR0913
    example_dag: PackageDAG,
    capsys: pytest.CaptureFixture[str],
    list_all: bool,
    reverse: bool,
    unicode: bool,
    expected_output: list[str],
) -> None:
    tree = example_dag.reverse() if reverse else example_dag
    encoding = "utf-8" if unicode else "ascii"
    render_text(tree, max_depth=float("inf"), encoding=encoding, list_all=list_all, frozen=False)
    captured = capsys.readouterr()
    assert "\n".join(expected_output).strip() == captured.out.strip()


@pytest.mark.parametrize(
    ("unicode", "level", "expected_output"),
    [
        (
            True,
            0,
            [
                "a==3.4.0",
                "b==2.3.1",
                "c==5.10.0",
                "d==2.35",
                "e==0.12.1",
                "f==3.1",
                "g==6.8.3rc1",
            ],
        ),
        (
            False,
            0,
            [
                "a==3.4.0",
                "b==2.3.1",
                "c==5.10.0",
                "d==2.35",
                "e==0.12.1",
                "f==3.1",
                "g==6.8.3rc1",
            ],
        ),
        (
            True,
            2,
            [
                "a==3.4.0",
                "├── b [required: >=2.0.0, installed: 2.3.1]",
                "│   └── d [required: >=2.30,<2.42, installed: 2.35]",
                "└── c [required: >=5.7.1, installed: 5.10.0]",
                "    ├── d [required: >=2.30, installed: 2.35]",
                "    └── e [required: >=0.12.1, installed: 0.12.1]",
                "b==2.3.1",
                "└── d [required: >=2.30,<2.42, installed: 2.35]",
                "    └── e [required: >=0.9.0, installed: 0.12.1]",
                "c==5.10.0",
                "├── d [required: >=2.30, installed: 2.35]",
                "│   └── e [required: >=0.9.0, installed: 0.12.1]",
                "└── e [required: >=0.12.1, installed: 0.12.1]",
                "d==2.35",
                "└── e [required: >=0.9.0, installed: 0.12.1]",
                "e==0.12.1",
                "f==3.1",
                "└── b [required: >=2.1.0, installed: 2.3.1]",
                "    └── d [required: >=2.30,<2.42, installed: 2.35]",
                "g==6.8.3rc1",
                "├── e [required: >=0.9.0, installed: 0.12.1]",
                "└── f [required: >=3.0.0, installed: 3.1]",
                "    └── b [required: >=2.1.0, installed: 2.3.1]",
            ],
        ),
        (
            False,
            2,
            [
                "a==3.4.0",
                "  - b [required: >=2.0.0, installed: 2.3.1]",
                "    - d [required: >=2.30,<2.42, installed: 2.35]",
                "  - c [required: >=5.7.1, installed: 5.10.0]",
                "    - d [required: >=2.30, installed: 2.35]",
                "    - e [required: >=0.12.1, installed: 0.12.1]",
                "b==2.3.1",
                "  - d [required: >=2.30,<2.42, installed: 2.35]",
                "    - e [required: >=0.9.0, installed: 0.12.1]",
                "c==5.10.0",
                "  - d [required: >=2.30, installed: 2.35]",
                "    - e [required: >=0.9.0, installed: 0.12.1]",
                "  - e [required: >=0.12.1, installed: 0.12.1]",
                "d==2.35",
                "  - e [required: >=0.9.0, installed: 0.12.1]",
                "e==0.12.1",
                "f==3.1",
                "  - b [required: >=2.1.0, installed: 2.3.1]",
                "    - d [required: >=2.30,<2.42, installed: 2.35]",
                "g==6.8.3rc1",
                "  - e [required: >=0.9.0, installed: 0.12.1]",
                "  - f [required: >=3.0.0, installed: 3.1]",
                "    - b [required: >=2.1.0, installed: 2.3.1]",
            ],
        ),
    ],
)
def test_render_text_given_depth(
    capsys: pytest.CaptureFixture[str],
    unicode: str,
    level: int,
    expected_output: list[str],
    example_dag: PackageDAG,
) -> None:
    render_text(example_dag, max_depth=level, encoding="utf-8" if unicode else "ascii")
    captured = capsys.readouterr()
    assert "\n".join(expected_output).strip() == captured.out.strip()


@pytest.mark.parametrize(
    ("level", "encoding", "expected_output"),
    [
        (
            0,
            "utf-8",
            [
                "a==3.4.0",
                "b==2.3.1",
                "c==5.10.0",
                "d==2.35",
                "e==0.12.1",
                "f==3.1",
                "g==6.8.3rc1",
            ],
        ),
        (
            0,
            "utf-8",
            [
                "a==3.4.0",
                "b==2.3.1",
                "c==5.10.0",
                "d==2.35",
                "e==0.12.1",
                "f==3.1",
                "g==6.8.3rc1",
            ],
        ),
        (
            2,
            "utf-8",
            [
                "a==3.4.0",
                "├── b [required: >=2.0.0, installed: 2.3.1]",
                "│   └── d [required: >=2.30,<2.42, installed: 2.35]",
                "└── c [required: >=5.7.1, installed: 5.10.0]",
                "    ├── d [required: >=2.30, installed: 2.35]",
                "    └── e [required: >=0.12.1, installed: 0.12.1]",
                "b==2.3.1",
                "└── d [required: >=2.30,<2.42, installed: 2.35]",
                "    └── e [required: >=0.9.0, installed: 0.12.1]",
                "c==5.10.0",
                "├── d [required: >=2.30, installed: 2.35]",
                "│   └── e [required: >=0.9.0, installed: 0.12.1]",
                "└── e [required: >=0.12.1, installed: 0.12.1]",
                "d==2.35",
                "└── e [required: >=0.9.0, installed: 0.12.1]",
                "e==0.12.1",
                "f==3.1",
                "└── b [required: >=2.1.0, installed: 2.3.1]",
                "    └── d [required: >=2.30,<2.42, installed: 2.35]",
                "g==6.8.3rc1",
                "├── e [required: >=0.9.0, installed: 0.12.1]",
                "└── f [required: >=3.0.0, installed: 3.1]",
                "    └── b [required: >=2.1.0, installed: 2.3.1]",
            ],
        ),
        (
            2,
            "ascii",
            [
                "a==3.4.0",
                "  - b [required: >=2.0.0, installed: 2.3.1]",
                "    - d [required: >=2.30,<2.42, installed: 2.35]",
                "  - c [required: >=5.7.1, installed: 5.10.0]",
                "    - d [required: >=2.30, installed: 2.35]",
                "    - e [required: >=0.12.1, installed: 0.12.1]",
                "b==2.3.1",
                "  - d [required: >=2.30,<2.42, installed: 2.35]",
                "    - e [required: >=0.9.0, installed: 0.12.1]",
                "c==5.10.0",
                "  - d [required: >=2.30, installed: 2.35]",
                "    - e [required: >=0.9.0, installed: 0.12.1]",
                "  - e [required: >=0.12.1, installed: 0.12.1]",
                "d==2.35",
                "  - e [required: >=0.9.0, installed: 0.12.1]",
                "e==0.12.1",
                "f==3.1",
                "  - b [required: >=2.1.0, installed: 2.3.1]",
                "    - d [required: >=2.30,<2.42, installed: 2.35]",
                "g==6.8.3rc1",
                "  - e [required: >=0.9.0, installed: 0.12.1]",
                "  - f [required: >=3.0.0, installed: 3.1]",
                "    - b [required: >=2.1.0, installed: 2.3.1]",
            ],
        ),
        (
            2,
            "utf-8",
            [
                "a==3.4.0",
                "├── b [required: >=2.0.0, installed: 2.3.1]",
                "│   └── d [required: >=2.30,<2.42, installed: 2.35]",
                "└── c [required: >=5.7.1, installed: 5.10.0]",
                "    ├── d [required: >=2.30, installed: 2.35]",
                "    └── e [required: >=0.12.1, installed: 0.12.1]",
                "b==2.3.1",
                "└── d [required: >=2.30,<2.42, installed: 2.35]",
                "    └── e [required: >=0.9.0, installed: 0.12.1]",
                "c==5.10.0",
                "├── d [required: >=2.30, installed: 2.35]",
                "│   └── e [required: >=0.9.0, installed: 0.12.1]",
                "└── e [required: >=0.12.1, installed: 0.12.1]",
                "d==2.35",
                "└── e [required: >=0.9.0, installed: 0.12.1]",
                "e==0.12.1",
                "f==3.1",
                "└── b [required: >=2.1.0, installed: 2.3.1]",
                "    └── d [required: >=2.30,<2.42, installed: 2.35]",
                "g==6.8.3rc1",
                "├── e [required: >=0.9.0, installed: 0.12.1]",
                "└── f [required: >=3.0.0, installed: 3.1]",
                "    └── b [required: >=2.1.0, installed: 2.3.1]",
            ],
        ),
        (
            2,
            "ascii",
            [
                "a==3.4.0",
                "  - b [required: >=2.0.0, installed: 2.3.1]",
                "    - d [required: >=2.30,<2.42, installed: 2.35]",
                "  - c [required: >=5.7.1, installed: 5.10.0]",
                "    - d [required: >=2.30, installed: 2.35]",
                "    - e [required: >=0.12.1, installed: 0.12.1]",
                "b==2.3.1",
                "  - d [required: >=2.30,<2.42, installed: 2.35]",
                "    - e [required: >=0.9.0, installed: 0.12.1]",
                "c==5.10.0",
                "  - d [required: >=2.30, installed: 2.35]",
                "    - e [required: >=0.9.0, installed: 0.12.1]",
                "  - e [required: >=0.12.1, installed: 0.12.1]",
                "d==2.35",
                "  - e [required: >=0.9.0, installed: 0.12.1]",
                "e==0.12.1",
                "f==3.1",
                "  - b [required: >=2.1.0, installed: 2.3.1]",
                "    - d [required: >=2.30,<2.42, installed: 2.35]",
                "g==6.8.3rc1",
                "  - e [required: >=0.9.0, installed: 0.12.1]",
                "  - f [required: >=3.0.0, installed: 3.1]",
                "    - b [required: >=2.1.0, installed: 2.3.1]",
            ],
        ),
    ],
)
def test_render_text_encoding(
    capsys: pytest.CaptureFixture[str],
    level: int,
    encoding: str,
    expected_output: list[str],
    example_dag: PackageDAG,
) -> None:
    render_text(example_dag, max_depth=level, encoding=encoding, list_all=True, frozen=False)
    captured = capsys.readouterr()
    assert "\n".join(expected_output).strip() == captured.out.strip()
