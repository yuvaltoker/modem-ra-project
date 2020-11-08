# What image do we start from
FROM polinux/snmpd

# The instructions for when the container is on, the ra behavior python program, making it all executable:
COPY ./instructions.sh /
COPY ./ra.py /
RUN chmod 777 /instructions.sh
RUN chmod 777 /ra.py

# 
COPY ./MY-TUTORIAL-MIB.txt /usr/share/snmp/mibs

RUN yum install -y nano
RUN yum install -y python3
RUN yum install -y epel-release
RUN yum install -y python-pip
RUN yum install -y python-devel
RUN yum groupinstall -y 'development tools'
RUN pip3 install pysnmp 
RUN pip3 install pysnmp-mibs
#RUN yum install -y libsmi # not used yet, delete in case of successful running project
#RUN echo path :/usr/share/snmp/mibs/ >> /etc/smi.conf # not used yet, delete in case of successful running project

# compiling your mib file into one that pysnmp can use, the new file/s destination repository is /root/.pysnmp/mibs
RUN mibdump.py MY-TUTORIAL-MIB.txt

ENTRYPOINT ["bash","/instructions.sh"]
