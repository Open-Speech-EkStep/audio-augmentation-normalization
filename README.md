## Data Augmentation and Normalization 

Pipeline to augment data and perform loudness normalization. 

Data can be augmented in the following ways: 
* Volume augmentation
* Speed perturbation 
* Adding background noise

Parameters can be specified in the src/config.yaml file. It has two basic blocks, namely data and operations. In the data block input and output paths are to be specified along with some additional parameters for some kind of operations. In operations block the type of augmentation or normalization has to be specified. The utility takes a single folder containing audios as input and creates a new folder with augmented or normalized audio at audio_dump_path. 

```
data: 
    audio_path: <path to folder containing audio>
    audio_dump_path: <path for saving augmented or normalized data>
    background_noise_path: <folder containing background noise to be added>
    background_noises: <list of background noise file names>
    noise_probabilities: <list of probabilities in which noise is to be added>
operations: 
    volume: <True or False>
    volume_gain: <list of volume gaines to be applied>
    loudness_normalization: <True or False>
    add_background_noise: <True or False>
    speed_perturb: <True or False>
    speed: <factor to scale speed of audio>
```

After specifying parameters in the config.yaml file the pipeline can be triggered by python src/pipeline.py