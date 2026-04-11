"""
Tests for ofd/builder/utils.py — UUID generation and string utilities.

These serve as idiomatic examples for further tests in this project.
"""

from ofd.builder import utils


# =============================================================================
# UUID generation — deterministic, spec-defined values
# =============================================================================


def test_generate_brand_uuid_prusament() -> None:
    # Value from docstring; changing this breaks OFD spec compatibility.
    assert utils.generate_brand_uuid("Prusament") == "ae5ff34e-298e-50c9-8f77-92a97fb30b09"


def test_generate_brand_uuid_is_deterministic() -> None:
    assert utils.generate_brand_uuid("Prusament") == utils.generate_brand_uuid("Prusament")


def test_generate_material_uuid_pla_galaxy_black() -> None:
    brand_uuid = utils.generate_brand_uuid("Prusament")
    assert utils.generate_material_uuid(brand_uuid, "PLA Prusa Galaxy Black") == "1aaca54a-431f-5601-adf5-85dd018f487f"


def test_generate_material_uuid_accepts_uuid_object() -> None:
    import uuid

    brand_str = utils.generate_brand_uuid("Prusament")
    brand_obj = uuid.UUID(brand_str)
    assert utils.generate_material_uuid(brand_str, "PLA") == utils.generate_material_uuid(brand_obj, "PLA")


def test_generate_brand_uuid_different_names_differ() -> None:
    assert utils.generate_brand_uuid("Prusament") != utils.generate_brand_uuid("Bambu Lab")


# =============================================================================
# slugify
# =============================================================================


def test_slugify_lowercase() -> None:
    assert utils.slugify("MixedCase") == "mixedcase"


def test_slugify_spaces_become_underscores() -> None:
    assert utils.slugify("PLA Basic") == "pla_basic"


def test_slugify_hyphens_become_underscores() -> None:
    assert utils.slugify("pla-basic") == "pla_basic"


def test_slugify_removes_special_characters() -> None:
    assert utils.slugify("Support@Plus!") == "supportplus"


def test_slugify_collapses_consecutive_underscores() -> None:
    assert utils.slugify("multiple   spaces") == "multiple_spaces"


def test_slugify_strips_leading_trailing_underscores() -> None:
    assert utils.slugify("_leading_") == "leading"


def test_slugify_preserves_plus_sign() -> None:
    assert utils.slugify("PLA+") == "pla+"


def test_slugify_all_invalid_chars_returns_empty_string() -> None:
    assert utils.slugify("!!!") == ""


# =============================================================================
# normalize_color_hex
# =============================================================================


def test_normalize_color_hex_uppercase_passthrough() -> None:
    assert utils.normalize_color_hex("#FF0000") == "#FF0000"


def test_normalize_color_hex_lowercase_to_upper() -> None:
    assert utils.normalize_color_hex("#ff0000") == "#FF0000"


def test_normalize_color_hex_expands_3digit() -> None:
    assert utils.normalize_color_hex("#fff") == "#FFFFFF"


def test_normalize_color_hex_expands_3digit_no_hash() -> None:
    assert utils.normalize_color_hex("fff") == "#FFFFFF"


def test_normalize_color_hex_adds_hash_to_6digit() -> None:
    assert utils.normalize_color_hex("FF0000") == "#FF0000"


def test_normalize_color_hex_none_returns_none() -> None:
    assert utils.normalize_color_hex(None) is None


def test_normalize_color_hex_empty_string_returns_none() -> None:
    assert utils.normalize_color_hex("") is None


def test_normalize_color_hex_list_takes_first() -> None:
    assert utils.normalize_color_hex(["#ff0000", "#00ff00"]) == "#FF0000"


def test_normalize_color_hex_unparseable_returned_as_is() -> None:
    assert utils.normalize_color_hex("not-a-color") == "not-a-color"


# =============================================================================
# ensure_list
# =============================================================================


def test_ensure_list_none_returns_empty() -> None:
    assert utils.ensure_list(None) == []


def test_ensure_list_scalar_string_wrapped() -> None:
    assert utils.ensure_list("pla") == ["pla"]


def test_ensure_list_scalar_int_wrapped() -> None:
    assert utils.ensure_list(42) == [42]


def test_ensure_list_list_returned_unchanged() -> None:
    assert utils.ensure_list(["a", "b"]) == ["a", "b"]


def test_ensure_list_dict_wrapped() -> None:
    assert utils.ensure_list({"k": "v"}) == [{"k": "v"}]
