# CIA triad classification experiment

One incident can affect several parts of the CIA triad. The classifier reads fictional events and records all their confidentiality, integrity, and availability labels. The experiment compares each result with a label set written in advance.

Use Python 3 and its standard library. Run these commands from the checkout root.

```sh
python3 applied-labs/r34-t049/example.py
python3 -m unittest discover -s ./applied-labs/r34-t049 -p "test_*.py"
```

| Scenario | Observed events | Expected labels |
| --- | --- | --- |
| Exposed invoices | Unauthorized reading | Confidentiality |
| Edited order totals | Altered records | Integrity |
| Checkout outage | Unavailable service | Availability |
| Leaked and changed files | Unauthorized reading and altered records | Confidentiality and integrity |
| Compromised booking app | Unauthorized reading, altered records, and unavailable service | Confidentiality, integrity, and availability |
| Routine maintenance | Routine log review | Empty set |

Run the same classifier on the first one, three, and six scenarios. A result counts as correct only if every expected label is present and there are no extra labels. Count the events examined as a measure of work.

```text
Batch size 1: 1/1 exact matches, events examined = 1
Batch size 3: 3/3 exact matches, events examined = 3
Batch size 6: 6/6 exact matches, events examined = 9
```

The smallest batch covers one impact. The second covers all three in isolation. The largest also covers incidents with several labels and a routine event with none. It checks more behaviors and examines nine events. These counts describe this fixture. The program uses preset event names and does not classify free-text reports or measure performance on real incidents.
