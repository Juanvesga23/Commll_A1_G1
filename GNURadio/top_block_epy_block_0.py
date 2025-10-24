import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    """
    Up-Converter en GNU Radio con salida real
    """

    def __init__(self, fc=100e3, samp_rate=1e6):
        gr.sync_block.__init__(
            self,
            name="up_converter_real",
            in_sig=[np.complex64],  # entrada compleja
            out_sig=[np.float32]    # salida real
        )
        self.fc = fc
        self.samp_rate = samp_rate
        self.phase = 0
        self.dt = 2 * np.pi * self.fc / self.samp_rate

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        # Generar portadora compleja
        n = np.arange(len(in0))
        carrier = np.exp(1j * (self.phase + self.dt * n))

        # Mezclar señal de entrada con portadora y tomar solo la parte real
        out[:] = np.real(in0 * carrier)

        # Actualizar fase para continuidad
        self.phase += self.dt * len(in0)
        self.phase = np.mod(self.phase, 2*np.pi)

        return len(out)

