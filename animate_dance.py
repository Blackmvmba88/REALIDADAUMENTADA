import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection

print("Iniciando el script de la Danza Reactiva (Versión Optimizada)...")

try:
    # --- 1. Cargar y Analizar el Sonido ---
    audio_path = librosa.example('brahms', hq=True)
    y, sr = librosa.load(audio_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    print("Audio cargado y analizado.")

    # --- OPTIMIZACIÓN: Reducir duración, FPS y resolución de datos ---
    duration = 4.0  # Reducido de 10s
    downsample_factor = 10
    fps = 20  # Reducido de 30 FPS

    # Recortar y diezmar el audio
    y_clip = y[:int(duration * sr)]
    y_downsampled = y_clip[::downsample_factor]
    beat_times_clip = beat_times[beat_times < duration]
    time_downsampled = np.linspace(0, duration, len(y_downsampled))
    print(f"Audio optimizado: {duration}s, {fps} FPS, diezmado por {downsample_factor}x.")

    # --- 2. Configuración de la Animación ---
    fig, ax = plt.subplots(figsize=(12, 4)) # Ligeramente más pequeño

    points = np.array([time_downsampled, y_downsampled]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    norm = plt.Normalize(0, 2 * np.pi)
    lc = LineCollection(segments, cmap='hsv', norm=norm)
    lc.set_array(np.linspace(0, 2 * np.pi, len(time_downsampled)))
    line = ax.add_collection(lc)

    ax.set_xlim(0, duration)
    ax.set_ylim(-0.8, 0.8)
    ax.set_title("Danza Reactiva")
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Amplitud")
    ax.grid(True, linestyle='--', alpha=0.6)

    # --- 3. Lógica de Animación y Reactividad ---
    glow_state = {'value': 0.0, 'decay': 0.85}

    def update(frame):
        current_time = frame / fps

        if any(np.isclose(current_time, beat_time, atol=1/fps) for beat_time in beat_times_clip):
            glow_state['value'] = 1.0

        current_glow = glow_state['value']
        line.set_linewidth(2 + current_glow * 4)
        glow_state['value'] *= glow_state['decay']

        new_colors = np.linspace(current_time, 2 * np.pi + current_time, len(time_downsampled))
        lc.set_array(new_colors % (2 * np.pi))

        return line,

    # --- 4. Crear y Guardar la Animación ---
    num_frames = int(duration * fps)
    print(f"Creando animación con {num_frames} fotogramas a {fps} FPS...")

    anim = FuncAnimation(fig, update, frames=num_frames, blit=True, interval=1000/fps)

    output_filename = "audio_dance.gif"
    print(f"Guardando animación como '{output_filename}'. Esto puede tardar un momento...")
    anim.save(output_filename, writer='pillow', fps=fps)

    print("¡Animación guardada con éxito!")

except Exception as e:
    print(f"\nOcurrió un error: {e}")
    import traceback
    traceback.print_exc()
