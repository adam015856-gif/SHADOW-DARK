name: Build SHADOW DARK APK

on:
  workflow_dispatch:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
      - name: Download Project
        uses: actions/checkout@v4

      - name: Cache Buildozer & Android SDK
        uses: actions/cache@v4
        with:
          path: |
            ~/.buildozer
            .buildozer
          key: buildozer-${{ runner.os }}-py3.10-${{ hashFiles('buildozer.spec') }}
          restore-keys: |
            buildozer-${{ runner.os }}-py3.10-

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            git zip unzip openjdk-17-jdk \
            autoconf libtool pkg-config \
            zlib1g-dev libffi-dev libssl-dev \
            build-essential cmake libncurses5-dev \
            libsqlite3-dev libreadline-dev libtk8.6 libgdm-dev \
            libdb4o-dev libpcap-dev

      - name: Install Buildozer
        run: |
          pip install --upgrade pip wheel setuptools
          pip install buildozer cython==0.29.33

      - name: Build APK
        run: yes | buildozer android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: SHADOW-DARK-APK
          path: bin/*.apk
