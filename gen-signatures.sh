#! /bin/bash
OUTPUT=keychecker_output.txt

echo -e "\n *********"
echo -e   " * INPUT *"
echo      " *********"

echo -e "\n15 words secret key:"
read MNEMONIC

echo -e "\nEmail:"
read EMAIL

echo -e "\nPassword:"
read PASSWORD

echo -e "\nEthereum address to whitelist:"
read ETH_ADDR

python pykeychecker/keychecker.py $MNEMONIC $EMAIL "$PASSWORD" $ETH_ADDR > $OUTPUT

echo -e "\n\n **********"
echo -e     " * OUTPUT *"
echo        " **********"

echo -e "\nTezos address (your public key hash):"
cat $OUTPUT | grep TZL_addr | cut -d ' ' -f2

echo -e "\nTezos public key (\`TZL_pk\`):"
cat $OUTPUT | grep TZL_pk | cut -d ' ' -f2

echo -e "\nSignature of the Ethereum address (\`ETH_addrSignature\`):"
cat $OUTPUT | grep ETH_addrSignature | cut -d ' ' -f2

echo -e "\nSignature of the declaration (\`declarationSignature\`):"
cat $OUTPUT | grep declarationSignature | cut -d ' ' -f2

echo -e "\nTransaction data:"
cat $OUTPUT | node jstxencoder
