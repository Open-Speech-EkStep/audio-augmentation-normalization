from pydub import AudioSegment
import numpy as np


class AudioAugmentation:
    def __init__(self, audio_file):
        self.audio_file = audio_file

    def volume_augmentation(self, gain):
        wav_file = AudioSegment.from_file(file=self.audio_file,
                                          format='wav')
        vol_modified_audio_file = wav_file + gain

        return vol_modified_audio_file

    def overlay_noise_on_audio(self, noise_file_path):
        wav_file = AudioSegment.from_file(file=self.audio_file,
                                          format='wav')
        noise = AudioSegment.from_file(file=noise_file_path,
                                       format='wav')
        wav_duration = wav_file.duration_seconds
        noise_duration = noise.duration_seconds
        start_time = np.random.choice(np.arange(0, int(noise_duration - wav_duration)))
        end_time = start_time + wav_duration
        clipped_noise = noise[start_time*1000: end_time*1000]
        mixed_audio = wav_file.overlay(clipped_noise)
        return mixed_audio

    def speed_change(self, speed=1.0):
        wav_file = AudioSegment.from_file(file=self.audio_file, format='wav')
        sound_with_altered_frame_rate = wav_file._spawn(wav_file.raw_data, overrides={
            "frame_rate": int(wav_file.frame_rate * speed)
        })
        return sound_with_altered_frame_rate.set_frame_rate(wav_file.frame_rate)

    def save_audio_file(self, audio, file_path):
        audio.export(out_f=file_path, format="wav")