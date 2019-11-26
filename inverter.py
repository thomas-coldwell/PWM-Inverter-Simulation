import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack

def main():

    sampling_frequency = 100000
    time_period = 1
    vd = 300
    ma = 0.8
    mf = 39
    tri_wave_peak = vd/2
    control_wave_frequency = 1
    tri_wave_frequency = mf*control_wave_frequency
    control_wave_peak = tri_wave_peak*ma

    t = []
    tri_wave = []
    control_wave = []
    pwm_wave = []

    min_freq_diff = 1000
    fundemental_freq_index = 0

    # Create a time series
    for time_step in range(sampling_frequency*time_period):
        # Record each time sample
        time = time_step/sampling_frequency
        t.append(time)
        # Generate the triangular waveform
        tri_wave_time_period = 1 / tri_wave_frequency
        tri_wave_t = (time / tri_wave_time_period) - int(time / tri_wave_time_period)
        if tri_wave_t < 0.25:
            tri_wave_p = tri_wave_t / 0.25
            tri_wave_v = -tri_wave_peak*tri_wave_p
        elif tri_wave_t < 0.75:
            tri_wave_p = (tri_wave_t-0.25) / 0.5
            tri_wave_v = -tri_wave_peak + (2*tri_wave_peak*tri_wave_p)
        else:
            tri_wave_p = (tri_wave_t-0.75) / 0.25
            tri_wave_v = tri_wave_peak + (-tri_wave_peak*tri_wave_p)
        tri_wave.append(tri_wave_v)
        # Generate the control wave
        control_wave_v = control_wave_peak*(np.sin(2*np.pi*control_wave_frequency*time))
        control_wave.append(control_wave_v)
        # Compare the triangular and control wave to generate the PWM
        if tri_wave_v > control_wave_v:
            pwm_wave_v = -tri_wave_peak
        else:
            pwm_wave_v = tri_wave_peak
        pwm_wave.append(pwm_wave_v)

    # Plot the graphs of each
    # fig, axs = plt.subplots(3, 1)
    # axs[0].plot(t, tri_wave)
    # axs[1].plot(t, control_wave)
    # axs[2].plot(t, pwm_wave)
    fft_y = scipy.fftpack.rfft(pwm_wave)
    fft_x = scipy.fftpack.rfftfreq(len(t), t[1] - t[0])
    # Find the frequency sample index closest to the fundemental frequency
    # for i in range(len(fft_x)):
    #     # fftfreq = fft_x[i]
    #     print(fft_x[i])
    fft_y_v = (1/np.sqrt(2)) * tri_wave_peak * ma * (np.abs(fft_y) / (np.abs(fft_y)[control_wave_frequency*2*time_period]))
    if tri_wave_frequency > 200:
        plt.plot(fft_x / 1000, fft_y_v)
        plt.xlabel('Frequency (kHz)')
        plt.xlim(-0.1, 9.9)
        plt.xticks(np.arange(-0.5, 9.5, 1.0))
    else:
        plt.plot(fft_x, fft_y_v)
        plt.xlabel('Frequency (Hz)')
        plt.xlim(-10, 190)
        plt.xticks(np.arange(-10, 190, 10))
    plt.ylabel('Voltage (V)')
    voltage_lim = int(np.round(np.max(fft_y_v) / 100, decimals=1)*100)
    plt.ylim(0, voltage_lim)
    plt.yticks(np.arange(0, voltage_lim, 5))
    plt.grid()
    plt.show()
        

main()