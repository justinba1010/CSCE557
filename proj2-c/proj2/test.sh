SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"

# Test vectors
# This could be any binary file (That doesn't have null terminators)

values=(
  'Hello world ß∂ƒ©˙∆©√ç≈Ωßåœ∑´®†¥¨˙©∫√ç≈ more special characters'
  '1234567890qwertyuioasdfghjk'
)

pushd $SCRIPT_DIR
  mkdir -p test
  pushd $SCRIPT_DIR/test
  for datarow in "${values[@]}"; do
    while IFS=',' read -r i n k;  do
    echo $datarow > ./plaintext
    echo "Testing encrypting and decrypting " $datarow
    echo "Key Generation"
    time (python3 $SCRIPT_DIR/generate_key.py publickey privatekey)
    echo "Encryption"
    time (python3 $SCRIPT_DIR/encrypt.py plaintext publickey cipher)
    echo "Decryption"
    time (python3 $SCRIPT_DIR/decrypt.py cipher privatekey decipher)
    diff plaintext decipher
    if [ $? != 0 ]; then
      echo "Failure"
    else
      echo "Success"
    fi

    done <<< "$datarow"
  done

    popd
popd
