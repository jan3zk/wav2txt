# WAV2TXT

Razpoznavalnik besedila iz zvočnih datotek WAV z uporabo Microsoftove spletne storitve [Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/speech-to-text/#features)

## Uporaba

Zagon na posamezni zvočni datoteki WAV:
```python wav2txt.py pot/do/datoteke.wav```

Zagon na vseh datotekah WAV znotraj mape:
```python wav2txt.py pot/do/mape/```

Opcijska uporaba izvršljive datoteke za okolje Windows:
```wav2txt.exe pot/do/datoteke.wav```
```wav2txt.exe pot/do/mape/```

Prednastavljen jezik je Slovenščina. Izbiro jezika lahko nastavimo z dodanim argumentom, npr. izbiro angleščine dosežemo z
```python wav2txt.py pot/do/datoteke.wav "English (United Kingdom)"```
