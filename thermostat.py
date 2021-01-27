# -*- coding: utf-8 -*-

import serial
import time

class Thermostat:
  setTemp = 170
  delta = 5
  fake = False
  arduino = None
  # fake parameters:
  T = 20
  heater = False
  heaterV = 0
  fan = False
  fanV = 0
  
  def init_serial(self, port):
    print("Init...")
    try:
      self.arduino = serial.Serial(port, 9600, timeout=1)
      time.sleep(1)
      print("... done!")
      return 0
    except:
      print("... failed!")
      return -1

  def read_temperature(self):
    if self.fake == True:
      if self.heater == True:
        self.heaterV = min(1, self.heaterV + 0.02)
      else:
        self.heaterV = max(0, self.heaterV - 0.02)
      if self.fan == True:
        self.fanV = min(1, self.fanV + 0.05)
      else:
        self.fanV = max(0, self.fanV - 0.05)
      self.T += self.heaterV*(550 - self.T)/500
      self.T += self.fanV*(20 - self.T)/200
      self.T += (20 - self.T)/1000
      return self.T
    else:
      self.arduino.write(b'T=?\r\n')
      buf = self.arduino.read_until(b'\n')
      try:
        temp = 21.0 + 0.4*float(buf)
      except:
        print("Value error:", buf)
        return -1
      return temp
    return -1
  
  def set_heater(self, state):
    if state == True:
      self.arduino.write(b'H=1\r\n')
    else:
      self.arduino.write(b'H=0\r\n')
    self.heater = state
  
  def set_fan(self, state):
    if state == True:
      self.arduino.write(b'F=1\r\n')
    else:
      self.arduino.write(b'F=0\r\n')
    self.fan = state
  
  def set_temp(self, temp):
    self.setTemp = temp
  
  def loop(self, temps=None):
    temp = self.read_temperature()
    if temp == -1:
      return
    if temps != None:
      temps.append(temp)
    if temp > self.setTemp + 10*self.delta:
      self.set_fan(True)
    if temp < self.setTemp + self.delta:
      self.set_fan(False)
    if temp > self.setTemp + self.delta:
      self.set_heater(False)
    if temp < self.setTemp - self.delta:
      self.set_heater(True)

