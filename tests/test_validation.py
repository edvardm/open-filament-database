from pathlib import Path

from ofd.validation import (
    ValidationError,
    ValidationLevel,
    ValidationOrchestrator,
    ValidationResult,
)


# -- ValidationResult --


def test_empty_result_is_valid() -> None:
    result = ValidationResult()
    assert result.is_valid
    assert result.error_count == 0
    assert result.warning_count == 0
    assert result.errors == []


def test_error_makes_result_invalid() -> None:
    result = ValidationResult()
    result.add_error(ValidationError(ValidationLevel.Error, "cat", "msg", None))
    assert not result.is_valid
    assert result.error_count == 1


def test_warning_alone_keeps_result_valid() -> None:
    result = ValidationResult()
    result.add_error(ValidationError(ValidationLevel.Warning, "cat", "msg", None))
    assert result.is_valid
    assert result.warning_count == 1
    assert result.error_count == 0


def test_error_and_warning_counted_separately() -> None:
    result = ValidationResult()
    result.add_error(ValidationError(ValidationLevel.Error, "cat", "err", None))
    result.add_error(ValidationError(ValidationLevel.Warning, "cat", "warn", None))
    assert result.error_count == 1
    assert result.warning_count == 1


def test_errors_list_contains_both_levels() -> None:
    result = ValidationResult()
    result.add_error(ValidationError(ValidationLevel.Error, "cat", "err", None))
    result.add_error(ValidationError(ValidationLevel.Warning, "cat", "warn", None))
    assert len(result.errors) == 2


def test_merge_aggregates_errors_and_warnings() -> None:
    r1 = ValidationResult()
    r1.add_error(ValidationError(ValidationLevel.Error, "cat", "err", None))
    r2 = ValidationResult()
    r2.add_error(ValidationError(ValidationLevel.Warning, "cat", "warn", None))
    r1.merge(r2)
    assert r1.error_count == 1
    assert r1.warning_count == 1
    assert len(r1.errors) == 2


# -- ValidationError --


def test_error_to_dict_structure() -> None:
    err = ValidationError(ValidationLevel.Error, "JSON Schema", "field required", "data/brand/brand.json")
    assert err.to_dict() == {
        "level": "ERROR",
        "category": "JSON Schema",
        "message": "field required",
        "path": "data/brand/brand.json",
    }


def test_warning_to_dict_level_string() -> None:
    err = ValidationError(ValidationLevel.Warning, "Folder Names", "mismatch", None)
    assert err.to_dict()["level"] == "WARNING"


def test_error_path_can_be_none() -> None:
    err = ValidationError(ValidationLevel.Error, "cat", "msg", None)
    assert err.path is None
    assert err.to_dict()["path"] is None


# -- ValidationOrchestrator integration --


def test_validate_all_passes_on_real_data() -> None:
    result = ValidationOrchestrator(
        data_dir=Path("data"),
        stores_dir=Path("stores"),
    ).validate_all()
    assert result.is_valid
