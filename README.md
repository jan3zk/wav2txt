# WAV2TXT

Razpoznavalnik govora iz zvočnih datotek WAV z uporabo Microsoftove spletne storitve [Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/speech-to-text/#features). Orodje za vsako vhodno datoteko WAV generira istoimensko tekstovno datoteko z razpoznanim besedilom.

## Uporaba

Zagon na posamezni zvočni datoteki WAV:

```python wav2txt.py -w pot/do/datoteke.wav```

Zagon na vseh datotekah WAV znotraj mape:

```python wav2txt.py -w pot/do/mape/```

Z opcijskimi argumenti lahko izberemo željen jezik, spletni brskalnik in punktuator, npr.:

```python -w wav2txt.py pot/do/datoteke.wav -l "English (United Kingdom)" -b Firefox -p```

### Strežniška aplikacija

Zagon aplikacije:

```python app.py```

Klic aplikacije:

```curl -X POST -F file=@datoteka.wav http://localhost:5000/recognise```

### Opcijsko

Uporaba [izvršljive datoteke](https://unilj-my.sharepoint.com/:u:/g/personal/janezkrfe_fe1_uni-lj_si/EZN2fcSiW-JAueoIyGGIA2wBDRHj8u4RQsacJgxNlIpwiQ) v okolju Windows:

```wav2txt.exe pot/do/datoteke.wav```

```wav2txt.exe pot/do/mape/```
