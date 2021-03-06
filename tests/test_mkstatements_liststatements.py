"""Use list of dictionaries to initialize list of Statement objects."""

from csv2shex.mkstatements import list_statements, Statement


def test_liststatements():
    """Turn list of dictionaries into list of Statement objects."""
    csvrows_list = [
        {"shape_id": "@a", "prop_id": "dct:creator", "value_type": "URI"},
        {"shape_id": "@a", "prop_id": "dct:subject", "value_type": "URI"},
        {"shape_id": "@a", "prop_id": "dct:date", "value_type": "String"},
        {"shape_id": "@b", "prop_id": "foaf:name", "value_type": "String"},
    ]
    assert list_statements(csvrows_list) == [
        Statement(start=True, shape_id="@a", prop_id="dct:creator", value_type="URI"),
        Statement(start=True, shape_id="@a", prop_id="dct:subject", value_type="URI"),
        Statement(start=True, shape_id="@a", prop_id="dct:date", value_type="String"),
        Statement(start=False, shape_id="@b", prop_id="foaf:name", value_type="String"),
    ]


def test_liststatements_without_shape_ids():
    """Not shape IDs specified, so shape is '@default'."""
    csvrows_list = [
        {"prop_id": "dct:creator", "value_type": "URI"},
        {"prop_id": "dct:subject", "value_type": "URI"},
        {"prop_id": "dct:date", "value_type": "String"},
    ]
    assert list_statements(csvrows_list) == [
        Statement(
            start=True, shape_id="@default", prop_id="dct:creator", value_type="URI"
        ),
        Statement(
            start=True, shape_id="@default", prop_id="dct:subject", value_type="URI"
        ),
        Statement(
            start=True, shape_id="@default", prop_id="dct:date", value_type="String"
        ),
    ]


def test_liststatements_with_shape_ids_specified_as_none():
    """Shape IDs specified as 'None', so shape is '@default'.
    When "shape_id" specified as 'None', row["shape_id"] will be False.
    General case: when field specified as None."""
    csvrows_list = [
        {"shape_id": None, "prop_id": "dct:creator", "value_type": "URI"},
        {"shape_id": None, "prop_id": "dct:subject", "value_type": "URI"},
        {"shape_id": None, "prop_id": "dct:date", "value_type": "String"},
    ]
    assert list_statements(csvrows_list) == [
        Statement(
            start=True, shape_id="@default", prop_id="dct:creator", value_type="URI"
        ),
        Statement(
            start=True, shape_id="@default", prop_id="dct:subject", value_type="URI"
        ),
        Statement(
            start=True, shape_id="@default", prop_id="dct:date", value_type="String"
        ),
    ]


def test_liststatements_with_shape_in_first_statement_only():
    """If shape IDs used previously, used for subsequent statements if no Shape ID."""
    csvrows_list = [
        {"shape_id": "@a", "prop_id": "dct:creator", "value_type": "URI"},
        {"shape_id": None, "prop_id": "dct:subject", "value_type": "URI"},
        {"shape_id": None, "prop_id": "dct:date", "value_type": "String"},
    ]
    assert list_statements(csvrows_list) == [
        Statement(start=True, shape_id="@a", prop_id="dct:creator", value_type="URI"),
        Statement(start=True, shape_id="@a", prop_id="dct:subject", value_type="URI"),
        Statement(start=True, shape_id="@a", prop_id="dct:date", value_type="String"),
    ]


def test_liststatements_with_shape_on_its_own_line():
    """If shape IDs used previously, used for subsequent statements if no Shape ID."""
    csvrows_list = [
        {"shape_id": "@a", "prop_id": None, "value_type": None},
        {"shape_id": None, "prop_id": "dct:creator", "value_type": "URI"},
        {"shape_id": None, "prop_id": "dct:subject", "value_type": "URI"},
    ]
    assert list_statements(csvrows_list) == [
        Statement(start=True, shape_id="@a", prop_id="dct:creator", value_type="URI"),
        Statement(start=True, shape_id="@a", prop_id="dct:subject", value_type="URI"),
    ]


def test_liststatements_with_shape_on_its_own_line_fields_with_none_are_implicit():
    """Fields with value None (here: 'annot' and 'start') are simply implicit."""
    csvrows_list = [
        {"shape_id": "@a", "prop_id": None, "value_type": None},
        {"shape_id": None, "prop_id": "dct:creator", "value_type": "URI"},
        {"shape_id": None, "prop_id": "dct:subject", "value_type": "URI"},
    ]
    assert list_statements(csvrows_list) == [
        Statement(
            start=True,
            shape_id="@a",
            prop_id="dct:creator",
            annot=None,
            value_type="URI",
        ),
        Statement(
            start=True,
            shape_id="@a",
            prop_id="dct:subject",
            prop_label=None,
            value_type="URI",
        ),
    ]
    assert list_statements(csvrows_list) == [
        Statement(start=True, shape_id="@a", prop_id="dct:creator", value_type="URI"),
        Statement(start=True, shape_id="@a", prop_id="dct:subject", value_type="URI"),
    ]


def test_liststatements_with_missing_value_type():
    """Should parse even if input lacks field 'value_type'."""
    as_input = [
        {
            "shape_id": "@book",
            "prop_id": "",
            "prop_label": "Book",
            "constraint_value": "",
            "annot": "",
        },
        {
            "shape_id": "",
            "prop_id": "rdf:type",
            "prop_label": "instance of",
            "constraint_value": "sdo:Book",
            "annot": "must be schema.org/Book",
        },
        {
            "shape_id": "",
            "prop_id": "rdf:type",
            "prop_label": "instance of",
            "constraint_value": "wd:Q571",
            "annot": "must be wikidata Book",
        },
    ]
    expected = [
        Statement(
            start=True,
            shape_id="@book",
            shape_label=None,
            prop_id="rdf:type",
            prop_label="instance of",
            mand=None,
            repeat=None,
            value_type=None,
            value_datatype=None,
            constraint_value="sdo:Book",
            constraint_type=None,
            shape_ref=None,
            annot="must be schema.org/Book",
        ),
        Statement(
            start=True,
            shape_id="@book",
            shape_label=None,
            prop_id="rdf:type",
            prop_label="instance of",
            mand=None,
            repeat=None,
            value_type=None,
            value_datatype=None,
            constraint_value="wd:Q571",
            constraint_type=None,
            shape_ref=None,
            annot="must be wikidata Book",
        ),
    ]
    assert list_statements(as_input) == expected
