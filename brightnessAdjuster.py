#! /bin/python3 -B

## brightness adjuster
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

class BrightnessAdjuster:
	def parseArgs(self):
		parser = argparse.ArgumentParser(description="Increases or Decreases the brightness of the primary monitor.")
		
		parser.add_argument('-v',
			'--verbose',
			action="store_true",
			help="Enables verbose mode. Disabled by default.",
			dest="verbose")
		
		parser.add_argument('-m',
			'--max',
			help="Sets the maximum brightness. The default is 100.",
			default=100,
			dest="maxBrightness")

		parser.add_argument('-b',
			help="The feature number of the brightness parameter. The default is 10.",
			default=10,
			type=int,
			dest="vcp")

		parser.add_argument('-n',
			'--bus',
			help="""The bus number of the display. Setting this to the right value speeds up the operation of the tool significantly. The default is "x", which means not known.""",
			default="x",
			dest="bus")

		parser.add_argument("verb",
			help="""Can be "dec" to decrement the brightness by "value", "inc" to increment the brightness by "value", "test" to test the needed baseline functionality of the i2c stack and your devices and "set" to  simply set a given value.""")
		
		parser.add_argument("value",
			help="""The difference to be applied to the monitor's brightness or the value to set, if the verb "set" is used. """)
		
		self.args = parser.parse_args()

		try:
			self.args.value = int(self.args.value)
		except:
			eprint("Error: value must be an integer in base 10.")
			sys.exit(1)
		if {
			"inc" : True,
			"dec" : True,
			"test" : True,
			"set" : True
		}.get(self.args.verb, None) == None:
			eprint("""Error: verb can only be "dec", "inc", "set" or "test".""")
			sys.exit(1)

		if self.args.bus != "x":
			try:
				int(self.args.bus)
			except:
				eprint("ERROR: bus needs to be an integer.")
				sys.exit(1)

	def getBrightness(self):
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

		brightness = stdout.decode().split()[3]
		
		if self.args.verbose:
			print(stdout.decode())

		try:
			brightness = int(brightness)
		except:
			eprint("ERROR: Could not decode {} as integer base 10".format(brightness))
			sys.exit(1)


		return brightness

	def setBrightness(self, value):
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

	def test(self):
		cmd = "ddcutil "
		if self.args.bus != "x":
			cmd += " --bus={} --nodetect".format(self.args.bus)

		cmd += " capabilities"

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

		print("All okay.")

		return

	def run(self):
		self.parseArgs()
		if self.args.verb == "test":
			self.test()
		elif self.args.verb == "set":
			self.setBrightness(self.args.value)
		else:			
			brightness = self.getBrightness()

			newBrightness = {
				"inc" : lambda x: brightness + x,
				"dec" : lambda x: brightness - x,
				}.get(self.args.verb)(self.args.value)
						
			if newBrightness > self.args.maxBrightness:
				# exit silently, maximum brightness was reached.
				if self.args.verbose:
					print("Maximum brightness reached.")
				sys.exit(0)

			self.setBrightness(newBrightness)

if __name__ == '__main__':
	adjuster = BrightnessAdjuster()
	adjuster.run()