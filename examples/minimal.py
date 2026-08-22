from sparkbrain.worlds import SwitchWorld, run_scenario

brain, frames = run_scenario(SwitchWorld.canonical_scenario())
for frame in frames:
    print(frame.external_event, frame.prediction)
