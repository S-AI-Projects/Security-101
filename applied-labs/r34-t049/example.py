"""Compare a CIA classifier on three sizes of the same fictional fixture."""

IMPACT_BY_EVENT = {
    "unauthorized reading": "confidentiality",
    "altered records": "integrity",
    "unavailable service": "availability",
}

# Each entry holds a name, the observed events, and independently set labels.
SCENARIOS = (
    ("exposed invoices", ("unauthorized reading",), {"confidentiality"}),
    ("edited order totals", ("altered records",), {"integrity"}),
    ("checkout outage", ("unavailable service",), {"availability"}),
    ("leaked and changed files", ("unauthorized reading", "altered records"),
     {"confidentiality", "integrity"}),
    ("compromised booking app", ("unauthorized reading", "altered records", "unavailable service"),
     {"confidentiality", "integrity", "availability"}),
    ("routine maintenance", ("routine log review",), set()),
)
SIZES = (1, 3, 6)


def classify(events: tuple[str, ...]) -> set[str]:
    labels = set()
    for event in events:
        impact = IMPACT_BY_EVENT.get(event)
        if impact is not None:
            labels.add(impact)
    return labels


def evaluate(scenarios: tuple) -> tuple[int, int]:
    """Count exact label-set matches and input events examined."""
    matches = 0
    events_examined = 0
    for _, events, expected in scenarios:
        matches += classify(events) == expected
        events_examined += len(events)
    return matches, events_examined


if __name__ == "__main__":
    for size in SIZES:
        matches, events_examined = evaluate(SCENARIOS[:size])
        print(f"Batch size {size}: {matches}/{size} exact matches, events examined = {events_examined}")
