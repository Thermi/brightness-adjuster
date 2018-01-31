Brightness Adjuster
=====================

Increases or decreases the brightness of the primary monitor.
This is just a simple wrapper around ddcutil.

It enables you to easily manipulate the screen brightness via keyboard shortcuts. Just bind the tool with the proper arguments to some keys using your DE's (Desktop Environment) tools.

Dependencies:
* Python3
* [ddcutil](https://github.com/rockowitz/ddcutil "ddcutil Github repository")
* i2c_dev kernel module


# How To Use

## Setup
1. insert the module i2c_dev

   `# modprobe i2c_dev`

2. Check the group of the pseudo files `/dev/i2c-*` and make sure you can write to them
   
   ```$ ls -l /dev/i2c-*
   crw-rw---- 1 root i2c 89,  0 30. Jan 23:42 /dev/i2c-0
   crw-rw---- 1 root i2c 89,  1 30. Jan 23:42 /dev/i2c-1
   crw-rw---- 1 root i2c 89, 10 30. Jan 23:42 /dev/i2c-10
   crw-rw---- 1 root i2c 89, 11 30. Jan 23:42 /dev/i2c-11
   crw-rw---- 1 root i2c 89,  2 30. Jan 23:42 /dev/i2c-2
   crw-rw---- 1 root i2c 89,  3 30. Jan 23:42 /dev/i2c-3
   crw-rw---- 1 root i2c 89,  4 30. Jan 23:42 /dev/i2c-4
   crw-rw---- 1 root i2c 89,  5 30. Jan 23:42 /dev/i2c-5
   crw-rw---- 1 root i2c 89,  6 30. Jan 23:42 /dev/i2c-6
   crw-rw---- 1 root i2c 89,  7 30. Jan 23:42 /dev/i2c-7
   crw-rw---- 1 root i2c 89,  8 30. Jan 23:42 /dev/i2c-8
   crw-rw---- 1 root i2c 89,  9 30. Jan 23:42 /dev/i2c-9
   ```

   If the files are owned by a specific group (not root, but e.g. `i2c`):
      1. Add yourself to that group: `usermod -a -G thatGroup yourusername`
      2. Reload the udev rules.
         `# udevadm control --reload-rules && udevadm trigger`
      6. Now you need to log out and log back in or get a new login shell and run the script.
         `$ ./brightnessAdjuster.py test 0`
         If the script worked, you're all set.
   
   else
      1. Create the group i2c.
         `# groupadd -r i2c`
      2. Add yourself to that group.
         `# usermod -a -G thatGroup yourusername`
      3. Copy the udev rule file to /etc/udev/rules.d/.
         `# cp 60-i2c-devices.rule /etc/udev/rules.d`
      4. Reload the udev rules.
         `# udevadm control --reload-rules && udevadm trigger`
      5. Check the group and access rights of the `i2c-*` files.
         `ls -l /dev/i2c-*`
         Make sure the group is now `i2c`.
      6. If that worked, you need to log out and log back in or get a new login shell and run the script.
         `$ ./brightnessAdjuster.py test 0`
         If the script worked, you're all set.

## Usage

Four verbs are available:
* dec
  decrements (decreases/lowers) the brightness of the first monitor by the given value.
* inc
  increments (increases/raise) the brightness of the first monitor by the given value.
* set
  set the brightness of the first monitor by the given value.
* test
  Test if the tool can access can find and access the primary monitor.

### Help Message
```
$ ./brightnessAdjuster.py -h
usage: brightnessAdjuster.py [-h] [-v] [-m MAXBRIGHTNESS] [-b VCP] [-n BUS]
                             verb value

Increases or Decreases the brightness of the primary monitor.

positional arguments:
  verb                  Can be "dec" to decrement the brightness by "value",
                        "inc" to increment the brightness by "value", "test"
                        to test the needed baseline functionality of the i2c
                        stack and your devices and "set" to simply set a given
                        value.
  value                 The difference to be applied to the monitor's
                        brightness or the value to set, if the verb "set" is
                        used.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Enables verbose mode. Disabled by default.
  -m MAXBRIGHTNESS, --max MAXBRIGHTNESS
                        Sets the maximum brightness. The default is 100.
  -b VCP                The feature number of the brightness parameter. The
                        default is 10.
  -n BUS, --bus BUS     The bus number of the display. Setting this to the
                        right value speeds up the operation of the tool
                        significantly. The default is "x", which means not
                        known.
```

# Known Problems
* The tool (rather ddcutil) is slow. That is because the transactions over i2c are slow. [The project page of ddcutil elaborates on that.](http://www.ddcutil.com/tuning/)
   ```
   I2C is an inherently unreliable protocol, requiring retry management. Furthermore, 90% of ddcutil's elapsed time is spent in timeouts mandated by the DDC specification.
   ```

# Bug Reporting
* Unless the error is related to the script or python itself, please file issues in the [ddcutil repo's issue tracker](https://github.com/rockowitz/ddcutil/issues).
* Issues with the script go into this [repo's issue tracker](https://github.com/Thermi/brightness-adjuster).
* Issues with Python itself go into [Python's issue tracker](https://bugs.python.org).