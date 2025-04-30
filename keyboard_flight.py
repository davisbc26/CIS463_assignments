# HR: ChatGPT was used to guide the integration of MAVSDK with PX4 SITL and to develop a Python script for keyboard-controlled drone flight. Assistance included environment setup (WSL, virtualenv), MAVLink communication troubleshooting, PX4 and QGroundControl configuration, and code for velocity-based offboard control using keypresses. Script includes real-time debug feedback and a printed control legend.
# Author: Benjamin Davis


import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityNedYaw
import keyboard

VELOCITY = 2.0  # m/s

async def main():
    drone = System(mavsdk_server_address='localhost', port=50051)
    await drone.connect(system_address="udp://:14540")

    print("Connecting to drone...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected!")
            break

    print("Arming...")
    await drone.action.arm()

    print("Taking off...")
    await drone.action.takeoff()
    await asyncio.sleep(5)

    print("Starting Offboard (keyboard control)...")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 0.0))
    try:
        await drone.offboard.start()
    except OffboardError as e:
        print(f"Offboard start failed: {e._result.result}")
        await drone.action.land()
        return

    print("""
🕹️  Keyboard Drone Controls:
----------------------------------------
  W  - Move Forward (North)
  S  - Move Backward (South)
  A  - Move Left (West)
  D  - Move Right (East)
  Z  - Ascend
  X  - Descend
  Q  - Rotate Left (Yaw -)
  E  - Rotate Right (Yaw +)
  L  - Land
  Esc - Emergency Stop + Disarm
----------------------------------------
Press a key to begin flying...
""")


    try:
        while True:
            north = east = down = yaw = 0.0
            keys_pressed = []

            if keyboard.is_pressed('w'):
                north = VELOCITY
                keys_pressed.append('W')
            if keyboard.is_pressed('s'):
                north = -VELOCITY
                keys_pressed.append('S')
            if keyboard.is_pressed('a'):
                east = -VELOCITY
                keys_pressed.append('A')
            if keyboard.is_pressed('d'):
                east = VELOCITY
                keys_pressed.append('D')
            if keyboard.is_pressed('z'):
                down = -VELOCITY
                keys_pressed.append('Z')
            if keyboard.is_pressed('x'):
                down = VELOCITY
                keys_pressed.append('X')
            if keyboard.is_pressed('q'):
                yaw = -30.0
                keys_pressed.append('Q')
            if keyboard.is_pressed('e'):
                yaw = 30.0
                keys_pressed.append('E')

            if keys_pressed:
                print(f"Keys pressed: {', '.join(keys_pressed)}")

            if keyboard.is_pressed('l'):
                print("Landing...")
                await drone.offboard.stop()
                await drone.action.land()
                break

            if keyboard.is_pressed('esc'):
                print("Emergency stop!")
                await drone.offboard.stop()
                await drone.action.disarm()
                break

            await drone.offboard.set_velocity_ned(VelocityNedYaw(north, east, down, yaw))
            await asyncio.sleep(0.1)

    except Exception as e:
        print(f"Error: {e}")
        await drone.offboard.stop()
        await drone.action.land()

if __name__ == "__main__":
    asyncio.run(main())
