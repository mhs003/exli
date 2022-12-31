exli
====
`exli` extracts links from pdf or txt files.

## install

in **Linux**:

clone the repo:
```bash
git clone https://github.com/mhs003/exli.git
cd exli 
```

install requirements:
```bash
sudo apt install python3 python3-pip
sudo pip3 install PyPDF2
sudo pip3 install tld
```

change installer file's permission:
```bash
chmod +x install-linux.bash
```

install `exli`:
```bash
bash install-linux.bash
```

---

in **Termux**:

clone the repo:
```bash
git clone https://github.com/mhs003/exli.git
cd exli 
```

install requirements:
```bash
pkg install python
pip install PyPDF2
pip install tld
```

change installer file's permission:
```bash
chmod +x install-termux.bash
```

install `exli`:
```bash
bash install-termux.bash
```


## uninstall

in **Linux**:

run,
```bash
chmod +x remove-linux.bash
bash remove-linux.bash
```

---

in **Termux**:

run,
```bash
chmod +x remove-termux.bash
bash remove-termux.bash
```

## usage

use the command in terminal to view help document:
```bash
exli -h
```
