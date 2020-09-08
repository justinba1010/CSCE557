SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"

pushd $SCRIPT_DIR
  mkdir -p test
  pushd $SCRIPT_DIR/test
    echo "hello world\n this is a test.\n ¡™£¢∞§¶•ª\n" > ./plaintext
    echo "Key Generation"
    time (python3 $SCRIPT_DIR/generate_key.py publickey privatekey)
    echo
    time (python3 $SCRIPT_DIR/encrypt.py plaintext publickey cipher)
    time (python3 $SCRIPT_DIR/decrypt.py cipher privatekey decipher)
    diff plaintext decipher
    if [ $? != 0 ]; then
      echo "Failure"
    else
      echo "Success"
    fi
  popd
popd
