#!/bin/bash

SOURCE="pyright-venv.py"
DESTINATION="$HOME/.local/bin"
TARGET="pyright-venv"

echo "
    ┌──────────────────────────────┐
    │      pyright-venv setup      │
    ├──────────────────────────────┤
    │ [1] Install pyright-venv     │
    │ [2] Uninstall pyright-venv   │
    │ [3] Exit                     │
    └──────────────────────────────┘
"

read -p "Select an option (default=1): " option
option=${option:-1}

echo ""

case "$option" in
  1)
    if [[ -f "$DESTINATION/$TARGET" ]]; then
      echo "[-] pyright-venv is already installed in $DESTINATION"
      echo "Reinstalling pyright-venv ..."
      echo ""
      rm "$DESTINATION/$TARGET"
    fi

    mkdir -p "$DESTINATION"  # Create the destination directory (~/.local/bin) if it does not yet exist
    cp "$SOURCE" "$DESTINATION/$TARGET"  # Copy the script to the destination directory
    chmod +x "$DESTINATION/$TARGET"  # Make the script executable as a program
    echo "[+] pyright-venv has been installed in $DESTINATION"

    if [[ ":$PATH:" != *":$DESTINATION:"* ]]; then
      echo "[!] $DESTINATION is not in your PATH"
      echo "You may want to add this line to your shell config (~/.bashrc or ~/.zshrc):"
      echo "  export PATH=\"$DESTINATION:\$PATH\""
    fi

    ;;
  2)
    if [[ -f "$DESTINATION/$TARGET" ]]; then
      rm "$DESTINATION/$TARGET"
      echo "[+] pyright-venv has been uninstalled from $DESTINATION"
    else
      echo "[-] pyright-venv is not currently installed in $DESTINATION"
    fi
    ;;
  3)
    exit 0
    ;;
  *)
    echo "[-] Invalid option: $option"
    echo ""
    exit 1
    ;;
esac

echo ""
