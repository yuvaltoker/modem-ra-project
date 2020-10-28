# What image do we start from
FROM polinux/snmpd
#FROM python:3

# The instructions for when the container is on && making it executive:
COPY ./instructions.sh /
COPY ./modem.py /
RUN chmod 777 /modem.py
RUN chmod 777 /instructions.sh

# The mib files
#COPY ./MY-TUTORIAL-MIB.txt /usr/share/snmp/mibs/
#COPY ../../mibs/NET-SNMP-TUTORIAL-MIB.txt /usr/share/snmp/mibs/

# Installing helpful functioning for the programmer's use
RUN yum install -y nano
RUN yum install -y python3
RUN yum install -y epel-release
RUN yum install -y python-pip
RUN yum install -y python-devel
RUN yum groupinstall -y 'development tools'
RUN pip3 install pysnmp 
RUN pip3 install redis

# When the container is on, execute the instruction file
#ENTRYPOINT ["python","./modem.py"]
ENTRYPOINT ["bash","/instructions.sh"]
