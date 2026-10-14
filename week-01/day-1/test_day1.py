"""Week 1, Day 1 - classes, type hints, decorators, and a pydantic model.

Run me:  pytest week-01/day-1 -v
"""

import inspect

import pytest
from pydantic import ValidationError


@pytest.fixture
def basics(load):
    return load("basics.py")


class TestNote:
    def test_attributes(self, basics):
        note = basics.Note("  milk ", "two litres")
        assert note.title == "milk"
        assert note.body == "two litres"

    def test_body_is_optional(self, basics):
        assert basics.Note("milk").body == ""

    def test_two_notes_are_two_objects(self, basics):
        first, second = basics.Note("a"), basics.Note("b")
        assert first.title == "a" and second.title == "b", (
            "Each Note keeps its own title. If both say 'b', the title is being "
            "stored on the class rather than on self."
        )

    def test_summary(self, basics):
        assert basics.Note("milk", "two litres").summary() == "milk: two litres"

    def test_a_long_summary_is_cut(self, basics):
        note = basics.Note("plan", "x" * 50)
        assert note.summary(10) == "plan: " + "x" * 10 + "..."

    def test_exactly_the_width_is_not_cut(self, basics):
        assert basics.Note("p", "x" * 30).summary() == "p: " + "x" * 30

    def test_matches(self, basics):
        note = basics.Note("Dentist", "Friday at 3pm")
        assert note.matches("dentist") is True
        assert note.matches("FRIDAY") is True
        assert note.matches("monday") is False


class TestTypeHints:
    def test_every_method_is_annotated(self, basics):
        for name in ("__init__", "summary", "matches"):
            hints = inspect.get_annotations(getattr(basics.Note, name))
            assert "return" in hints, f"Note.{name} has no return type."
            assert len(hints) >= 2, f"Note.{name} has unannotated arguments."


class TestLogged:
    def test_it_records_the_name(self, basics):
        basics.CALLS.clear()

        @basics.logged
        def add(a, b):
            return a + b

        assert add(2, 3) == 5
        assert basics.CALLS == ["add"]

    def test_every_call_is_recorded(self, basics):
        basics.CALLS.clear()

        @basics.logged
        def ping():
            return "pong"

        ping()
        ping()
        assert basics.CALLS == ["ping", "ping"]

    def test_keyword_arguments_pass_through(self, basics):
        @basics.logged
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}"

        assert greet("Sam", greeting="Hi") == "Hi, Sam"

    def test_the_wrapper_keeps_the_name(self, basics):
        @basics.logged
        def save_note():
            return None

        assert save_note.__name__ == "save_note", (
            "The decorated function is now called 'wrapper'. FastAPI uses a "
            "function's name to label its routes - use functools.wraps."
        )


class TestNoteIn:
    def test_a_good_note(self, basics):
        note = basics.NoteIn(title="milk", body="two litres")
        assert note.title == "milk" and note.body == "two litres"

    def test_body_defaults_to_empty(self, basics):
        assert basics.NoteIn(title="milk").body == ""

    @pytest.mark.parametrize("data", [
        {"title": ""}, {"title": "x" * 81}, {"body": "no title"},
        {"title": "ok", "body": "x" * 2001}, {"title": 5},
    ])
    def test_bad_notes_are_refused(self, basics, data):
        with pytest.raises(ValidationError):
            basics.NoteIn(**data)
