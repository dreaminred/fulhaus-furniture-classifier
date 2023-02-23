import sys
import os
from glob import glob
from sklearn.model_selection import train_test_split
from skimage import io

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

        os.makedirs(directory+"/train")
        os.makedirs(directory+"/train/Bed")
        os.makedirs(directory+"/train/Chair")
        os.makedirs(directory+"/train/Sofa")

        os.makedirs(directory+"/test")
        os.makedirs(directory+"/test/Bed")
        os.makedirs(directory+"/test/Chair")
        os.makedirs(directory+"/test/Sofa")

        os.makedirs(directory+"/validate")
        os.makedirs(directory+"/validate/Bed")
        os.makedirs(directory+"/validate/Chair")
        os.makedirs(directory+"/validate/Sofa")


def rearrange_data(bed_filenames, chair_filenames, sofa_filenames, output_dir):
    labels_bed = ["bed"] * 100
    X_training_set_bed, X_testing_set_bed_, y_training_bed, y_testing_bed_ = train_test_split(bed_filenames,
                                                                                              labels_bed,
                                                                                              test_size=0.3,
                                                                                              random_state=42)
    X_testing_set_bed, X_validation_set_bed, y_testing_bed, y_validation_bed = train_test_split(X_testing_set_bed_,
                                                                                                y_testing_bed_,
                                                                                                test_size=0.3,
                                                                                                random_state=42)
    training_dir = output_dir + "/train/Bed\\"

    for filename in X_training_set_bed:
        nameIndex = filename.rfind('\\') # used for saving file names
        im_name = filename[nameIndex+1:]
        save_path = training_dir + im_name
        im = io.imread(filename)
        io.imsave(save_path,im)

    testing_dir = output_dir + "/test/Bed\\"

    for filename in X_testing_set_bed:
        nameIndex = filename.rfind('\\') # used for saving file names
        im_name = filename[nameIndex+1:]
        save_path = testing_dir + im_name
        im = io.imread(filename)
        io.imsave(save_path,im)

    validation_dir = output_dir + "/validate/Bed\\"

    for filename in X_validation_set_bed:
        nameIndex = filename.rfind('\\') # used for saving file names
        im_name = filename[nameIndex+1:]
        save_path = validation_dir + im_name
        im = io.imread(filename)
        io.imsave(save_path,im)

    labels_chair = ["chair"] * 100
    X_training_set_chair, X_testing_set_chair_, y_training_chair, y_testing_chair_ = train_test_split(chair_filenames,
                                                                                                      labels_chair,
                                                                                                      test_size=0.3,
                                                                                                      random_state=42)
    X_testing_set_chair, X_validation_set_chair, y_testing_chair, y_validation_chair = train_test_split(X_testing_set_chair_,
                                                                                                        y_testing_chair_,
                                                                                                        test_size=0.3,
                                                                                                        random_state=42)
    training_dir = output_dir + "/train/Chair\\"

    for filename in X_training_set_chair:
        nameIndex = filename.rfind('\\') # used for saving file names
        im_name = filename[nameIndex+1:]
        save_path = training_dir + im_name
        im = io.imread(filename)
        io.imsave(save_path,im)

    testing_dir = output_dir + "/test/Chair\\"

    for filename in X_testing_set_chair:
        nameIndex = filename.rfind('\\') # used for saving file names
        im_name = filename[nameIndex+1:]
        save_path = testing_dir + im_name
        im = io.imread(filename)
        io.imsave(save_path,im)

    validation_dir = output_dir + "/validate/Chair\\"

    for filename in X_validation_set_chair:
        nameIndex = filename.rfind('\\') # used for saving file names
        im_name = filename[nameIndex+1:]
        save_path = validation_dir + im_name
        im = io.imread(filename)
        io.imsave(save_path,im)


    labels_sofa = ["sofa"] * 100
    X_training_set_sofa, X_testing_set_sofa_, y_training_bed, y_testing_bed_ = train_test_split(sofa_filenames,
                                                                                                labels_sofa,
                                                                                                test_size=0.3,
                                                                                                random_state=42)
    X_testing_set_sofa, X_validation_set_sofa, y_testing_sofa, y_validation_sofa = train_test_split(X_testing_set_sofa_,
                                                                                                    y_testing_bed_,
                                                                                                    test_size=0.3,
                                                                                                    random_state=42)

    training_dir = output_dir + "/train/Sofa\\"

    for filename in X_training_set_sofa:
        nameIndex = filename.rfind('\\') # used for saving file names
        im_name = filename[nameIndex+1:]
        save_path = training_dir + im_name
        im = io.imread(filename)
        io.imsave(save_path,im)

    testing_dir = output_dir + "/test/Sofa\\"

    for filename in X_testing_set_sofa:
        nameIndex = filename.rfind('\\') # used for saving file names
        im_name = filename[nameIndex+1:]
        save_path = testing_dir + im_name
        im = io.imread(filename)
        io.imsave(save_path,im)

    validation_dir = output_dir + "/validate/Sofa\\"

    for filename in X_validation_set_sofa:
        nameIndex = filename.rfind('\\') # used for saving file names
        im_name = filename[nameIndex+1:]
        save_path = validation_dir + im_name
        im = io.imread(filename)
        io.imsave(save_path,im)


def main(input_dir, output_dir):
    bed_dir = glob(input_dir + "/Bed/*.jpg")
    chair_dir = glob(input_dir + "/Chair/*.jpg")
    sofa_dir = glob(input_dir + "/Sofa/*.jpg")

    create_directory(output_dir)

    rearrange_data(bed_dir, chair_dir, sofa_dir, output_dir)

if __name__ == '__main__':
    input = sys.argv[1]
    output = sys.argv[2]
    main(input, output)