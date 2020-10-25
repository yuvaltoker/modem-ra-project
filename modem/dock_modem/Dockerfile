# What image do we start from
#FROM polinux/snmpd
FROM python:3
# The instructions for when the container is on && making it executive:
COPY ./instructions.sh /
COPY ./modem.py /
RUN chmod 777 /modem.py
RUN chmod 777 /instructions.sh
# The mib files
#COPY ./MY-TUTORIAL-MIB.txt /usr/share/snmp/mibs/
#COPY ../../mibs/NET-SNMP-TUTORIAL-MIB.txt /usr/share/snmp/mibs/
# Installing helpful functioning for the programmer's use
RUN apt update
RUN apt install -y nano
RUN pip install redis
# When the container is on, execute the instruction file
#ENTRYPOINT ["python","./modem.py"]
ENTRYPOINT ["bash","/instructions.sh"]
