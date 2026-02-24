
Lamp Smartener
===============

This is the "Lamp Smartener" or "Overengineered Light Switch" it works on
USB powered LED lights.

WIP

Component selection
-------------------

 * the NE7000 can be substituted for any N-type with a Vth around 1-2 V. and
   can switch 5V,
 * The AO3400 can be substituted for any N-type that can handle 600mA of
   current, and switch 5V.  And disipate 1.25W of heat.
 * Likewise AO3401 can be substituted for any P-type that can handle 600mA of
   current and switch 5V.
 * TODO resistor tollerance
 * TODO current limiter advice.


Assembly notes
--------------

Solder the small SMD components first, it's easier to reach them before you
put the big ones in.

Solder the switches before mounting the USB ports, the usb port shield pin
will interfere with switch soldering.

Do not confuse the mosfet types.  They're different for good reasons.
p-type and n-type just arnt' compatible.  However, the NE7000 can be
substituted with more AO3400 units (probably), but not the other way around.

TODO: Add alterantive 2 and 1 port versions with the current limiter.

Mount the uC with either pin headers or directly.  for direct soldering try
holding it in place with pins/wires in the through-holes then solder the
edges.


Firmware
--------

Firmware uses the esphome framework and can be compiled with:

   $ mkdir /tmp/esphome
   $ docker run --rm --privileged -v "${PWD}":/config -v "/tmp/esphome:/config/.esphome" --device=/dev/ttyACM0 -it ghcr.io/esphome/esphome run lamp-smartener.yaml

Assuming you have pluged the ESP32 module into your PC and it is connected
at /dev/ttyACM0

Alternatlvely you can build and flash it in separete steps, this will erase
any wifi credentials that may be on the device, the above method does not:

   $ mkdir /tmp/esphome
   $ docker run --rm --privileged -v "${PWD}":/config -v "/tmp/esphome:/config/.esphome" -it ghcr.io/esphome/esphome compile lamp-smartener.yaml
   $ cp /tmp/esphome/build/lamp-smartener/.pioenvs/lamp-smartener/firmware.factory.bin .
   $ esptool.py write_flash 0x0 firmware.factory.bin

The device will reboot and create a new Wifi network with "Lamp Smartener"
in its name.  The password is "Overengineered Light Switch".  Connect to it
with something like your phone then visit http://192.168.4.1  Tell the page
there what wifi network you'd like it to join.

Home assistant will be able to discover it, if you use (or would like to
use) esphome's dashboard to maintain firmware updates (which is available as
a HA addon) you can adopt the device there as well.


Using the device
----------------

Each button will twoggle it's lamp (if installed) or drive automations in
Home Assistant.  In the single lamp version by default the 2nd button does
nothing directly, but it can be used to run automations in home assistant.

Pressing and holding both buttons together for 10 seconds will initiate a
factory reset, the status light will glow orange and any lamps will flash,
keep holding the buttons for another 5s to conform the factory reset,
otherwise release buttons to cancel.

Each button can be "disconnected" from its light by turning the "direct"
control switch off for that switch and lamp.  Eg if the button should run a
home assistant automation instead (which may turn on the lamp to 50%
brightness if you touch the button after midnight, and full brightness
otherwise).  The "direct" setting will persisted across reboots.

