#! /bin/python3 -B

## input switcher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Noel Kuntze "Thermi" <noel.kuntze+github@thermi.consulting>

import argparse
import subprocess
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class InputSwitcher:
	def parseArgs(self):
		parser = argparse.ArgumentParser(description="Cycles between inputs of the primary monitor.")
		
		parser.add_argument('-v',
			'--verbose',
			action="store_true",
			help="Enables verbose mode. Disabled by default.",
			dest="verbose")
		

		parser.add_argument('-b',
			help="The feature number of the input source parameter. The default is 60.",
			default=60,
			type=int,
			dest="vcp")

		parser.add_argument('-n',
			'--bus',
			help="""The bus number of the display. Setting this to the right value speeds up the operation of the tool significantly. The default is "x", which means not known.""",
			default="x",
			dest="bus")

		parser.add_argument("values",
			nargs='+',
			help="""The list of values to cycle between.""")
		
		self.args = parser.parse_args()

		if len(self.args.values) < 2:
			eprint("""ERROR: At least two values must be given.""")
			sys.exit(1)

		if self.args.bus != "x":
			try:
				int(self.args.bus)
			except:
				eprint("ERROR: bus needs to be an integer.")
				sys.exit(1)

	def getInputSource(self):
		cmd = "ddcutil -t"
		if self.args.bus != "x":
			cmd += " --bus={} --nodetect".format(self.args.bus)

		cmd += " getvcp {}".format(self.args.vcp)
		cmd = cmd.split()

		if self.args.verbose:
			print("cmd: {}".format(cmd))

		process = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		stdout,stderr = process.communicate()

		if process.returncode:
			eprint("ERROR: ddcutil exited with an error: {}".format(stderr.decode()))
			eprint("ERROR: printed on stdout: {}".format(stdout.decode()))
			sys.exit(1)

		inputSource = stdout.decode().split()[3]
		
		if self.args.verbose:
			print(stdout.decode())

		return inputSource

	def setInputSource(self, value):
		cmd = "ddcutil -t"
		if self.args.bus != "x":
			cmd += " --bus={} --nodetect".format(self.args.bus)

		cmd += " setvcp {} {}".format(self.args.vcp, value)
		cmd = cmd.split()
		
		if self.args.verbose:
			print("cmd: {}".format(cmd))

		process = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		stdout,stderr = process.communicate()

		if process.returncode:
			eprint("ERROR: ddcutil exited with an error: {}".format(stderr.decode()))
			eprint("ERROR: printed on stdout: {}".format(stdout.decode()))
			sys.exit(1)

		if self.args.verbose:
			print("stdout: {}".format(stdout.decode()))

		return 

	def run(self):
		self.parseArgs()
		try:
			position = self.args.values.index(self.getInputSource())
		except:
			# item not in list
			if self.args.verbose:
				print("Item not in list. Setting first value.")
				self.setInputSource(self.args.values[0])
		else:
			if self.args.verbose:
				print("Setting {} as input.".format(self.args.values[(position+1)%len(self.args.values)]))
			self.setInputSource(self.args.values[(position+1)%len(self.args.values)])

if __name__ == '__main__':
	adjuster = InputSwitcher()
	adjuster.run()