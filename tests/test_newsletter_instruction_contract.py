from pathlib import Path

import yaml


INSTRUCTIONS = Path(__file__).resolve().parent.parent / "INSTRUCTIONS.md"
ACTION_SCHEMA = Path(__file__).resolve().parent.parent / "gpt.yaml"


def test_newsletter_workflow_requires_preheader_in_authoring_and_submission():
    text = INSTRUCTIONS.read_text()

    assert "with `subject`, `preheader`, and `body`." in text
    assert "each section is `{subject, preheader, body}`." in text


def test_action_operation_descriptions_fit_custom_gpt_limit():
    spec = yaml.safe_load(ACTION_SCHEMA.read_text())
    violations = []

    for path, methods in spec["paths"].items():
        for method, operation in methods.items():
            if method.lower() not in {"get", "post", "put", "patch", "delete"}:
                continue
            description = operation.get("description", "")
            if len(description) > 300:
                violations.append(
                    (
                        operation.get("operationId"),
                        method.upper(),
                        path,
                        len(description),
                    )
                )

    assert violations == []
