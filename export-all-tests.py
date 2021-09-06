#!/usr/bin/env python3

import subprocess, os, sys

EXPORT_DIR = 'exported'

try:
	os.mkdir(EXPORT_DIR)
except FileExistsError:
	pass #that's fine!

def run_export(basename, did, wid, eid):
	print(f"Exporting '{EXPORT_DIR}/{basename}.svg' from https://cad.onshape.com/documents/{did}/w/{wid}/e/{eid} ...")

	try:
		os.unlink(f'{EXPORT_DIR}/{basename}.svg')
	except FileNotFoundError:
		pass
	try:
		os.unlink(f'{EXPORT_DIR}/{basename}.log')
	except FileNotFoundError:
		pass

	with open(f"{EXPORT_DIR}/{basename}.log", 'w') as log:
		ret = subprocess.run([
			'python2', 'faster_script.py',
			'--did', did,
			'--wid', wid,
			'--eid', eid,
			'--output', f'{EXPORT_DIR}/{basename}.svg'
		], stdout=log, stderr=subprocess.STDOUT)
	if ret.returncode:
		print(f"  Failed (return code {ret.returncode}), log is in '{basename}.log'.")
	else:
		print(f"  Succes. Log is in '{basename}.log'.")


#These haven't been added to the list yet because I am not sure what they are:

# document evaluate test
'''
did = "36ad7f2f4e1268bfd6df7618"
wid = "b9622808903e3a2f41542423"
eid = "c93892577d28abd4165cc7f8"
'''

# box
'''
# 1
did = "342cee7fe5c2effe369c8dc3"
wid = "1362f0d767136d7d96f8c33a"
eid = "7d2020bde3f6f951e141da13"
'''

run_export('box', "a793a3e438b3a8a7859e3244", "d66b8b4a9bb905cb4090461b", "bdaa56060d3b9fbbd545f5e7")
run_export('harder-box', did="b3ea79d344251df6495836cc", wid="37bdc8e4d3b079cb2acffc8d", eid="f5ad63f423a46fabd7ae042d")
run_export('tilt', did="34f358b08844ead297ba74f6", wid="275579ddc140dfe00b49da5e", eid="745d66adff6ff8d563831f69")
run_export('tab-and-slot', did="8340450a9fd4cc9837a89656", wid="d01511894f7b5682a854cff1", eid="7394a48da4001f45b67489f8")
run_export('slotted', did="d934491f87de847f2d4bccac", wid="2abe57ce0ac3f5cbe20ee001", eid="54bf2b3c2414d066af55dcec")
run_export('nur-box', did="b9e234f251a607d0d9ce0e9a", wid="c45c28f23e25a36988322572", eid="960e4e2c57080fe58395912f")
run_export('nur-tslot-box', did="e163a13cdcf203350a1a1ce2", wid="50030d897bfa683e0da3be9a", eid="bd80ff440cc33e6e73cdfc32")
run_export('bird-house', did="939592630e92d28997eb29da", wid="3ce34ba3e44b5d34438378b5", eid="93d44db90466c59ec8203929")
run_export('chair', did="3b2c4abe65815a81dc709aa8", wid="97f88956c7d4edca883aa894", eid="56e319b635b4794492166d23")
run_export('raspberry-pi', did="2583e97f0a333a38d03fc29e", wid="eb85696d78b9ca148a08977d", eid="2a7422c47555a3ece3c994f1")
run_export('printer', did="a7c63a8b20c4b911aa9ee0dd", wid="0ff2f9dda8a0ccfbf9ba7679", eid="b01cb8d18f450ea6f16185b8")
run_export('oct-candle', did="da1045b9fbea9a5b3b6516c8", wid="33af49ef094546773e9a5e40", eid="a87ebba31cd6f918db244ce9")
run_export('house', did="cb694ed0b30f8354559273f1", wid="733bb59e3d32dfa30a2e47c9", eid="3616eb0cf82bed75c4f40e6e")
run_export('arcade', did="0ada0244726dbd2eccf605c4", wid="74af87e822132b87fad407ce", eid="4a428daee5c62a5644aef745")
run_export('laptop', did="4553f9339af206c9dbac6b64", wid="597b7587765e8d04f6a1b00e", eid="197ab26790f10eddbd774050")
run_export('windmill', did="029851f598e19e5b49784a9b", wid="a902a5bd9d5432b35d9b372c", eid="2a77759f7830e9bad303a87b")
run_export('dice', did="0fc385d7050f56bc9a1adae3", wid="63eddd978595af3059316e76", eid="c3a9b1ec7ac169d26c478ced")
run_export('tray', did="b50e40745ce6ce567e69c657", wid="85237d35c764cbc9b835ef62", eid="6868d15c5e6449716872430e")
run_export('tests', did="175191ecf6dfd33fc82e76eb", wid="4b3b42dc77a0a6698a0372c5", eid="843560ba2c50135fa96a61ec")
