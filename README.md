# Description

BruteCoin is a Bitcoin collider that generates random private keys and checks if the linked wallets have any balance.

# Infos.

This project was created for fun and to experiment with cryptography, BTC addresses generation, data serialization and de-serialization, and multi processes.
The brute forcer uses a high amount of RAM because it needs to load the full dataset in memory for each process that gets created.

Maybe in the future i could experiment exploiting the <a href="https://en.wikipedia.org/wiki/Birthday_attack">Birthday Attack</a> to find partial collisions in a non random way.

# Why you should not use this to try to break into wallet addresses.

<a href="https://crypto.stackexchange.com/questions/47809/why-havent-any-sha-256-collisions-been-found-yet"> Is very unlikely to find a SHA256 collision using brute force.</a>

It takes ~0.001169 seconds to generate the three types of addresses from the same private key.
If you only need to generate addresses, you can generate up to 2566 addresses per second (per process).

It takes ~6 seconds to check if the three types of addresses have any balance.
YES, the search is slow af and could be improved BUT who cares. This is only for fun.

Using only one process and 16GB of RAM:
- You can generate up to ~81 billions addresses per year.
- You can check only up to ~15 millions addresses per year, basically nothing out of the 2^160 possible wallets.

In conclusion, if you don't have a quantum computer, it is just a big waste of time and electricity.

# Installation.

```
$ git clone https://github.com/andydarko/brutecoin.git brutecoin

$ cd brutecoin && python3 -m pip install -r requirements.txt
```

# Usage.

- Download <a href="http://addresses.loyce.club/">the updated wallet list</a> with balance (balance not shown, sorted in alphabetical order).
- Rename the downloaded file to "dataset.txt" and move it into the DATASET folder.
- Run ```$ python3 serializer.py``` to serialize the .txt data in bytes files.
- Once the dataset is splitted and serialized, run ```$ python3 bruteforcer.py```

# How It Works.

Just read the code lol.
