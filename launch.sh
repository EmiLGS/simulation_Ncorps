is_installed()
{
    LANG=C apt-cache policy "$1" 2> /dev/null | grep -qv "Installed:(none)"
}
is_pip_installed()
{
    pip list 2> /dev/null | grep -qv "$1"
}

if ! is_installed python3;
    then
        sudo apt-get install python3.10;
fi
if ! is_installed pip;
    then
        python3 get-pip.py;
fi
if ! is_pip_installed pygame;
    then
        python3 -m pip install -U pygame --user;
fi
if ! is_pip_installed matplotlib;
    then
        pip install matplotlib
fi
python3 Main.py