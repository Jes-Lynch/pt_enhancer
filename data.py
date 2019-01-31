from dataset import DatasetFromFolder
from os.path import join
from torchvision.transforms import Compose, CenterCrop, ToTensor, Resize


def calculate_valid_crop_size(crop_size, upscale_factor):
    return crop_size - (crop_size % upscale_factor)


#For all of these transformations, we are currently assuming an upscale factor of 8 (256 -> 2048)
#Input final size: 128
def input_transform(crop_size, upscale_factor):
    return Compose([
        Resize((int(1024/upscale_factor), int(1024/upscale_factor)), interpolation=3),
        CenterCrop(crop_size/upscale_factor),
        ToTensor(),
    ])


#Intermediate 1 final size: 256
def int1_transform(crop_size, upscale_factor):
    return Compose([
        Resize((int(1024/(upscale_factor/2)), int(1024/(upscale_factor/2))), interpolation=3),
        CenterCrop(crop_size/(upscale_factor/2)),
        ToTensor(),
    ])


#Intermediate 2 final size: 512
def int2_transform(crop_size, upscale_factor):
    return Compose([
        Resize((int(1024/(upscale_factor/4)), int(1024/(upscale_factor/4))), interpolation=3),
        CenterCrop(crop_size/(upscale_factor/4)),
        ToTensor(),
    ])


#Target final size: 1024
def target_transform(crop_size, upscale_factor):
    return Compose([
        Resize((1024, 1024), interpolation=3),
        CenterCrop(crop_size),
        ToTensor(),
    ])


def get_training_set(upscale_factor):
    root_dir = join("dataset", "kidney/images")
    highres_dir = join(root_dir, "highres")
    int2_dir = join(root_dir, "int2")
    int1_dir = join(root_dir, "int1")
    lowres_dir = join(root_dir, "lowres")
    crop_size = calculate_valid_crop_size(1024, upscale_factor)

    return DatasetFromFolder(lowres_dir, int1_dir, int2_dir, highres_dir,
                             input_transform=input_transform(crop_size, upscale_factor),
                             int1_transform=int1_transform(crop_size, upscale_factor),
                             int2_transform=int2_transform(crop_size, upscale_factor),
                             target_transform=target_transform(crop_size, upscale_factor))


def get_test_set(upscale_factor):
    root_dir = join("dataset", "kidney/images")
    highres_dir = join(root_dir, "highres")
    int2_dir = join(root_dir, "int2")
    int1_dir = join(root_dir, "int1")
    lowres_dir = join(root_dir, "lowres")
    crop_size = calculate_valid_crop_size(1024, upscale_factor)

    return DatasetFromFolder(lowres_dir, int1_dir, int2_dir, highres_dir,
                             input_transform=input_transform(crop_size, upscale_factor),
                             int1_transform=int1_transform(crop_size, upscale_factor),
                             int2_transform=int2_transform(crop_size, upscale_factor),
                             target_transform=target_transform(crop_size, upscale_factor))
