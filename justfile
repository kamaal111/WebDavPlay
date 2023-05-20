set export

DEVCONTAINER := ".devcontainer"
MANAGE_PY := "manage.py"
DEVCONTAINER_VIRTUAL_ENVIRONMENT :=  DEVCONTAINER / ".venv"

run-dev:
    #!/bin/zsh

    . $DEVCONTAINER_VIRTUAL_ENVIRONMENT/bin/activate
    python $MANAGE_PY migrate
    python $MANAGE_PY runserver

setup-dev-container: copy-to-container setup-zsh-environment setup-python-for-devcontainer

initialize-dev-container: copy-git-config-from-outside-container set-environment

[private]
setup-python-for-devcontainer:
    #!/bin/zsh

    if [ ! -d $DEVCONTAINER_VIRTUAL_ENVIRONMENT ]
    then
        python -m venv $DEVCONTAINER_VIRTUAL_ENVIRONMENT
    fi

    . $DEVCONTAINER_VIRTUAL_ENVIRONMENT/bin/activate

    pip install poetry

[private]
setup-zsh-environment:
    #!/bin/zsh

    if [ ! -f $ZSH/oh-my-zsh.sh ]
    then
        echo "Installing Oh My Zsh"
        sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    fi

    if [ ! -d ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions ]
    then
        echo "Installing zsh-autosuggestions"
        git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
    fi

    if [ ! -d ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting ]
    then
        echo "Installing zsh-syntax-highlighting"
        git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
    fi

    echo "Updating zsh configuration"
    cp -f $DEVCONTAINER/.zshrc ~/.zshrc
    cp -f $DEVCONTAINER/.zshenv ~/.zshenv

[private]
set-environment:
    #!/bin/zsh

    ENVIRONMENT_FILE="$DEVCONTAINER/.zshenv"

    rm -rf $ENVIRONMENT_FILE
    touch $ENVIRONMENT_FILE

    echo "export LC_ALL=C" >> $ENVIRONMENT_FILE
    echo "export USER=$USER" >> $ENVIRONMENT_FILE

[private]
copy-git-config-from-outside-container:
    #!/bin/zsh

    cp -f ~/.gitconfig $DEVCONTAINER/.gitconfig

[private]
copy-to-container:
    #!/bin/zsh

    cp -f $DEVCONTAINER/.gitconfig ~/.gitconfig
