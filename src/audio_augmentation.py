from pydub import AudioSegment


class AudioAugmentation:
    def __init__(self, audio_file):
        self.audio_file = audio_file

    def volume_augmentation(self, gain):
        wav_file = AudioSegment.from_file(file=self.audio_file,
                                          format='wav')
        vol_modified_audio_file = wav_file + gain

        return vol_modified_audio_file

    def save_audio_file(self, audio, file_path):
        audio.export(out_f=file_path,
                     format="wav")