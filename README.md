<h1 align="center">Video Sesini Dönüştür</h1>
  <p align="center">
    Video Kodlayıcı Telegram Botu
    <br />
    <a href="https://telegram.dog/SesVideoBot"><strong>Örnek Bot »</strong></a>
    <br />
    <a href="https://github.com/Turkce-Botlar-Sohbet/VideoSesDonustur/issues">Hata Bildir</a>
    |
    <a href="https://github.com/Turkce-Botlar-Sohbet/VideoSesDonustur/issues">Özellik İste</a>
  </p>
</p>

<hr>

<h2 align="center">Bot Hakkında</h2>
<p align="center">
    <a href="https://github.com/Turkce-Botlar-Sohbet/VideoSesDonustur">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/2048px-Telegram_logo.svg.png" height="100" width="100" alt="Telegram Logo">
    </a>
</p>
<p align='center'>
    Telegram'ın ses formatına destek vermediği hiç sesi çıkmayan videoları FFmpeg aracılığıyla uygun formata kodlar ve bunu herhangi bir kalite kaybı olmadan yapar.
</p>

### Ortam Değişkenleri:
Ortam değişkenlerini ayarlayın ve bunları [config.env](./config.env) içine ekleyin.
- `API_ID` - [https://my.telegram.org](https://my.telegram.org)'da bir uygulama oluşturarak edinin.
- `API_HASH` - [https://my.telegram.org](https://my.telegram.org)'da bir uygulama oluşturarak edinin.
- `BOT_TOKEN` - [https://t.me/BotFather](https://t.me/BotFather) adresinden bir bot oluşturarak edinin.
- `SUDO_USERS` - Yetkili kullanıcının ID numarasını ekleyin. Birden fazla kullanıcı için ayırıcı olarak boşluk kullanın.
- `DOWNLOAD_DIR` - (İsteğe bağlı) İndirilen dosyaları saklamak için geçici indirme dizini. Varsayılan: "downloads/"

### Kodlama Biçimini Yapılandırma:
FFmpeg profilini değiştirmek isterseniz şuradan ayarlayın: [ffmpeg.py](/functions/ffmpeg.py)

## Colab
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Turkce-Botlar-Sohbet/VideoSesDonustur/blob/master/VideoSesDonustur.ipynb)

## Scalingo
[![Deploy](https://cdn.scalingo.com/deploy/button.svg)](https://dashboard.scalingo.com/create/app?source=https://github.com/ali-mmagneto/VideoSesDonustur/tree/master)

## Linux'ta Docker ile Kurulum:

- 1. Python ve Docker'ı kurun.
```
sudo snap install docker
sudo apt install python3
```
- 2. Repo'yu Klonlayın.
```
git clone https://github.com/Turkce-Botlar-Sohbet/VideoSesDonustur
cd VideoSesDonustur
```
- 3. Yapılandırma Dosyasını Ayarlayın.
```
nano config.env
```
- 4. Docker Görüntüsü Oluşturun.
```
sudo docker build . -t videosesdonustur
```
- 5. Botu Çalıştırın.
```
sudo docker run videosesdonustur
```

### Telif Hakkı ve Lisans
- Copyright &copy; 2021 &mdash; [Türkçe Botlar Sohbet](https://t.me/botsohbet)
- [MIT License](./LICENSE)
