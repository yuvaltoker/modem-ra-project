# What image do we start from
FROM polinux/snmpd

# The instructions for when the container is on, the modem behavior python program, making it all executable:
COPY ./instructions.sh /
COPY ./modem.py /
RUN chmod 777 /modem.py
RUN chmod 777 /instructions.sh

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
ENTRYPOINT ["bash","/instructions.sh"]
