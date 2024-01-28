## Skrypt sprawdzajacy zakres portow na danym adresie lub zakresie portow 

#import argparse
import socket
from colorama import init, Fore
#from threading import Thread, Lock
#from queue import Queue
import ipaddress
import sys
import scanless

init()

#%% Main
'''
    Glowna funkcja kodu:
        - wyswietla proste menu
        - wywoluje w sobie inne funkcje
'''
def main():
    addresses = []
    ports = (-1, -1)
    while True:
        print(Fore.CYAN + "-- Menu --")
        print("1. Pojedynczy adres")
        print("2. Zakres adresow")
        print("3. Zakres portow")
        print("4. Rozpocznij skanowanie")
        print("5. Szybkie skanowanie wybranych adresow")
        print("0. Zakoncz")
        
        choice = int(input("Twoj wybor: "))
        match choice:
            case 1: # Wprowadzenie pojedynczego adresu
                addresses = single_adress()
            case 2: # Wproadzenie zakresu adresow 
                addresses = addresses_range()
            case 3:
                ports = port_input()
            case 4:
                scan_ports(addresses, ports)
            case 5:
                quick_scan()
            case 0:
                sys.exit()
#%% Walidator adresow
'''
    Funkcja sprawdza poprawnosc podanego adresu
'''
def validate_ip(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True  # Adres IPv4 jest poprawny
    except ipaddress.AddressValueError:
        try:
            ipaddress.IPv6Address(ip)
            return True  # Adres IPv6 jest poprawny
        except ipaddress.AddressValueError:
            return False  # Niepoprawny adres IP



#%% Pojedynczy adres

'''
    Funkcja pobiera pojedynczy adres od uzytkownika
'''
def single_adress():
    address = []
    address.append(input("Podaj adres: "))
    if validate_ip(address[0]):
        return address
    else:
        return []

#%% Zakres adresow
'''
    Funkcja pobiera adres ip startowy i koncowy od uzytkownika, sprawdza poprawnosc danych
    Uzytkownik wprowadza adres ip poczatkowy oraz koncowy, otrzymujemy tablice 
'''
def addresses_range():
    start = input("Podaj adres startowy: ")
    end = input("Podaj adres koncowy: ")
    
    if not (validate_ip(start) and validate_ip(end)):
        return []
    
    start_int = int(ipaddress.IPv4Address(start).packed.hex(), 16)
    end_int = int(ipaddress.IPv4Address(end).packed.hex(), 16)
    
    if start_int >= end_int:
        return []
    
    addresses = [str(ipaddress.IPv4Address(ip)) for ip in range(start_int, end_int + 1)]
    
    return addresses

#%% Zakres portow
'''
    Funkcja pobiera port startowy i koncowy od uzytkownika, sprawdza poprawnosc danych
    Uzytkownik wprowadza port startowy i koncowy, zwraca je w postaci tupla
'''
def port_input():
    start = input("Podaj port startowy: ")
    end = input("Podaj port koncowy: ")
    
    if start >= end:
        return (end, start)
    else:
        return (start, end)
    
#%% Skanowanie portow
def scan_ports(ips, ports):
    if ips == [] and ports == ("-1", "-1"):
        print("Brak danych do skanowania. ")
        return None
    for ip in ips:
        for port in range(int(ports[0]), int(ports[1]) + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)

            try:
                sock.connect((ip, port))
                print(Fore.GREEN + f"{ip} : {port} is open")
            except (socket.timeout, socket.error):
                print(Fore.RED + f"{ip} : {port} is closed")
            finally:
                sock.close()

#%% Szybki skan wybranych adresow
def quick_scan():
    addresses = input("Podawaj adresy po spacji: ")
    addresses = addresses.split()
    for address in addresses:
        sl = scanless.Scanless()
        try:
            output = sl.scan(address, scanner='yougetsignal')
            data = output['raw'].split('\n')
            #print(data)
            for d in data:
                if "closed" in d:
                    print(Fore.RED + d)
                else:
                    print(Fore.GREEN + d)
        except Exception as e:
            print(f"Błąd podczas skanowania: {str(e)}")
        print("---------------------")
        
    
#%%  


main()
    
