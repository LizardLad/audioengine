import ctypes

libwavutils_path = '/home/oliver/Development/ML/audio/build/libwavutil.so'
libwavutils = ctypes.CDLL(libwavutils_path)

def get_max_samples_in_wav_from_directory(directory: str) -> int:
    directory_c_str = ctypes.c_char_p(directory.encode())
    max_samples = libwavutils.get_max_samples_in_wav_from_directory(directory_c_str)
    return max_samples

print('Highest number of samples: {}'.format(get_max_samples_in_wav_from_directory('/home/oliver/Datasets/audioengine_single_word/clips/')))
