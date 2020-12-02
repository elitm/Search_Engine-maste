import csv
import pickle


def save_obj(obj, name):
    """
    This function save an object as a pickle.
    :param obj: object to save
    :param name: name of the pickle file.
    :return: -
    """
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    """
    This function will load a pickle file
    :param name: name of the pickle file
    :return: loaded pickle file
    """
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def load_inverted_index():
    with open('inverted_idx.pkl', 'rb') as f:
        return pickle.load(f)


def print_to_csv(csv_path, data):
    file = open(csv_path, 'w', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerows(data)
    file.close()
