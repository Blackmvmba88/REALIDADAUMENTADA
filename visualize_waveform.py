import librosa
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Cargar el Sonido ---
audio_path = librosa.example('brahms', hq=True)
print(f"Loading audio file from: {audio_path}")

try:
    y, sr = librosa.load(audio_path)
    print("\nAudio file loaded successfully!")
    print(f"Shape: {y.shape}, Sample Rate: {sr} Hz")

    # --- 2. Encontrar el Pulso ---
    print("\nFinding the heartbeat of the song...")
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    # FIX for DeprecationWarning: Use .item() to extract the scalar value from a 0-dim array
    tempo_scalar = tempo.item()

    print(f"Heartbeat found!")
    print(f"Estimated Tempo: {tempo_scalar:.2f} BPM")

    # Convert beat frames to time in seconds
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # --- 3. Visualizar con Pulso ---
    print("\nGenerating waveform plot with beats...")

    time = np.arange(0, len(y)) / sr

    plt.figure(figsize=(15, 5))
    plt.plot(time, y, label='Forma de Onda', alpha=0.75)

    # Add vertical lines for each detected beat
    plt.vlines(beat_times, -1, 1, color='r', linestyle='--', label=f'Pulso ({tempo_scalar:.2f} BPM)')

    plt.title("El Corazón de la Canción: Forma de Onda y Pulso")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()

    output_filename = "waveform_with_beats.png"
    plt.savefig(output_filename)

    print(f"Waveform plot with beats saved as '{output_filename}'")

except Exception as e:
    print(f"\nAn error occurred: {e}")
