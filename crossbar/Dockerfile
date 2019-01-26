FROM crossbario/crossbar-armhf

# copy over our own node directory from the host into the image
# set user "root" before copy and change owner afterwards
USER root
COPY ./crossbar /node
RUN chown -R crossbar:crossbar /node

ENTRYPOINT ["crossbar", "start", "--cbdir", "/node/.crossbar"]
