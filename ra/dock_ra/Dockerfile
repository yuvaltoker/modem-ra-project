FROM polinux/snmpd
COPY ./instructions.sh /
COPY ./ra.py /
COPY ./test.py /
RUN chmod 777 /instructions.sh
RUN chmod 777 /ra.py
RUN chmod 777 /test.py
RUN yum install -y nano
RUN yum install -y python3
RUN yum install -y epel-release
RUN yum install -y python-pip
RUN yum install -y python-devel
RUN yum groupinstall -y 'development tools'
RUN pip3 install pysnmp 
ENTRYPOINT ["bash","/instructions.sh"]
