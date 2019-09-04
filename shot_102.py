import serial
from time import sleep

class shot_102:
    def __init__(self, comport_name, pulse_per_unit=(1000, 1000), write_waittime=0.1):
        # pulse_per_unitの値
        # リニアステージ(SGSP20-85) : 1000 パルス/mm　もしくは 1 パルス/μm

        self._pulse_per_unit = pulse_per_unit
        self._ser = serial.Serial(comport_name)
        self._ser.baudrate = 9600
        self._write_waittime = write_waittime

    def clear_buf(self):
        self._ser.write("\r\n".encode())
        sleep(self._write_waittime)
        self._ser.read_all()

    def read_retval(self):
        sleep(self._write_waittime)
        read_val = self._ser.read_all().decode().splitlines()[0]
        return read_val

    def is_busy(self):

        self.clear_buf()
        self._ser.write(b"!:\r\n")
        status = self.read_retval()

        if status is "B":
            return True
        else:
            return False

    def hold_motor(self, axis):
        self.clear_buf()
        sending_command = "C:{}1\r\n".format(axis).encode()
        self._ser.write(sending_command)
        status = self.read_retval()
        return status

    def release_motor(self, axis):
        self.clear_buf()
        sending_command = "C:{}0\r\n".format(axis).encode()
        self._ser.write(sending_command)
        status = self.read_retval()
        return status

    def go_mechanical_origin(self, axis, direction):
        """
        機械原点復帰
        :param axis: 軸番号（1, 2)
        :param direction: 軸方向（'+' or '-')
        :return: status
        """
        self.clear_buf()
        sending_command = "H:{}{}\r\n".format(axis, direction).encode()
        self._ser.write(sending_command)
        status = self.read_retval()

        while self.is_busy():
            sleep(0.1)
        return status

    def set_current_position_as_origin(self, axis):
        self.clear_buf()
        sending_command = "R:{}\r\n".format(axis).encode()
        self._ser.write(sending_command)
        status = self.read_retval()

        while self.is_busy():
            sleep(0.1)
        return status

    def set_cmd_relative_move_pulse(self, axis, n_pulse):
        self.clear_buf()
        if n_pulse > 0:
            direction = "+"
        else:
            direction = "-"
        sending_command = "M:{}{}P{}\r\n".format(axis, direction, abs(n_pulse)).encode()
        self._ser.write(sending_command)
        status = self.read_retval()
        return status

    def set_cmd_absolute_move_pulse(self, axis, n_pulse):
        self.clear_buf()
        if n_pulse > 0:
            direction = "+"
        else:
            direction = "-"
        sending_command = "A:{}{}P{}\r\n".format(axis, direction, abs(n_pulse)).encode()
        self._ser.write(sending_command)
        status = self.read_retval()
        return status

    def unit_to_pulse(self, axis, unit_val):
        return int(unit_val * self._pulse_per_unit[axis-1])

    def set_cmd_relative_move_unit(self, axis, unit_val):
        n_pulse = self.unit_to_pulse(axis, unit_val)
        status = self.set_cmd_relative_move_pulse(axis, n_pulse)
        return status

    def set_cmd_absolute_move_unit(self, axis, unit_val):
        n_pulse = self.unit_to_pulse(axis, unit_val)
        status = self.set_cmd_absolute_move_pulse(axis, n_pulse)
        return status

    def start_move(self):
        self.clear_buf()
        sending_command = "G:\r\n".encode()
        self._ser.write(sending_command)
        status = self.read_retval()

        while self.is_busy():
            sleep(0.1)
        return status

    def close_com(self):
        self._ser.close()