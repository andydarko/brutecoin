import base58
import ecdsa
import hashlib
import binascii
from bitcoinaddress import segwit_addr
import datetime
import multiprocessing
import pickle


P2PKH_LOCATION = "./DATASET/p2pkh.funny"
P2WPKH_LOCATION = "./DATASET/p2wpkh.funny"
P2SH_LOCATION = "./DATASET/p2sh.funny"


def gen_private_key():
    return ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)


def gen_public_key(private_key):
    return '04' + private_key.get_verifying_key().to_string().hex()


def gen_compressed_public_key(private_key):
    verifying_key = private_key.get_verifying_key()

    x_coordinate = bytes.fromhex(verifying_key.to_string().hex())[:32]
    y_coordinate = bytes.fromhex(verifying_key.to_string().hex())[32:]

    if int.from_bytes(y_coordinate, byteorder='big', signed=True) % 2 == 0:
        compressed_public_key = bytes.fromhex(f'02{x_coordinate.hex()}')
    else:
        compressed_public_key = bytes.fromhex(f'03{x_coordinate.hex()}')

    return compressed_public_key


def gen_key_hash(compressed_public_key):
    # SHA256 to the Public Key and apply RIDEMP160 to get the KeyHash.
    return hashlib.new('ripemd160', hashlib.sha256(compressed_public_key).digest()).digest()


# Legacy address (1 -> BASE58)
def gen_p2pkh_address(public_key):
    # Prepend 00 as Network Byte.
    prepend_nb = '00' + hashlib.new('ripemd160', binascii.unhexlify(
        hashlib.sha256(binascii.unhexlify(public_key)).hexdigest())).hexdigest()

    # Double SHA256.
    hash_sha56 = prepend_nb
    for x in range(1, 3):
        hash_sha56 = hashlib.sha256(binascii.unhexlify(hash_sha56)).hexdigest()

    # Get 4 bytes as Checksum;
    # Append Checksum value to the prepended Network Byte;
    # Base58 encode the result to get the Bitcoin Address.
    return base58.b58encode(binascii.unhexlify(prepend_nb + hash_sha56[:8]))


# Native SEGWITH address (bc1q -> BECH32)
def gen_v0_p2wpkh_address(compressed_public_key):
    key_hash = gen_key_hash(compressed_public_key)
    p2wpkh_address = segwit_addr.encode('bc', 0, key_hash)

    return p2wpkh_address


# Backward compatible SEGWITH address (3 -> BASE58)
def gen_p2sh_address(compressed_public_key):
    key_hash = gen_key_hash(compressed_public_key)

    # Placing the KeyHash in a P2WPKH_VO Script
    p2wpkh_v0 = bytes.fromhex(f'0014{key_hash.hex()}')

    # Hashing the P2WPKH_VO Script
    hashed_p2wpkh_v0 = hashlib.new('ripemd160', hashlib.sha256(p2wpkh_v0).digest()).digest()

    # Calculating the checksum
    checksum_full = hashlib.sha256(hashlib.sha256(bytes.fromhex(f'05{hashed_p2wpkh_v0.hex()}')).digest()).digest()
    checksum = checksum_full[:4]

    # Assembling the nested address
    binary_address = bytes.fromhex(f'05{hashed_p2wpkh_v0.hex()}{checksum.hex()}')

    # Encode nested address in base58
    p2sh_address = base58.b58encode(binary_address)

    return p2sh_address


def get_current_time():
    current_time = datetime.datetime.now()
    return "[" + str(current_time) + "]"


def check_balance(checking_address, dataset_lst):
    flag = 0

    for data in dataset_lst:
        if data == checking_address:
            flag = 1

    return flag


def byte_reader(file_location):
    file_bin = open(file_location, "rb")
    raw_data = set(pickle.load(file_bin))
    file_bin.close()
    return raw_data


def main(p2pkh_dataset, p2wpkh_dataset, p2sh_dataset):

    process_name = multiprocessing.current_process()

    print(get_current_time() + " " + str(process_name))

    i = 0

    while True:

        i += 3

        private_key = gen_private_key()

        public_key = gen_public_key(private_key)

        compressed_public_key = gen_compressed_public_key(private_key)

        p2pkh_address = gen_p2pkh_address(public_key).decode('utf8')
        p2wpkh_address = gen_v0_p2wpkh_address(compressed_public_key)
        p2sh_address = gen_p2sh_address(compressed_public_key).decode()

        addresses_list = [p2pkh_address, p2wpkh_address, p2sh_address]

        balance = 0

        for a in addresses_list:

            if a.startswith("1"):
                balance = check_balance(a, p2pkh_dataset)
            elif a.startswith("bc1q"):
                balance = check_balance(a, p2wpkh_dataset)
            elif a.startswith("3"):
                balance = check_balance(a, p2sh_dataset)

            if balance != 0:
                print(get_current_time() + " < - POSSIBLE COLLISION FOUND - >")
                print("---------------------------------------------------")
                print("Collision Address: " + a)
                print("Private Key: " + private_key.to_string().hex())
                print("---------------------------------------------------")
                with open('collisions.txt', 'a') as collisions:
                    collisions.write("Collision Address: " + a + '\n')
                    collisions.write("Private Key: " + private_key.to_string().hex() + '\n')
                    collisions.write("Public Key: " + str(public_key) + '\n')
                    collisions.write("Compressed Public Key: " + str(compressed_public_key) + '\n')

        print(get_current_time() + " "
              + private_key.to_string().hex() + " "
              + str(p2pkh_address) + " "
              + str(p2wpkh_address) + " "
              + str(p2sh_address)
              )


if __name__ == '__main__':

    print(get_current_time() + " Reading datasets!")

    dataset_p2pkh = byte_reader(P2PKH_LOCATION)
    dataset_p2wpkh = byte_reader(P2WPKH_LOCATION)
    dataset_p2sh = byte_reader(P2SH_LOCATION)

    print(get_current_time() + " Dataset loaded!")

    # for cpu in range(multiprocessing.cpu_count()):                     # -> To use all cores
    multiprocessing.Process(target=main, args=(dataset_p2pkh, dataset_p2wpkh, dataset_p2sh,)).start()
