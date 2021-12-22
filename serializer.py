import pickle
import datetime

DATASET = "./DATASET/dataset.txt"
P2PKH_LOCATION = "./DATASET/p2pkh.funny"
P2WPKH_LOCATION = "./DATASET/p2wpkh.funny"
P2SH_LOCATION = "./DATASET/p2sh.funny"


def get_current_time():
    current_time = datetime.datetime.now()
    return "[" + str(current_time) + "]"


def line_counter(filename):
    with open(filename) as f:
        line_count = 0
        for line in f:
            line_count += 1

    f.close()

    return line_count


def write_bytes(data, file_location):
    bin_file = open(file_location, "wb")
    bin_file.write(data)
    bin_file.close()
    print(get_current_time() + " Bytes written to " + str(file_location))


def tickle_my_pickle():

    print(get_current_time() + " Reading dataset lenght...")

    dataset_size = line_counter(DATASET)

    print(get_current_time() + " The dataset has " + str(dataset_size) + " addresses.")

    file = open(DATASET, 'r')
    file.seek(0)

    dataset_p2pkh = []
    dataset_p2wpkh = []
    dataset_p2sh = []

    print(get_current_time() + " Loading dataset in memory...")

    for address in file:
        if address.startswith("1"):
            dataset_p2pkh.append(address.strip("\n"))
        elif address.startswith("3"):
            dataset_p2sh.append(address.strip("\n"))
        elif address.startswith("bc1q"):
            dataset_p2wpkh.append(address.strip("\n"))

    print(get_current_time() + " Dataset loaded!")

    p2pkh_obj = pickle.dumps(dataset_p2pkh)
    p2wpkh_obj = pickle.dumps(dataset_p2wpkh)
    p2sh_obj = pickle.dumps(dataset_p2sh)

    print(get_current_time() + " Objects created!")

    write_bytes(p2pkh_obj, P2PKH_LOCATION)
    write_bytes(p2wpkh_obj, P2WPKH_LOCATION)
    write_bytes(p2sh_obj, P2SH_LOCATION)


if __name__ == '__main__':
    tickle_my_pickle()
