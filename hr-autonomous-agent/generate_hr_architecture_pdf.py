from pathlib import Path
import textwrap

PAGE_W = 612
PAGE_H = 792
LEFT = 54
RIGHT = 558
TOP = 64
BOTTOM = 52

STYLES = {
    "title": ("F2", 18, 24, 0.52),
    "subtitle": ("F1", 11, 15, 0.50),
    "section": ("F2", 12, 18, 0.52),
    "body": ("F1", 10.5, 13, 0.50),
    "mono": ("F3", 8.8, 11, 0.60),
    "small": ("F1", 9, 12, 0.50),
}


def esc(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def wrap(text: str, width: int, initial: str = "", subsequent: str = ""):
    return textwrap.wrap(
        text,
        width=width,
        break_long_words=False,
        initial_indent=initial,
        subsequent_indent=subsequent,
    )


def width_estimate(text: str, font: str, size: float) -> float:
    factor = STYLES.get("body")[3]
    if font == "F2":
        factor = 0.54
    elif font == "F3":
        factor = 0.60
    return len(text) * size * factor


class Page:
    def __init__(self, number: int):
        self.number = number
        self.y = PAGE_H - TOP
        self.ops = []

    def text(self, x: float, y: float, text: str, font: str, size: float):
        self.ops.append(f"BT /{font} {size} Tf 1 0 0 1 {x:.1f} {y:.1f} Tm ({esc(text)}) Tj ET")

    def line(self, x1: float, y1: float, x2: float, y2: float):
        self.ops.append("0 G 0.8 w")
        self.ops.append(f"{x1:.1f} {y1:.1f} m {x2:.1f} {y2:.1f} l S")

    def write(self, style: str, text: str = "", align: str = "left"):
        font, size, leading, _ = STYLES[style]
        if self.y < BOTTOM:
            raise RuntimeError(f"Page {self.number} overflow")
        if text:
            x = LEFT
            if align == "center":
                x = max(LEFT, (PAGE_W - width_estimate(text, font, size)) / 2)
            self.text(x, self.y, text, font, size)
        self.y -= leading

    def paragraph(self, text: str, width: int = 90):
        for line in wrap(text, width):
            self.write("body", line)

    def bullets(self, items, width: int = 86):
        for item in items:
            for line in wrap(item, width, initial="- ", subsequent="  "):
                self.write("body", line)
            self.y -= 2

    def mono_block(self, lines):
        for line in lines:
            self.write("mono", line)

    def table_block(self, rows, left_col: int = 24, right_col: int = 52):
        self.write("mono", f"{'Setting':<{left_col}}  Value")
        self.write("mono", f"{'-' * left_col}  {'-' * right_col}")
        for key, value in rows:
            wrapped = textwrap.wrap(value, width=right_col, break_long_words=False) or [""]
            self.write("mono", f"{key:<{left_col}}  {wrapped[0]}")
            for extra in wrapped[1:]:
                self.write("mono", f"{'':<{left_col}}  {extra}")

    def footer(self):
        self.line(LEFT, 34, RIGHT, 34)
        self.text(RIGHT - 34, 20, f"Page {self.number}", "F1", 9)

    def stream(self):
        return "\n".join(self.ops) + "\n"


def build_pages():
    pages = []

    p1 = Page(1)
    p1.write("title", "HR Autonomous Agent Architecture", "center")
    p1.write("subtitle", "HR-operations-first reasoning, execution, recovery, and reflection", "center")
    p1.y -= 6
    p1.line(LEFT, p1.y + 8, RIGHT, p1.y + 8)
    p1.y -= 8
    p1.write("section", "1. Overview")
    p1.paragraph(
        "The agent is designed as a controlled autonomous workflow for HR operations. It interprets goals in business terms first, prepares the target environment, inspects relevant application logic, executes the smallest safe action, verifies the outcome, and continuously improves through recorded memory and reflection."
    )
    p1.y -= 6
    p1.write("section", "2. Key Features")
    p1.bullets([
        "Business-operation-first interpretation of user goals.",
        "Warm-start behavior that reuses known context before broad discovery.",
        "Mandatory reasoning and action justification before mutation.",
        "Targeted system inspection to support safe execution.",
        "Bounded retry behavior with explicit recovery logic.",
        "Persistent memory, logs, and post-run reflection.",
    ])
    p1.y -= 6
    p1.write("section", "3. Design Goals")
    p1.bullets([
        "Make HR outcomes the primary decision lens before treating a request as an engineering task.",
        "Start quickly by using configured startup data and warm context by default.",
        "Prefer narrow, reversible operations with verification after every meaningful step.",
        "Escalate rather than guess when confidence or evidence is insufficient.",
        "Retain lessons across runs so later execution becomes safer and faster.",
    ])
    p1.y -= 6
    p1.write("section", "4. Core Operating Principles")
    p1.bullets([
        "Summary-only inspection output during normal operation.",
        "Targeted discovery before broad rediscovery.",
        "Read-first validation before write actions when possible.",
        "Reflection after every completed or terminally failed run.",
    ])
    p1.footer()
    pages.append(p1)

    p2 = Page(2)
    p2.write("title", "HR Autonomous Agent Architecture", "center")
    p2.write("subtitle", "System structure and core components", "center")
    p2.y -= 6
    p2.line(LEFT, p2.y + 8, RIGHT, p2.y + 8)
    p2.y -= 8
    p2.write("section", "5. System Architecture")
    p2.mono_block([
        "+-----------------------------+",
        "| User Goal / CLI Invocation  |",
        "+-----------------------------+",
        "              |",
        "              v",
        "+-----------------------------+",
        "| Workflow Contract          |",
        "| Runtime Configuration      |",
        "| Strategy + Safety Rules    |",
        "+-----------------------------+",
        "              |",
        "              v",
        "+-----------------------------+",
        "| Warm Start + Session Prep  |",
        "+-----------------------------+",
        "              |",
        "       -----------------------------",
        "       |             |             |",
        "       v             v             v",
        "   Reasoning     Discovery     Execution",
        "       |                           |",
        "       --------> Verification <----",
        "                      |",
        "                 Recovery",
        "                      |",
        "             Reflection + Memory",
    ])
    p2.y -= 8
    p2.write("section", "6. Component Responsibilities")
    p2.write("mono", f"{'Component':<18}  Responsibility")
    p2.write("mono", f"{'-' * 18}  {'-' * 52}")
    component_rows = [
        ("Workflow Layer", "Defines the governing contract for runtime behavior."),
        ("Config Layer", "Supplies startup behavior, environment assumptions, defaults, and safety settings."),
        ("Reasoning Agent", "Interprets intent and produces the safest execution path."),
        ("Discovery Agent", "Refreshes only the technical facts needed for the active goal."),
        ("Execution Agent", "Performs one justified action at a time and verifies the outcome."),
        ("Recovery Agent", "Diagnoses failures, applies narrow corrections, and retries only when justified."),
        ("Reflection Agent", "Evaluates results and improves future heuristics."),
        ("State & Memory", "Stores workflow progress, history, and operational evidence."),
    ]
    for key, value in component_rows:
        wrapped = textwrap.wrap(value, width=52, break_long_words=False) or [""]
        p2.write("mono", f"{key:<18}  {wrapped[0]}")
        for extra in wrapped[1:]:
            p2.write("mono", f"{'':<18}  {extra}")
    p2.footer()
    pages.append(p2)

    p3 = Page(3)
    p3.write("title", "HR Autonomous Agent Architecture", "center")
    p3.write("subtitle", "Runtime flow and decision behavior", "center")
    p3.y -= 6
    p3.line(LEFT, p3.y + 8, RIGHT, p3.y + 8)
    p3.y -= 8
    p3.write("section", "7. Runtime Workflow")
    p3.mono_block([
        "Receive Goal",
        "    |",
        "Load Workflow Contract and Runtime Settings",
        "    |",
        "Load Warm State and Known Context",
        "    |",
        "Validate Service Availability and Session State",
        "    |",
        "Reasoning Agent: classify goal and choose safest path",
        "    |",
        "Discovery Agent: inspect only the modules needed now",
        "    |",
        "Execution Agent: perform smallest justified action",
        "    |",
        "Verification: confirm response and state change",
        "    |",
        "Recovery Agent: retry only if failure is recoverable",
        "    |",
        "Reflection Agent: store lessons for future runs",
    ])
    p3.y -= 8
    p3.write("section", "8. Confidence Model")
    p3.bullets([
        "High confidence: proceed with normal safeguards because the business meaning, module, and action path are all supported.",
        "Medium confidence: proceed only with narrow and reversible actions plus explicit verification.",
        "Low confidence: inspect further or escalate instead of guessing.",
    ])
    p3.y -= 6
    p3.write("section", "9. Example Reasoning Snapshot")
    p3.mono_block([
        "Goal: approve pending attendance requests for last week",
        "Task Type: attendance operations",
        "Confidence: Medium",
        "Relevant Areas: attendance, approval flow, authentication",
        "Inferred Action Path: authenticate -> confirm scope ->",
        "                      approve eligible requests -> verify",
        "Strategy:",
        "1. Validate configured backend and active session",
        "2. Confirm attendance approval workflow",
        "3. Execute the smallest safe approval action",
        "4. Verify the post-action state",
        "5. Record the result, memory update, and reflection",
    ])
    p3.footer()
    pages.append(p3)

    p4 = Page(4)
    p4.write("title", "HR Autonomous Agent Architecture", "center")
    p4.write("subtitle", "Configured profile, guardrails, and completion guarantees", "center")
    p4.y -= 6
    p4.line(LEFT, p4.y + 8, RIGHT, p4.y + 8)
    p4.y -= 8
    p4.write("section", "10. Configured Operating Profile")
    p4.table_block([
        ("Entry Command", 'agent run "<goal>"'),
        ("Default Persona", "hr operations specialist"),
        ("Goal Interpretation", "business-operation-first"),
        ("Startup Mode", "configured-path warm-start"),
        ("Runtime Shell", "powershell"),
        ("Warm Cache Reuse", "enabled when the active target still matches"),
        ("Discovery Preference", "targeted refresh before any broad rediscovery"),
        ("Authentication", "required before task execution"),
        ("Retry Limit", "3"),
        ("Safe Mode", "enabled"),
        ("Bulk Operations", "disabled unless reasoning marks them explicitly safe"),
        ("CLI Visibility", "summary-only during inspection"),
        ("Action Reasoning", "required before every execution step"),
        ("Memory Update", "after each task and major state transition"),
        ("Reflection", "required after completion or terminal failure"),
    ])
    p4.y -= 6
    p4.write("section", "11. Risk and Recovery Guardrails")
    p4.bullets([
        "Prefer read-only verification before any write action.",
        "Avoid broad or bulk changes unless the reasoning step explicitly justifies them.",
        "Retry only when the failure is plausibly recoverable and something meaningful changes.",
        "Escalate when evidence is conflicting, destructive side effects appear, or confidence remains too low.",
    ])
    p4.y -= 6
    p4.write("section", "12. Completion Guarantees")
    p4.bullets([
        "A run ends only after it reaches a terminal outcome such as completed, failed, or escalated.",
        "Execution history, failure records, state tracking, task memory, and reflection must all be updated.",
        "Recorded lessons are expected to influence later runs so the system becomes safer and more consistent over time.",
    ])
    p4.footer()
    pages.append(p4)

    return pages


def build_pdf(output_path: Path):
    streams = [page.stream() for page in build_pages()]
    objects = [None, None, None]
    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>")

    page_object_numbers = []
    for stream in streams:
        stream_bytes = stream.encode("latin-1")
        content_num = len(objects)
        objects.append(f"<< /Length {len(stream_bytes)} >>\nstream\n{stream}endstream")
        page_num = len(objects)
        objects.append(
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 3 0 R /F2 4 0 R /F3 5 0 R >> >> /Contents {content_num} 0 R >>"
        )
        page_object_numbers.append(page_num)

    objects[1] = "<< /Type /Catalog /Pages 2 0 R >>"
    kids = " ".join(f"{n} 0 R" for n in page_object_numbers)
    objects[2] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_object_numbers)} >>"

    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number in range(1, len(objects)):
        offsets.append(len(pdf))
        pdf.extend(f"{number} 0 obj\n{objects[number]}\nendobj\n".encode("latin-1"))
    xref_pos = len(pdf)
    pdf.extend(f"xref\n0 {len(objects)}\n".encode("latin-1"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))
    pdf.extend(
        f"trailer\n<< /Size {len(objects)} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("latin-1")
    )
    output_path.write_bytes(pdf)


if __name__ == "__main__":
    build_pdf(Path("hr-autonomous-agent/hr_autonomous_agent_architecture.pdf"))