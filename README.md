# mitm-smtp
A proxy for SMTP to catch both, encrypted and unencrypted mails sent using SMTP.

## Usage
To use mitm-smtp as a transparent SMTP Proxy, enable forwarding mode...
``sysctl -w net.ipv4.ip_forward=1``
...block ICMP redirects...
``sysctl -w net.ipv4.conf.all.send_redirects=0``
...and create a port forwarding.
``iptables -t nat -A PREROUTING -p tcp --destination-port 587 -j REDIRECT --to-port 8888``

## Reference
https://tools.ietf.org/html/rfc5321

manage/account/verify?email&#61;blog%40smartnoob.de&amp;t&#61;ZjErNvfUarveUSgJ
