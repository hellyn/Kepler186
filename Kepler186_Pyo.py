from pyo import *

s = Server().boot()
s.start()
wav = SquareTable()
env = CosTable([(0,0), (0,1), (200,.5), (30,0)])
met = Metro(.200, 1000).play()
amp = TrigEnv(met, table=env, mul=.1)
pit = TrigXnoiseMidi(met, dist='loopseg', x1=20, scale=1, mrange=(48,84))
out = Osc(table=wav, freq=pit, mul=amp).out()
s.gui(locals())