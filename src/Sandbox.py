#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Jul 27, 2015
Datenbereinigung und -zusammenstellung für die Stimmungsanalyse
Programm greift auf einen Teil-Extrakt der Nachrichtensammlung zu.
Future Import: Python 2.x Division ist nicht korrekt abgebildet

@author: Jan Dombrowicz
@version: 1.6
'''
from __future__ import division

def sandy(unternehmen):
    from string import punctuation
    
    # Import der Module
    import pandas as pd
    import csv
    
    # Datenimport
    with open('/home/jd/dev/python/UseCase_StocksPrediction/data/gewichte.csv', mode='r') as f:
        reader = csv.reader(f)
        gewichte = {rows[0]: rows[1] for rows in reader}

    df_pos = pd.read_csv('/home/jd/2ext/stocks_prediction_1.0/positiv_neu.csv', delimiter = ',', names = ['ID', 'Wort'])
    df_neg = pd.read_csv('/home/jd/2ext/stocks_prediction_1.0/negativ_neu.csv', delimiter = ',', names = ['ID', 'Wort'])
    df_news = pd.read_csv('/home/jd/2ext/stocks_prediction_1.0/data/cleaned/'+unternehmen+'.csv', delimiter =';', names = ['Titel', 'Artikel', 'Datum', 'URL', 'Unternehmen'])
    df_news = df_news.reset_index(drop=True)
    
    df_tmp = pd.DataFrame()

    print(gewichte)
    # DQ -> str.lower() um Wörterbuch mit Artikel zu harmonisieren
    df_pos = df_pos['Wort'].str.lower().tolist()
    df_neg = df_neg['Wort'].str.lower().tolist()
    
    # Variablen Initialisierung
    cnt_pos = 0
    cnt_neg = 0
    multiplikator = 1
    
    # Einlesen der Nachrichten und Vorbereitung der Daten
    # Im Anschluss werden die Wörter auf die Zugehörigkeit zu einem Wörterbuch geprüft und entsprechend gewertet
    for artikel in df_news['Artikel']:
        # Alle Wörter kleinschreiben und Sonderzeichen entfernen
        artikel_processed = artikel.lower()
        for p in list(punctuation):
            artikel_processed=artikel_processed.replace(p,' ')
        
        for wort in artikel_processed.split(' '):
            if wort in df_pos:
                cnt_pos += (multiplikator * 1)
                multiplikator = 1
            if wort in df_neg:
                cnt_neg += (multiplikator * 1)
                multiplikator = 1
            if wort in gewichte:
                multiplikator = int(gewichte[wort])
                print("Setze Multiplikator " + wort + " auf " + str(gewichte[wort]))
    
        test = pd.Series([(cnt_pos/len(artikel_processed))*100, (cnt_neg/len(artikel_processed))*100, (cnt_pos/len(artikel_processed))*100 - (cnt_neg/len(artikel_processed))*100 ,len(artikel_processed)])
        cnt_pos = 0
        cnt_neg = 0
        df_tmp = df_tmp.append(test, ignore_index=True)
        
    df_tmp = df_tmp.reset_index(drop=True)
    
    # Zusammenführung der Dataframes. Fehleranfällig - Besser über einen Key joinen
    df_result = pd.concat([df_news, df_tmp], axis=1)
    
    df_result.to_csv('/home/jd/2ext/stocks_prediction_1.0/'+unternehmen+'_bewertung.csv', sep=';', encoding='utf-8', quotechar='\'')

sandy('Adidas')
