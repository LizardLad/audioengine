import tensorflow as tf

def get_num_gpus() -> int:
    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    return len(physical_devices)

def set_gpu_memory_limit(physical_gpu_device, limit: int=4096):
    try:
        tf.config.experimental.set_virtual_device_configuration(physical_gpu_device, [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=4096)])
    except Exception as exception:
        #Virtual devices must be set before GPUs have been initialized
        print(exception)

def set_gpu_list_memory_limit(physical_devices: list, limit: int=4096):
    for physical_device in physical_devices:
        set_gpu_memory_limit(physical_device, limit=limit)