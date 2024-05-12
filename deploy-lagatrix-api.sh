#!/bin/bash

error_msg() {
    echo -e "\e[31m$1\e[0m"
    exit 1
}

add_service_user() {
    useradd -r -s /usr/sbin/nologin lagatrix
    passwd -d lagatrix
}

set_service() {
    cp lagatrix-api.service /usr/lib/systemd/system/lagatrix-api.service
    systemctl enable lagatrix-api.service
    systemctl start lagatrix-api.service
}

set_files() {
    python3 -m venv /opt/lagatrix-api/venv
    source /opt/lagatrix-api/venv/bin/activate
}

create_skeleton() {
    mkdir /opt/lagatrix-api
    mkdir /opt/lagatrix-api/log
    mkdir /opt/lagatrix-api/ssl

    touch /opt/lagatrix-api/log/lagatrix.log
    touch /opt/lagatrix-api/log/error.log
}

deploy_files() {
    chown lagatrix:lagatrix -R /opt/lagatrix-api
    cp ./pyproject.toml /opt/lagatrix-api
    cp ./poetry.lock /opt/lagatrix-api
    cp -r ./src/* /opt/lagatrix-api
    cp ./lagatrix.conf /opt/lagatrix-api
    cp ./executor.sh /opt/lagatrix-api
}

install_system_components() {
    $1 $4 $3
    $1 $4 $2 $5
}

install_python_components() {
    pip install poetry
    poetry lock
    poetry install --no-root --only main
}

create_key_pait() {
    openssl req -x509 -newkey rsa:4096 -nodes -out /opt/lagatrix-api/ssl/cert.pem -keyout /opt/lagatrix-api/ssl/key.pem -days 365 -subj "/C=ES/ST=La Rioja/L=Logronio/O=Lagatrix/OU=LA/CN=lagatrix.com"
}

set_package_manager() {
    family=$(cat /etc/os-release | grep -w 'ID_LIKE\|ID' | awk -F = '{print $2}' | xargs)

    case "${family}" in
        *rhel*)
            package_manager=yum
            install_param=install
            update_param=update
            no_confirm=-y
            packages="sudo python3-venv dmidecode openssl"
        ;;
        *debian*)
            package_manager=apt
            install_param=install
            update_param=update
            no_confirm=-y
            packages="sudo python3-venv dmidecode openssl"
        ;;
        *suse*)
            package_manager=zypper
            install_param=install
            update_param=update
            no_confirm=-n
            packages="cronie sudo python3-venv dmidecode openssl"
        ;;
        *arch*)
            package_manager=pacman
            install_param=-S
            update_param=-Sy
            no_confirm=--noconfirm
            packages="cronie sudo python3-venv dmidecode openssl"
        ;;
        *)
            error_msg "No supported family"
        ;;
    esac
}

main() {
    set_package_manager

    if install_system_components $package_manager $install_param $update_param $no_confirm "$packages"; then

        if ls lagatrix-api.service src pyproject.toml > /dev/null 2>&1; then
            add_service_user $package_manager > /dev/null 2>&1
            set_service > /dev/null 2>&1
            create_skeleton
            set_files
            create_key_pait > /dev/null 2>&1
            deploy_files

            install_python_components

            systemctl status start lagatrix-api.service > /dev/null 2>&1

            echo -e "\e[32mInstalation complete\e[0m"
        else
            error_msg "The files needed to install Lagatrix API could not be found"
        fi
    else
        error_msg "The components were not installed correctly"
    fi
}

if (( $(id -u) == 0 )); then
    main
else
    error_msg "Need root permissions"
fi
