# -*- coding: utf-8 -*-
import PatchArrayScript
import CalcPara
import numpy as np


class PatchArray:
    def __init__(self, freq, power, phase):
        self.freq = freq
        self.power = power
        self.phase = phase
        self.hp = np.zeros(8)
        self.l, self.w, self.d, self.xf = None, None, None, None

    def size(self):
        self.l, self.w, self.hp, self.d, self.xf = CalcPara.size(self.freq)
        return self.l, self.w, self.hp, self.d, self.xf

    def call_hfss(self):
        h = PatchArrayScript.HFSS()

        h.set_variable('l', self.l)
        h.set_variable('w', self.w)
        h.set_variable('d', self.d)
        h.set_variable('xf', self.xf)
        h.set_variable('h', self.w + 9 * self.d)
        for index in range(len(self.hp)):
            h.set_variable('hp' + str(index), self.w/2.0 + (index + 1) * self.d)  # self.hp[index]

        # tail_rod
        h.override(True)
        h.create_cylinder('GND', 0, 0, 0, '55mm', '(w + 9 * d)', 'Z', 'aluminum')
        h.create_cylinder('Substrate', 0, 0, 0, '60mm', '(w + 9 * d)', 'Z', 'air')
        h.change_color('Substrate', 64, 128, 128)
        # patch_antenna
        h.create_rectangle('patch', '(-xf - l/2)', 'd', 'w', 'l', 'Y')
        h.change_color('patch', 0, 128, 0)
        h.duplicate_line('patch', 'd', 8)
        h.wrap_sheet()
        # wire
        h.create_cylinder('Feed', 0, '54.8mm', 'w/2', '0.5mm', '5.2mm', 'Y', 'copper')
        h.change_color('Feed', 255, 255, 0)
        h.duplicate_line('Feed', 'd', 9)
        h.delete('Feed')
        for index in range(len(self.hp)):
            h.subtract('Substrate', 'Feed_' + str(index + 1), True)
            h.solve_inside('Feed_' + str(index + 1))
        # GND
        h.create_box('50mm', '54.8mm', '(w + 9 * d)', 'Tool')
        h.subtract('GND', 'Tool', False)
        h.create_object_from_faces()
        h.subtract('Substrate', 'GND', False)
        # lumped port
        h.create_cycle('w/2', '1.5mm')
        h.duplicate_line('Port', 'd', 9)
        h.delete('Port')
        # _start = self.hp[0] - self.d - 0.5
        # _end = self.hp[0] - self.d - 1.5
        _start = self.w/2.0 - 0.5
        _end = self.w/2.0 - 1.5
        for index in range(len(self.hp)):
            _start = _start + self.d
            _end = _end + self.d
            h.subtract('GND_ObjectFromFace2', 'Port_' + str(index + 1), True)
            h.assign_port('Port_' + str(index + 1), _start, _end, 'lumpedPort' + str(index + 1))
        # boundaries
        h.assign_perfe('GND_ObjectFromFace1', 'GND_ObjectFromFace2')
        h.create_region('d/2')
        # setup
        h.insert_setup(self.freq)
        h.insert_sweep(self.freq - 0.15, self.freq + 0.15)
        h.insert_field_setup()
        h.edit_sources(self.power[0], self.power[1], self.power[2], self.power[3],
                       self.phase[0], self.phase[1], self.phase[2], self.phase[3])
        h.create_report()
        h.save()
        # h.run()
        h.csv('C:/Users/tee/Desktop', False)


if __name__ == '__main__':
    _freq = 2.44
    _power = [1, 1, 1, 1]
    _phase = [0, 0, 0, 0]
    _patch = PatchArray(_freq, _power, _phase)
    _patch.size()
    _patch.call_hfss()
