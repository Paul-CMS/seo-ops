def t_harness(h):
    h.check("extra scenario modules load (tests/checks)", h.SB.exists())


SCENARIOS = [t_harness]
