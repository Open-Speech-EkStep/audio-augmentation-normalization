import yaml
import glob
import os
from audio_augmentation import AudioAugmentation
from audio_normalization import AudioNormalization
from tqdm import tqdm


class Pipeline:
    def __init__(self, yaml_file):
        self.yaml_file = yaml_file

    def read_yaml(self):
        with open(self.yaml_file) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data

    def rectify_audio_path(self, path):
        if path[-1]=="/":
            path = path[:-1]
        return path

    def modified_volume_folder_name(self, audio_input_path, audio_dump_path, gain):
        if gain > 0:
            output_folder_name = (audio_dump_path + '/' +
                                  audio_input_path.split('/')[-1] +
                                  '_vol_up_' + str(gain))
            return output_folder_name
        else:
            output_folder_name = (audio_dump_path + '/' +
                                  audio_input_path.split('/')[-1] +
                                  '_vol_down_' + str(gain * -1))
            return output_folder_name

    def modify_volume(self, input_audio_path, gain, output_folder_path):
        audio_files = glob.glob(input_audio_path + '/*.wav')
        for audio in audio_files:
            modified_audio = AudioAugmentation(audio).volume_augmentation(gain)
            output_file_name = (output_folder_path + '/' +
                                audio.split('/')[-1])
            modified_audio.export(output_file_name, format='wav')

    def normalize_loudness(self, input_audio_path, audio_dump_path):
        audio_files = glob.glob(input_audio_path + '/*.wav')
        output_folder_path = audio_dump_path + '/' + input_audio_path.split('/')[-1] + '_loud_norm'
        if os.path.isdir(output_folder_path):
            print('Folder %s exists' % output_folder_path)
            exit()
        os.makedirs(output_folder_path)
        for audio in audio_files:
            normalized_audio = AudioNormalization(audio).loudness_normalization()
            output_file_name = (output_folder_path + '/' +
                                audio.split('/')[-1])
            normalized_audio.export(output_file_name, format='wav')

    def volume_augmentation(self, audio_dump_path, config_parameters, input_audio_path):
        volume_gains = config_parameters['operations']['volume_gain']
        for gain in tqdm(volume_gains):
            output_folder_name = self.modified_volume_folder_name(input_audio_path, audio_dump_path, gain)
            if os.path.isdir(output_folder_name):
                print('Folder %s exists' % output_folder_name)
                continue
            os.makedirs(output_folder_name)
            self.modify_volume(input_audio_path, gain, output_folder_name)

    def check_background_noise_audios(self, config_parameters):
        noise_path = config_parameters['data']['background_noise_path']
        probabilities = config_parameters['data']['noise_probabilities']
        noise_path = self.rectify_audio_path(noise_path)
        if not os.path.isdir(noise_path):
            print("Error: Incorrect path for background noises. Folder does not exist")
            exit()
        noise_files = glob.glob(noise_path + '/*.wav')
        noise_files = [f.split('/')[-1] for f in noise_files]
        config_noise = config_parameters['data']['background_noises']
        flag = 0
        if (set(config_noise) & set(noise_files)) == set(config_noise):
            flag = 1
        if flag:
            print('Noise audios found in specified path')
        if flag == 0:
            print('Error: Noise not found in specified path')
            exit()
        if sum(probabilities) < 0.9:
            print("Error: Sum of noise weights should be close to 1 ")
            exit()

    def pipeline(self):
        config_parameters = self.read_yaml()
        input_audio_path = config_parameters['data']['audio_path']
        audio_dump_path = config_parameters['data']['audio_dump_path']
        input_audio_path = self.rectify_audio_path(input_audio_path)
        audio_dump_path = self.rectify_audio_path(audio_dump_path)

        if config_parameters['operations']['volume']:
            print("Augmenting Volume")
            self.volume_augmentation(audio_dump_path, config_parameters, input_audio_path)

        if config_parameters['operations']['loudness_normalization']:
            print("Normalizing volume")
            audio_path = config_parameters['data']['path_for_loudness_normalization']
            self.normalize_loudness(audio_path, audio_dump_path)

        if config_parameters['operations']['add_background_noise']:
            self.check_background_noise_audios(config_parameters)
            print('Adding Noise')



if __name__ == "__main__":
    Pipeline('config.yaml').pipeline()
