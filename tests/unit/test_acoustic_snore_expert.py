import sys, os, numpy as np

current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(os.path.dirname(current_dir))
expert_path = os.path.join(project_root, 'expert_modules')
for p in [project_root, expert_path]:
    if p not in sys.path:
        sys.path.insert(0, p)

from expert_modules.acoustic_snore_expert import AcousticSnoreExpert

SR = 2000


def _make_audio(label: str, duration_s: float = 1.0):
    t = np.linspace(0, duration_s, int(SR * duration_s), endpoint=False)
    if label == 'loud_snore':
        amp = 0.3
    elif label == 'no_snore':
        amp = 0.001
    else:
        amp = 0.08
    return amp * np.sin(2 * np.pi * 100 * t)


def test_loud_snore():
    expert = AcousticSnoreExpert(name='snore', domain='acoustic')
    audio = _make_audio('loud_snore')
    resp = expert.process_query('detect_snore', {'audio': audio, 'sr': SR})
    assert resp.answer == 'loud_snore'
    assert resp.confidence > 0.5


def test_no_snore():
    expert = AcousticSnoreExpert(name='snore', domain='acoustic')
    audio = _make_audio('no_snore')
    resp = expert.process_query('detect_snore', {'audio': audio, 'sr': SR})
    assert resp.answer == 'no_snore'
    assert resp.confidence < 0.4 