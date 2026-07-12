import urllib.request
from html.parser import HTMLParser


class CalculatorPageParser(HTMLParser):
    """Parse calculator page to extract form elements."""

    def __init__(self):
        super().__init__()
        self.inputs = []  # list of (type, name) for input elements
        self.select_options = {}  # {name: [values]}
        self.buttons = []  # list of (type, name, text) tuples
        self._in_form = False
        self._current_select_name = None
        self._form_method = None
        self._form_action = None
        self._current_button_type = None
        self._current_button_name = None
        self._button_text_parts = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "form":
            self._in_form = True
            self._form_method = attrs_dict.get("method", "").upper()
            self._form_action = attrs_dict.get("action", "")
        elif tag == "input" and self._in_form:
            inp_type = attrs_dict.get("type", "text")
            name = attrs_dict.get("name", "")
            self.inputs.append((inp_type, name))
        elif tag == "select" and self._in_form:
            self._current_select_name = attrs_dict.get("name", "")
            self.select_options[self._current_select_name] = []
        elif tag == "option":
            if self._current_select_name is not None:
                val = attrs_dict.get("value", "")
                self.select_options[self._current_select_name].append(val)
        elif tag == "button" and self._in_form:
            self._current_button_type = attrs_dict.get("type", "")
            self._current_button_name = attrs_dict.get("name", "")
            self._button_text_parts = []

    def handle_endtag(self, tag):
        if tag == "form":
            self._in_form = False
        elif tag == "select":
            self._current_select_name = None
        elif tag == "button" and self._in_form:
            text = "".join(self._button_text_parts)
            self.buttons.append((self._current_button_type, self._current_button_name, text))
            self._current_button_type = None
            self._current_button_name = None
            self._button_text_parts = []

    def handle_data(self, data):
        if self._current_button_name is not None:
            self._button_text_parts.append(data)


def test_calculator_interface():
    """Verify the calculator UI meets all acceptance criteria for US-001."""

    # Criterion 1: App serves plain HTML at root route /
    req = urllib.request.Request("http://localhost:41003/")
    with urllib.request.urlopen(req, timeout=5) as resp:
        status = resp.status
        content_type = resp.headers.get("Content-Type", "")
        html = resp.read().decode("utf-8")

    assert status == 200, f"Expected 200, got {status}"
    assert "text/html" in content_type, f"Not HTML: {content_type}"

    # Parse the page
    parser = CalculatorPageParser()
    parser.feed(html)

    # Criterion 2: Exactly two input fields for numbers
    number_inputs = [i for i in parser.inputs if i[0] == "number"]
    assert len(number_inputs) == 2, (
        f"Expected exactly 2 number inputs, found {len(number_inputs)}: {number_inputs}"
    )

    # Criterion 3: Way to pick one of four basic operations
    operation_values = parser.select_options.get("operation", [])
    expected_ops = {"add", "subtract", "multiply", "divide"}
    actual_ops = set(operation_values)
    assert expected_ops == actual_ops, (
        f"Expected operations {expected_ops}, found {actual_ops}"
    )

    # Criterion 4: Calculate button present and submits form to server
    calc_buttons = [b for b in parser.buttons if "Calculate" in b[2]]
    assert len(calc_buttons) >= 1, (
        f"No 'Calculate' submit button found. Buttons: {parser.buttons}"
    )
    # Button type should be submit so it submits the form
    btn_type = calc_buttons[0][0]
    assert btn_type == "submit", (
        f"Calculate button type is '{btn_type}', expected 'submit'"
    )
    # Form action should point to server (/)
    assert parser._form_action == "/", (
        f"Form action is '{parser._form_action}', expected '/'"
    )