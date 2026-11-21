# SecOps Scenario Evaluator with Recovery (R34-T008)

Extends **4.4 End of module quiz** by demonstrating failure handling and recovery:
- An invalid input (missing asset) fails with a structured error.
- The next valid input recovers and passes cleanly.

## Running Tests
```bash
python3 -m unittest discover -s ./applied-labs/r34-t008 -p "test_*.py"
```
