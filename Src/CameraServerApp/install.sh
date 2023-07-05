tools=(build-essential cmake curl default-jdk libgtk2.0-dev pkg-config libv4l-dev libavcodec-dev libavformat-dev libswscale-dev python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev ant)
curl -sL https://github.com/opencv/opencv/archive/refs/tags/4.8.0.tar.gz | tar xvz -C /tmp

cd /tmp/opencv-4.8.0 && mkdir build && cd build

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export ANT_HOME=/usr/bin/ant

cmake -D BUILD_SHARED_LIBS=OFF ..
make -j8
make install

mkdir /opencv-java-bin
cp bin/opencv-480.jar lib/libopencv_java480.so /opencv-java-bin

apt-get remove --purge -y ${tools[@]} && apt-get autoclean && apt-get -y autoremove && apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*Z