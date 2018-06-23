const fs = require('fs')
const coder = require('web3-eth-abi')

const METHOD_SIGNATURE = 'whitelist(bytes32,bytes,bytes)'
const METHOD_INPUT_TYPES = ['bytes32', 'bytes', 'bytes']

/* LIBS */

function remove_0x (addr) {
  return addr.replace('0x', '')
}

function add_0x (addr) {
  if (addr.startsWith('0x')) {
    return addr
  }

  return '0x' + addr
}

function generate_tx_data (TZL_pk, ETH_addr_signature, declaration_signature) {
  let params = Array.prototype.slice.call(arguments, 0).map(add_0x)
  let encodedFunctionSignature = coder.encodeFunctionSignature(METHOD_SIGNATURE)
  let encodedParameters = remove_0x(coder.encodeParameters(METHOD_INPUT_TYPES, params))
  let tx_data = encodedFunctionSignature + encodedParameters

  return remove_0x(tx_data)
}

function parse_input () {
  let stdinBuffer = fs.readFileSync(0)
  let data = stdinBuffer.toString()
  let parsed = JSON.parse(`{
    ${data.trim().split('\n')
      .map(l => l.split(':')
	   .map(e => `"${e.trim()}"`)
	   .join(':')
	  )
      .join(',')}
  }`)

  return parsed
}

/** MAIN **/

function main () {
  // parse input
  let input = parse_input()

  // get tx data
  let tx_data = generate_tx_data(
    input.TZL_pk,
    input.ETH_addrSignature,
    input.declarationSignature
  )

  // Print transaction data
  console.log(add_0x(tx_data))

}

if (!module.parent) {
  main()
}
