# Command-line tools 

This repository contains **Command-line tools** to ease  [whitelisting](https://tzlibre.github.io/whitelist.html) for the [TzLibre](https://tzlibre.github.io) split.

These tools are based on a fork of DLS [`fundraiser-tools`](https://github.com/tezos/fundraiser-tools).

The **Command-line tools** support you in:

1. generating two digital signatures (namely `ETH_addrSignature` and `declarationSignature`) to prove  ownership of a Tezos private key and therefore the right to receive TZL coins;
2. serializing both signatures in a single `tx-data` field to be broadcast into an Ethereum transaction according to the instructions provided on the [TzLibre website](https://tzlibre.github.io/whitelist.html#send-tx).

To improve usability and security a sandboxed execution environment is provided as a Docker container, along with an invocation bash script.

## Security

As a standard security practice when handling sensitive data you must:
1. Read the whole source beforehand and be fully responsible for the code you run on your computer.
2. Verify the computer you're using is secure and not compromised.

## Table of Content

- [Declaration](#declaration): description and content of the declaration
- [Repository content](#repository-content): description of the directories and files of the repository
- [Signatures generation](#signatures-generation): instructions to generate your `ETH_addrSignature` and `declarationSignature`, and to serialize them inside a sandboxed environment.
- [Tech details](#tech-details): technical details of the tools used in the sandboxed execution environment.

## Declaration

Whitelisting involves cryptografically signing a declaration to support decoupling the Tezos idea from its implementations. You must read, understand and agree with the declaration before signing it. Signatures are pseudonymous and not linked with your identity. You should not sign the declaration if you don't fully understand and agree with its content.

> Declaration: `I hereby cryptographically prove to be a contributor of Tezos Stiftung (CHE-290.597.458), a Swiss Foundation based in Gubelstrasse 11, 6300 Zug, Switzerland. I recognize and welcome the existence multiple implementations of Tezos. I ask and expect Tezos Stiftung to foster competition among them by funding and supporting their development, marketing and growth. Funds allotted to various Tezos implementations shall always be directly proportional to their market capitalization at the time of each distribution of funds. Distribution of funds to multiple existing Tezos implementations shall begin no later than January 1st 2019 and consistently continue throughout time. Following priorities autonomously set by each community, Tezos Stiftung shall distribute funds in the most appropriate, effective and transparent way.`


## Repository content

This repository contains the following directories and files:

- `Dockerfile`: instructions to create the Docker-based sandboxed execution environment. A Docker environment increases safety and stability, and allows the user to avoid installing dependencies or configuring an environment.
- `gen-signatures.sh`: Bash script that improves usability and security by interactively asking the user for inputs while running the `pykeychecker` and `jstxencoder` tools. 
- `pykeychecker`: written in Python, this is an extended version (you can verify the [4 diffs](https://github.com/tezos/fundraiser-tools/compare/master...tzlibre:master?diff=split&name=master]#diff-e6c8e5e03826917a611ce5c5e23626fc)) of the broken DLS [`fundraiser-tools`](https://github.com/tezos/fundraiser-tools) which it also fixes. This is the only part of the code that interacts with private and sensible data. It then generates signatures for the declaration and for your Ethereum address. 
- `jstxencoder`: Node.js tool to serialize public key and signatures as a `tx-data` hexadecimal field. It allows to pass the three parameters to an Ethereum smart contract.


## Signatures generation

### Inputs
This information is required:

- Tezos address (aka public key hash). You can find it in the PDF containing your contribution data.
- 15 words secret. You can find them in the PDF containing your contribution data.
- email used when contributing to the Tezos ICO. You can find it in the PDF containing your contribution data.
- password set during Tezos ICO.
- an Ethereum address you want to whitelist.

> You can whitelist an Ethereum address only once. The same Ethereum address can't be used to split multiple Tezos addresses. If you need to split several Tezos addresses you must to use a new Ethereum address each time. 

### Outputs
At the end of this process you'll get:

- `ETH_addrSignature`: signature of your Ethereum address.
- `declarationSignature`: signature of the declaration (reported below).
- `tx-data`: a serialization of the previous two signatures, ready to be used as *transaction data* in a standard Ethereum transaction.

### 1. Sandboxed execution environment generation
To improve security, simplify environment configuration and avoid installing dependencies, you can build a Docker image starting from our `Dockerfile`. 

The `Dockerfile` creates an environment and then prepares it to run `gen-signature.sh`. You can read the content of the file to verify its behavior.

#### 1.1 Install Docker
You'll need a working Docker environment. Docker installation instructions can be found [here](https://www.docker.com/community-edition#/download).

#### 1.2 Get the code

Clone the **Command-line tools** repository from GitHub:

```sh
git clone https://github.com/tz-libre/fundraiser-tools.git
```

then move to the repository folder:

```sh
cd fundraiser-tools
```

#### 1.3 Build the `tzlibre/cl-tools` Docker image
Once you cloned the repository and have Docker up and running, you should issue:

```sh
docker build . -t tzlibre/cl-tools
```

> Depending on your system configuration you might need to run Docker with admin privileges: (e.g. `sudo docker build . -t tzlibre/cl-tools`).

At the end of the build, you should see this message:

```sh
Successfully tagged tzlibre/cl-tools:latest
```

or

```sh
Successfully built <some-hex-numbers>
```

These messages confirm the environment has been successfully built.

### 2. Run Docker container to produce signatures

You have now built a Docker image that can use the `gen-signatures.sh` script. 

> **THIS STEP WILL REQUIRE TO INPUT YOUR SENSITIVE INFORMATION. WE SUGGEST TO DISCONNECT FROM ALL NETWORKS BEFORE CONTINUING.**

To generate signatures issue this command and follow on screen instructions:

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

> You should now verify that `Tezos address` provided in output is the same you find in your Tezos contribution PDF.

> Finally, you should copy & paste the `Transaction data` provided in output, and then save it as a plain text file.

### 3. Signatures verification (optional)

To verify correctness of the produced signatures you can use the [`signatures-verification-tool`](https://github.io/tzlibre/signatures-verification-tool).

### 4. Broadcast

You've now generated your `Transaction data`. 

You must now broadcast them by sending an Ethereum transaction following instructions on the [TzLibre website](https://tzlibre.github.io/whitelist.html#send-tx).

- - -

## Tech details

This section explains technical details of the tools used in the sandboxed environment. It'll help you understand what happens under the hood: although the sendboxed environment enhances usability and security (and we encourage you to use it), you might choose to separately run each tool to produce the required signatures.

### `pykeychecker`

The `pykeychecker` is a fork of DLS [`fundraiser-tools`](https://github.com/tezos/fundraiser-tools) which fixes a broken dependency in the DLS repo. It also upgrades it to sign your Ethereum address and the declaration reported above. You can check the [code diff](https://github.com/tezos/fundraiser-tools/compare/master...tzlibre:master?diff=split&name=master]#diff-e6c8e5e03826917a611ce5c5e23626fc)). Note that this is the only code that interacts with private and sensitive data.

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
> If your password contains special characters (e.g. `&`, `\`, `|`, `!`, etc.), encapsulate it with `'`. 
> If your password contains `'`, prepend `'\'` (e.g.`I'mapassword -> 'I'\''mapassword'`).

Here is a usage example:

```sh
python pykeychecker/keychecker.py word1 word2 word word4 word5 word6 word7 word8 word9 word10 word11 word12 word13 word14 word15 your@email.com yourPassord 0x1234567890123456789012345678
```

#### Verify the computed Tezos address 

Open `keychecker_output.txt` and verify that the computed Tezos address is correct.

```sh
cat keychecker_output.txt | grep TZL_addr
```

If it does not match your Tezos address, please check input parameters again.

You can verify that no private data is contained in this file.

### `jstxencoder`

`jstxencoder` serializes the output of  `pykeychecker` to allow invoking an Ethereum smart contract method by issuing a standard tx with data.

#### Install system dependencies

- Node.js: use [nvm](https://github.com/creationix/nvm) to install the latest stable release.
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

Instead of running `pykeychecker` and `jstxencoder` separately, we suggest to use the `gen-signature.sh` script to improve usability and security. 

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

We encourage you to read `gen-signature.sh` content to verify its behavior.
