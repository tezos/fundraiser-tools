# Command-line tools (forked from [`fundraiser-tools`](https://github.com/tezos/fundraiser-tools) by [DLS](https://github.com/tezos))

This repository contains **Command-line tools** to support the [whitelisting procedure](https://tzlibre.github.io/whitelist.html) for the [TzLibre](https://tzlibre.github.io) split.

**Command-line tools** support you in:

1. generating two digital signatures (namely `ETH_addrSignature` and `declarationSignature`) to prove the ownership of a DLS-Tezos private key and therefore to be entitled to split them into TzLibre Tezzies;
2. serializing those signatures in a single `tx-data` field to be issued as an Ethereum transaction according to the instructions given on the [TzLibre website](https://tzlibre.github.io/whitelist.html#send-tx).

Furthermore a sendboxed execution environment is provided as a Docker container, along with a convenient invocation bash script to improve usability and security (by avoiding to store private data on command line history).

> **PLASE BE FULL RESPONSIBLE ON THE CODE YOU RUN: READ THE WHOLE CODEBASE BEFORE RUNNING IT.**

## Table of Content

- [Repository content](#repository-content): an overall description of directories and files of the repository
- [Signatures generation](#signatures-generation): the instructions to generate your `ETH_addrSignature` and `declarationSignature` and to serialize them inside a sandboxed environment.
- [Tech details](#tech-details): technical details about tools used in the sandboxed execution environment.

## Repository content

This repository contains the following directories and files:

- `pykeychecker`: an extend version (only [4 diffs](https://github.com/tezos/fundraiser-tools/compare/master...tzlibre:master?diff=split&name=master)) of the [`fundraiser-tools`](https://github.com/tezos/fundraiser-tools) by DLS; this is the only part of the code that interacts with private and sensible data to generate the required signatures.
- `jstxencoder`: a Node.js tools to serialize signatures as a `tx-data` hexadecimal field.
- `gen-signatures.sh`: a Bash script that improves usability and security by interactively asking for parameters to the user. 
- `Dockerfile`: the instructions to create the Docker-based sandboxed execution environment. 

## Signatures generation

### Inputs
To accomplish this step you need the following information:

- the Tz address (aka public key hash), you can find it in the pdf document you got during Tezos ICO
- the 15 word secret, provided in the pdf document you got during Tezos ICO
- the email you used during Tezos ICO, you can find it in the pdf document you got during Tezos ICO
- the password you use during the Tezos ICO
- an Ethereum address (under your control) you want to whitelist

> Pay attention: you can only whitelist an Ethereum address once, if you have to split several Tezos addresses, you have to use a different Ethereum address each time. 

### Outputs
At the end of this process you'll get:

- `ETH_addrSignature`: the signature of your Ethereum address
- `declarationSignature`: the signature of the declaration reported below
- `tx-data`: a serialization of the previous two, ready to be used as *transaction data* in a standard Ethereum transaction

> declaration to be signed: `I hereby cryptographically prove to be a contributor of Tezos Stiftung (CHE-290.597.458), a Swiss Foundation based in Gubelstrasse 11, 6300 Zug, Switzerland. I recognize and welcome the existence multiple implementations of Tezos. I ask and expect Tezos Stiftung to foster competition among them by funding and supporting their development, marketing and growth. Funds allotted to various Tezos implementations shall always be directly proportional to their market capitalization at the time of each distribution of funds. Distribution of funds to multiple existing Tezos implementations shall begin no later than January 1st 2019 and consistently continue throughout time. Following priorities autonomously set by each community, Tezos Stiftung shall distribute funds in the most appropriate, effective and transparent way.`

### Sandboxed execution environment generation
To improve security and simplify the environment configuration and dependencies installation process, you have to build a Docker image starting from our `Dockerfile`. 

By reading the Dockerfile content you'll be able to verify its behavior: it creates the environment and prepares it to run the script `gen-signature.sh`.

#### Install Docker
As a prerequisite of this step you need a working Docker environment. Docker installation instructions can be found [here](https://www.docker.com/community-edition#/download).

#### Get the code

Clone the repository from GitHub by issuing the command:

```sh
git clone https://github.com/tz-libre/fundraiser-tools.git
```

and then move inside the repository folder:

```sh
cd fundraiser-tools
```

#### Build the `tzlibre/cl-tools` Docker image
Once you cloned the repository and have Docker up and running, you have to issue this command:

```sh
docker build . -t tzlibre/cl-tools
```

> According to your system configuration you might need to run Docker with admin privileges: (e.g. `sudo docker build . -t tzlibre/cl-tools`).

At the end of the build, you should see the message:

```sh
Successfully tagged tzlibre/cl-tools:latest
```

or

```sh
Successfully built <some-hex-numbers>
```

which confirms that the building process terminated successfully.

### Run the Docker container to produce signatures

You have now built a Docker image that can use the `gen-signatures.sh` script. 

> **SINCE THIS STEP REQUIRES YOU TO INPUT YOUR SENSITIVE INFORMATION, WE SUGGEST YOU TO DISCONNECT FROM ALL NETWORKS BEFORE TO CONTINUE.**

To generate signatures issue this command and follow the instructions on screen:

```sh
docker run -it --rm tzlibre/cl-tools
```

> According to your system configuration you might need to run Docker with admin privileges: (e.g. `sudo docker run -it --rm tzlibre/cl-tools`).

Here is a full usage example:

```sh
$ docker run -it --rm tzlibre/cl-tools

 *********
 * INPUT *
 *********
   
15 Word Secret Key:
word1 word2 word word4 word5 word6 word7 word8 word9 word10 word11 word12 word13 word14 word15
   
Email:
your@email.com
   
Password:
yourPassword
   
Ethereum address to whitelist:
0x1234567890123456789012345678
   
   
 **********
 * OUTPUT *
 **********
	  
Tezos address (your public key hash):
tz1bG4r2PkzsxARQFnScVr51NaXrcVdF1Myg
	  
Tezos public key (`TZL_pk`):
012f1e1c8ed3eea205c75323c6db7f2a74b3273921c06a6629056331612d275e
	  
Signature of the Ethereum address (`ETH_addrSignature`):
1a9871ca4357ef82ab8b427e428e1f430c78755f4d15b826d89bfc57e0309e3f468b5ea5b73921138f9a5e3d132a995c7bacd5a8a50800589e29232382e66c0d
	  
Signature of the declaration (`declarationSignature`):
460323168a9b29629586ea888be344243a12003c381a9c427d2ebd94406f5e0376f1240c7d97b9acd686fa6003e10d72bdffc3f7ddeb3c7904d783a392ca490f
	  
Transaction data:
0x1d997f8b012f1e1c8ed3eea205c75323c6db7f2a74b3273921c06a6629056331612d275e000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000000401a9871ca4357ef82ab8b427e428e1f430c78755f4d15b826d89bfc57e0309e3f468b5ea5b73921138f9a5e3d132a995c7bacd5a8a50800589e29232382e66c0d0000000000000000000000000000000000000000000000000000000000000040460323168a9b29629586ea888be344243a12003c381a9c427d2ebd94406f5e0376f1240c7d97b9acd686fa6003e10d72bdffc3f7ddeb3c7904d783a392ca490f
```

> **VERIFY THAT THE `TEZOS ADDRESS` PROVIDED IN OUTPUT IS THE SAME YOU FIND IN THE PDF DOCUMENT YOU GOT DURING TEZOS ICO.**

### Optional signatures verification

To verify correctness of the produced signatures resort to [`signatures-verification-tool`](https://github.io/tzlibre/signatures-verification-tool).

### What's next?

In order to whitelist, issue a transaction according to the instructions provided in [TzLibre website](https://tzlibre.github.io/whitelist.html#send-tx).

After the transaction has been mined, you should wait. It usually takes up to 10 minutes for the oracle to respond.

Finally, you must verify that your address has been correctly whitelisted. You can do it on the (Verify)[https://tzlibre.github.io/verify.html] page on the TzLibre website.

- - -

## Tech details

This section explains technical usage details of the tools used in the sandboxed environment. This helps you to understand what happens under the hood. Although the sendboxed environment enhances usability and security (and we encourage you to use it), you might decide to separately run each tool to produce the required signatures.

### `pykeychecker`

The `pykeychecker` is a fork of [`fundraiser-tools`](https://github.com/tezos/fundraiser-tools) by DLS modified to sign your Ethereum address and the declaration reported above. Please check the (code diff)[https://github.com/tezos/fundraiser-tools/compare/master...tzlibre:master?diff=split&name=master]). Note that this is the only code that interacts with private and sensitive data.

#### Install system dependencies

- [Python 2.x](https://www.python.org/) (it is installed by default on many systems)
- [libsodium](libsodium.org) (on OSX via brew: `brew install libsodium`, on Ubuntu: `sudo apt install libsodium-dev`)

#### Install package dependencies

```sh
cd pykeychecker; pip install -r requirements.txt; cd ..
```
#### Run `pykeychecker` and save the output in a file named `keychecker_output.txt`

```sh
python pykeychecker/keychecker.py <15_words_mnemonic_seed> <your@email.com> <your_P4s5w0rd> <0x...yourEthAddress> > keychecker_output.txt
```
> PAY ATTENTION: if your password contains special characters (e.g. `&`, `\`, `|`, `!`, etc.), surrond it with `'`. 
> PAY ATTENTION: if your password contains `'`, refer to this example: `tz'libre -> 'tz'\''libre'`.
> **PAY ATTENTION: THIS APPROACH LEAKS YOUR SECRET INFORMATION ON THE COMMAND LINE. PLEASE USE THE (`gen-signatures.sh`)[#gen-signatures.sh] SCRIPT INSTEAD.**

Here is a usage example:

```sh
python pykeychecker/keychecker.py word1 word2 word word4 word5 word6 word7 word8 word9 word10 word11 word12 word13 word14 word15 your@email.com yourPassord 0x1234567890123456789012345678
```

#### Verify the computed Tezos address 

Open `keychecker_output.txt` and verify that the computed Tezos address is correct.

```sh
cat keychecker_output.txt | grep TZL_addr
```

If it does not match, carefully check input parameters.

You'll also be able to check that no private data is present in this file.

### `jstxencoder`

The `jstxencoder` serializes the output of the forked version of `pykeychecker` to allow to conveniently invoke an Ethereum smart contract method issuing a standard tx with data.

#### Install system dependencies

- Node.js: use [nvm](https://github.com/creationix/nvm) to install last stable release.
- `make` and a proper C/C++ compiler toolchain (`sudo apt install build-essentials` on Ubuntu, Xcode on Mac OS X)

#### Install package dependencies

```sh
cd jstxencoder; npm install; cd ..
```

#### Run

```sh
cat keychecker_output.txt | node jstxencoder 
```

### `gen-signatures.sh`

Instead of running `pykeychecker` and `jstxencoder` separately, you are encouraged to exploit the `gen-signature.sh` script to improve usability and security. 

First of all, read the `gen-signature.sh` file to verify what it does.

To do so, issue the command and follow the provided instructions:

```sh
bash gen-signatures.sh
```

Here is an example:

```sh
$ bash gen-signature.sh

 *********
 * INPUT *
 *********
   
15 words secret key:
word1 word2 word word4 word5 word6 word7 word8 word9 word10 word11 word12 word13 word14 word15
   
Email:
your@email.com
   
Password:
yourPassword
   
Ethereum address to whitelist:
0x1234567890123456789012345678
   
   
 **********
 * OUTPUT *
 **********
	  
Tezos address (your public key hash):
tz1bG4r2PkzsxARQFnScVr51NaXrcVdF1Myg
	  
Tezos public key (`TZL_pk`):
012f1e1c8ed3eea205c75323c6db7f2a74b3273921c06a6629056331612d275e
	  
Signature of the Ethereum address (`ETH_addrSignature`):
1a9871ca4357ef82ab8b427e428e1f430c78755f4d15b826d89bfc57e0309e3f468b5ea5b73921138f9a5e3d132a995c7bacd5a8a50800589e29232382e66c0d
	  
Signature of the declaration (`declarationSignature`):
460323168a9b29629586ea888be344243a12003c381a9c427d2ebd94406f5e0376f1240c7d97b9acd686fa6003e10d72bdffc3f7ddeb3c7904d783a392ca490f
	  
Transaction data:
0x1d997f8b012f1e1c8ed3eea205c75323c6db7f2a74b3273921c06a6629056331612d275e000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000000401a9871ca4357ef82ab8b427e428e1f430c78755f4d15b826d89bfc57e0309e3f468b5ea5b73921138f9a5e3d132a995c7bacd5a8a50800589e29232382e66c0d0000000000000000000000000000000000000000000000000000000000000040460323168a9b29629586ea888be344243a12003c381a9c427d2ebd94406f5e0376f1240c7d97b9acd686fa6003e10d72bdffc3f7ddeb3c7904d783a392ca490f
```

