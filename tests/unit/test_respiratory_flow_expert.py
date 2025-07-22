import sys
import os
import numpy as np

# Ensure import paths
current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(os.path.dirname(current_dir))
expert_modules_path = os.path.join(project_root, 'expert_modules')

for path in [project_root, expert_modules_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

from expert_modules.respiratory_flow_expert import RespiratoryFlowExpert


def _generate_signal(event: str, sr: int = 25, duration: float = 10.0):
    """Generate synthetic respiratory flow signal."""
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    if event == "central":
        # Near-zero flow with tiny noise
        return 0.002 * np.random.randn(len(t))
    elif event == "obstructive":
        # 1 Hz obstruction oscillation plus baseline noise
        return 0.5 * np.sin(2 * np.pi * 1.0 * t) + 0.05 * np.random.randn(len(t))
    else:
        raise ValueError("Unknown event type")


def test_classify_central():
    expert = RespiratoryFlowExpert(name="resp_flow", domain="respiratory")
    flow = _generate_signal("central")
    context = {"flow": flow, "sr": 25}
    response = expert.process_query("classify_airway_event", context)
    assert response.answer == "central", f"Expected central, got {response.answer}"
    assert response.confidence >= 0.1


def test_classify_obstructive():
    expert = RespiratoryFlowExpert(name="resp_flow", domain="respiratory")
    flow = _generate_signal("obstructive")
    context = {"flow": flow, "sr": 25}
    response = expert.process_query("classify_airway_event", context)
    assert response.answer == "obstructive", f"Expected obstructive, got {response.answer}"
    assert response.confidence >= 0.1 