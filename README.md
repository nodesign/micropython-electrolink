# Micropython-electrolink

This is implementation of [Electrolink protocol](https://github.com/projectiota/electrolink) in Micropython.

`Electrolink` is technology that permits to control and program connected things over the Internet (more precisely via JsonRPC-over-MQTT). Every board or microcontroler that can run Micropython can be easily controlled over the network using Electrolink.
This technology has been initialy conceived and developped for [WeIO](https://github.com/nodesign/weio) project in 2013 by [Uros Petrevski](https://github.com/ukicar) & [Drasko Draskovic](https://github.com/drasko). Seeing great benefits from having possibility to interact in real-time with things in the network, team decided to extract project from WeIO and create separate one. Team was joined by [Paul Rathgeb](https://github.com/ks156) who was equaly participating in design and specification, architecture and RIOT RTOS Electrolink implementation.

This protocol using module `electroGpio` implements the most common interfaces to control GPIO, I2C, SPI, etc. over the network but it gives also a great simplicity for writing custom commands (see `modules`). This implementation targets specificaly ESP8266 but will enlarge it's support over time.

`MicropythonServer` is implementation of pure Electrolink.

`ElectroConsole` is interactive tool dedicated to interact with Electrolink directly from console. 

`Modules` are extensions of some specific functions that can be used with Eectrolink

`MqttBroker` is simple Mqtt server broker easy to use

## Installation

## Electrolink server
Install micropyton on your ESP8266 board. This steps will not be discussed here. However this is a good place to start: https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html

You need Mqtt broker launched somewhere so you can connect your computer and your board on to. You can try mqttBroker from the project or use another one that you are used to.

Before transfering files to the board change `micropythonServer/config.json` to match the ip address of your Mqtt broker. Then copy files to the board

```bash
ampy -p /dev/tty.SLAB_USBtoUART put config.json
ampy -p /dev/tty.SLAB_USBtoUART put electrolink.py
ampy -p /dev/tty.SLAB_USBtoUART put electroGPIO.py
ampy -p /dev/tty.SLAB_USBtoUART put main.py
```
When you restart your ESP board main program will start and if everything goes fine will be connected to the Mqtt broker

## ElectroConsole
Before starting interactive console change `electroConsole/config.toml` file to match ip address of your Mqtt broker.
Then

```bash
python electroConsole.py
```

If everything goes fine you will get electrolink prompt. Electrolink console will try to ping your board. If ping is OK then it will ask what functions will be available to you. That means that once you get command prompt you can use tab, auto completition and edition like in any other console tool.

```bash
electrolink > getSpells()
electrolink >
weioESP/reply
{
    "deleteFile": {
        "description": "Delete specified file", 
        "parameters": "path"
    }, 
    "getFile": {
        "description": "Get file data", 
        "parameters": "path"
    }, 
    "getFileList": {
        "description": "Get file list in directory", 
        "parameters": "path"
    }, 
    "getInfo": {
        "description": "Get board info", 
        "parameters": null
    }, 
    "getSpells": {
        "description": "Get available instructions to call", 
        "parameters": null
    }, 
    "ping": {
        "description": "Verify if board responds, will respond 1", 
        "parameters": null
    }, 
    "reset": {
        "description": "Hardware reset electronics", 
        "parameters": null
    }, 
    "writeFile": {
        "description": "Write data in file", 
        "parameters": "path, data"
    }
}
electrolink > ping()
electrolink > 
weioESP/reply
weioESP is alive!
electrolink > ping()
electrolink > digitalWrite(14,1)
electrolink > writeFile("some.txt", "file:some.txt")
```
## License 
[Apache-2.0](LICENSE)
