# Contest Management System (CMS) on Docker-Compose

This project aims to wrap the Contest Management System [CMS]((https://github.com/cms-dev/cms) in a docker-compose setup.

## How to Use

- The setup was tested on Ubuntu 18.04 with Docker 19.03.6.
- Docker-compose was manually installed. (version 1.25.4)
### Setup Steps
- Install docker and docker-compose on your Ubuntu 18.04 workstation.
```sh
apt-get install -y docker.io docker-compose git
usermod -aG docker $USER
systemctl enable docker && systemctl start docker
curl -L https://github.com/docker/compose/releases/download/1.25.4/docker-compose-`uname -s`-`uname -m` -o /usr/bin/docker-compose
chmod +x /usr/bin/docker-compose
```
- Clone this repository to `./cms-compose` and enter the directory.
- Add your certificate to `./nginx/*.key\crt` or self-generate SSL certificates using `./generateCerts.sh`.
- Modify your CMS config in `./cms-app/config/*.conf`.
- Put your courses into `./courses/`.
- Start the docker-compose instance.
`docker-compose up --build`
- Enter
  - `https://$HOST/` for contest login
  - `https://$HOST/admin` for admin login

### Remarks
When modifying the `./cms-app/config/cms.conf`, make sure to keep the access credentials/database name to the PostgreSQL database. If you need to change the credentials/database name, please adapt them in `./docker-compose.yml` and `./postgres/initdb.sql` accordingly.

The logs are accessible at `./cms-logs/` after the docker-compose instance was launched.
