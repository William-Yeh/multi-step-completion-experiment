"""Structural-invariant tests for ``build_task_prompt``.

These tests lock in the high-level shape of each experiment's prompt so that
unintended drift (a missing section, a removed gate clause, the variants
collapsing into each other) fails loudly. They do not snapshot full text —
wording is allowed to iterate without breaking tests.

Run with::

    uv run --with pytest --with "rich>=13.0" pytest tests/

The ``--with`` flags supply ``pytest`` and the runtime deps of ``run.py``
(declared in its PEP 723 inline metadata). Add new ``--with`` entries here
if ``run.py`` gains additional top-level imports.
"""

from __future__ import annotations

from pathlib import Path

from run import (
    ACCEPTED_RESPONSE_KEYS,
    DEFECT_CATEGORIES,
    _join_oxford,
    accepted_tool_result,
    build_task_prompt,
    check_footnotes,
)

CASE_DIR = Path("/tmp/case_01")
CASE_ID = "case_01"


def _prompt(experiment: str) -> str:
    return build_task_prompt(experiment, CASE_ID, CASE_DIR)


def test_exp1_uses_steps_and_constraints_sections():
    prompt = _prompt("1")
    assert "Steps (perform in order):" in prompt
    assert "Constraints:" in prompt
    assert "1. Read input.md." in prompt
    assert "3. Write final.md and result.json." in prompt


def test_exp1_self_check_lives_in_constraints_not_steps():
    prompt = _prompt("1")
    assert "MUST NOT run the external checker" in prompt
    assert "4. " not in prompt.split("Constraints:")[0]


def test_exp2_uses_steps_and_constraints_sections():
    prompt = _prompt("2")
    assert "Steps (perform in order):" in prompt
    assert "Constraints:" in prompt
    assert "5. After the tool accepts the check request" in prompt


def test_exp2_gate_references_every_response_key():
    prompt = _prompt("2")
    for key in ACCEPTED_RESPONSE_KEYS:
        assert f'"{key}"' in prompt, f"gate clause missing key: {key}"
    assert 'Set model_status="completed" only if tool_invocation contains' in prompt


def test_exp2_constraints_describe_response_keys_from_constant():
    prompt = _prompt("2")
    keys_list = ", ".join(ACCEPTED_RESPONSE_KEYS)
    assert f"call-acknowledgement ({keys_list})" in prompt


def test_exp1_has_no_presence_gate_clause():
    """Exp 1 carries no gate language binding model_status to tool_invocation.

    The string ``tool_invocation`` itself does appear in exp 1 (the JSON schema
    is shared across variants), so we test for the *gate clause wording*, not
    the field name.
    """
    prompt = _prompt("1")
    assert "Set model_status=" not in prompt
    assert "tool_invocation contains" not in prompt


def test_exp3_protocol_structure_preserved():
    """Exp 3's branching protocol was intentionally NOT flattened to a numbered list."""
    prompt = _prompt("3")
    assert "Protocol:" in prompt
    assert "Steps (perform in order):" not in prompt
    assert "preflight" in prompt.lower()


def test_all_experiments_share_defect_vocabulary():
    """Every variant must enumerate the full DEFECT_CATEGORIES list (vocabulary parity).

    Without this, exp 3 would have an unfair advantage: its repair clause names
    every defect category, so its agent knows exactly what to scan for. Exp 1
    and exp 2 would have to infer the same categories from prose. We level the
    playing field by surfacing the names in the shared preamble.
    """
    for experiment in ("1", "2", "3"):
        prompt = _prompt(experiment)
        for category in DEFECT_CATEGORIES:
            assert category in prompt, (
                f"experiment {experiment} prompt missing defect category: {category}"
            )


def test_check_footnotes_returns_all_defect_category_keys():
    """Every DEFECT_CATEGORIES key must appear in check_footnotes' result dict."""
    result = check_footnotes("paragraph.[^1]\n\n[^1]: def\n")
    for category in DEFECT_CATEGORIES:
        assert category in result, f"check_footnotes missing key: {category}"


def test_accepted_tool_result_returns_all_response_keys():
    """Every ACCEPTED_RESPONSE_KEYS key must appear in accepted_tool_result's response."""
    result = accepted_tool_result("candidate.md")
    for key in ACCEPTED_RESPONSE_KEYS:
        assert key in result, f"accepted_tool_result missing key: {key}"


def test_join_oxford_handles_all_arities():
    """_join_oxford renders Oxford-style joins for 0, 1, 2, and 3+ items.

    The helper exists specifically to handle len <= 1, which the original
    inline expression got wrong (produced ", and foo" or IndexError); these
    cases exercise that contract.
    """
    assert _join_oxford(()) == ""
    assert _join_oxford(("a",)) == "a"
    assert _join_oxford(("a", "b")) == "a, and b"
    assert _join_oxford(("a", "b", "c")) == "a, b, and c"
