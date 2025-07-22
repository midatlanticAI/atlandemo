import sys, os
import numpy as np

current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(os.path.dirname(current_dir))
controllers_path = os.path.join(project_root, 'controllers')
if controllers_path not in sys.path:
    sys.path.insert(0, controllers_path)

from controllers.adaptive_bilevel_controller import AdaptiveBilevelController


def test_obstructive_increase():
    ctl = AdaptiveBilevelController()
    ipap0, epap0 = ctl.get_state()['ipap'], ctl.get_state()['epap']
    ipap1, epap1 = ctl.update('obstructive', leak_lpm=20)
    assert ipap1 > ipap0 and epap1 > epap0
    # Delta limited
    assert ipap1 - ipap0 <= ctl.max_delta_per_breath


def test_clear_decay():
    ctl = AdaptiveBilevelController()
    # raise pressure first
    for _ in range(5):
        ctl.update('obstructive', leak_lpm=20)
    ipap_high = ctl.get_state()['ipap']
    # send clear events
    for _ in range(ctl.decay_breaths + 1):
        ctl.update('central', leak_lpm=20)
    ipap_after = ctl.get_state()['ipap']
    assert ipap_after < ipap_high


def test_leak_alarm_stepdown():
    ctl = AdaptiveBilevelController()
    # elevate pressures
    for _ in range(10):
        ctl.update('obstructive', leak_lpm=20)
    ipap_before = ctl.get_state()['ipap']
    # sustained leak
    for _ in range(ctl.leak_breaths):
        ctl.update('central', leak_lpm=ctl.leak_threshold + 5)
    state = ctl.get_state()
    assert state['alarm'] == 'leak_high'
    assert state['ipap'] <= ipap_before
    # leak resolves
    ctl.update('central', leak_lpm=10)
    assert ctl.get_state()['alarm'] is None 