# Astroncia IPTV
### IPTV player with EPG support

[![license](https://img.shields.io/badge/license-GPL%20v.3-green.svg)](https://gitlab.com/astroncia/iptv/-/blob/master/COPYING) [![PPA](https://img.shields.io/badge/PPA-available-green.svg)](https://launchpad.net/~astroncia/+archive/ubuntu/iptv) [![AUR](https://img.shields.io/aur/version/astronciaiptv)](https://aur.archlinux.org/packages/astronciaiptv/) [![Packaging status](https://repology.org/badge/tiny-repos/astronciaiptv.svg)](https://repology.org/project/astronciaiptv/versions)  

[![GUI](https://gitlab.com/astroncia/iptv/-/raw/master/screenshots/astroncia-iptv-screenshot-thumb.png)](https://gitlab.com/astroncia/iptv/-/raw/master/screenshots/astroncia-iptv-screenshot.png)  

## Download

deb and rpm packages available in [Releases](https://gitlab.com/astroncia/iptv/-/releases)  
  
For Ubuntu / Linux Mint **recommended** install from [Launchpad PPA - ppa:astroncia/iptv](https://launchpad.net/~astroncia/+archive/ubuntu/iptv):  
```sudo add-apt-repository ppa:astroncia/iptv -y```  
```sudo apt-get update```  
```sudo apt-get install astroncia-iptv```  
  
Installation for Debian:  
```sudo gpg --no-default-keyring --keyring /usr/share/keyrings/astroncia-iptv-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0x20F6B78167C962EA29F8112EB4A4D3FDCE021A84```  
```echo 'deb [signed-by=/usr/share/keyrings/astroncia-iptv-archive-keyring.gpg] http://ppa.launchpad.net/astroncia/iptv/ubuntu focal main' | sudo tee /etc/apt/sources.list.d/astroncia-iptv.list```  
```sudo apt-get update```  
```sudo apt-get install astroncia-iptv```  
  
If you got *No dirmngr* error when running gpg:  
```sudo apt-get install dirmngr```  
```sudo dirmngr &```  
  
[Arch Linux (AUR)](https://aur.archlinux.org/packages/astronciaiptv/)  

## Information

Software provided **as is**, no guarantees.  

Repository mirrors:  
[GitLab](https://gitlab.com/astroncia/iptv) (**main repository**)  
[Bitbucket](https://bitbucket.org/astroncia/astroncia-iptv/src/master/)  
[Codeberg](https://codeberg.org/astroncia/iptv)  

## License

Code: [GPLv3](https://gitlab.com/astroncia/iptv/-/blob/master/COPYING)  
Icons: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
  
*Icons by [Font Awesome](https://fontawesome.com/)*  

## Capabilities

Watching IPTV (from m3u8 playlist)  
Viewing unencrypted streams UDP (multicast), HTTP, HLS (m3u8)  
Adding channels to favorites  
Recording TV programs  
Hotkeys  
Channel search  
TV program (EPG) support in XMLTV and JTV formats  
Display of technical information - video / audio codec, bit rate, resolution  
Channel groups (from playlist and custom)  
Hide channels  
Sorting channels  
Video settings for each channel - contrast, brightness, hue, saturation, gamma  
Change user agent for each channel  
M3U playlist editor  
TV archive  

## Dependencies

- Qt 6 *(or Qt 5)*
- libmpv1 (>= 0.27.2)
- [ffmpeg](https://ffmpeg.org/)
- Python 3 (>= 3.6)
- [PySide6](https://pypi.org/project/PySide6/) *(or PyQt5)*
- [Pillow](https://pypi.org/project/Pillow/) (python3-pil)
- [pandas](https://pypi.org/project/pandas/) (python3-pandas)
- [PyGObject](https://pypi.org/project/PyGObject/) (python3-gi)
- [pydbus](https://pypi.org/project/pydbus/) (python3-pydbus)
- [Unidecode](https://pypi.org/project/Unidecode/) (python3-unidecode)
- [requests](https://pypi.org/project/requests/) (python3-requests)
- [chardet](https://pypi.org/project/chardet/) (python3-chardet)

## Installation

**Installing dependencies:**

on Debian/Ubuntu:  
```sudo apt update && sudo apt install ffmpeg git libmpv1 python3 python3-requests python3-chardet python3-pyqt5 python3-pil python3-pandas python3-gi python3-unidecode python3-pydbus python3-pip python3-setuptools python3-dev python3-wheel```

**Cloning repository:**

```git clone --depth=1 https://gitlab.com/astroncia/iptv.git astronciaiptv```  
```cd astronciaiptv```  

**Installing Python modules:**  

```python3 -m pip install -r requirements.txt```  

**Create translation files:**  
  
```make```  

**Starting:**

```./start_linux.sh```

## View recordings

MKV container used for recordings  
For recordings view recommended [VLC media player](https://www.videolan.org/).  

## Program update

```git pull https://gitlab.com/astroncia/iptv.git```  

## Disclaimer

Astroncia IPTV doesn't provide any playlists or other digital content.  
