import re
import random

IP_ADDRESS_RE = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")
MASK_BINARY_RE = re.compile(r"^1*0*$")
IP_ADDRESS = "192.168.10.5"
MASK = "255.255.255.0"

def check_ip_address(ip_addr):
	if ip_address_valid(ip_addr):
		return True
  
def check_mask(MASK):
	if ip_address_valid(mask):
		return True
 
 
def ip_address_valid(ip_addr):
  if not IP_ADDRESS_RE.match(ip_addr):
    return False
  ip_addr_octets = ip_addr.split(".")
  #for octet in ip_addr_octets:
  #  if int(octet) < 0 or int(octet) > 255:
  #    return False
  return all(0 <= int(octet) <= 255 for octet in ip_addr_octets)
  
def mask_valid(mask):
  if not ip_address_valid(mask):
    return False
  mask_binary = convert_ip_addr_decimal_to_binary(mask)
  return MASK_BINARY_RE.match(mask_binary)   
  
def convert_ip_addr_decimal_to_binary(ip_addr):
  decimal_octets = ip_addr.split('.')
  binary_octets =[]
  for decimal_octets in decimal_octets:
    binary_octet = '{0:08b}'.format(int(decimal_octets))
    binary_octets.append(binary_octet)
  ip_addr_binary=''.join(binary_octets)
  return ip_addr_binary

def convert_ip_addr_to_human(ip_addr_int):
    ip_addr_bin = '{0:032b}'.format(ip_addr_int)
    decimal_octets = []
    for i in range(4):
      start = i*8
      end = (i+1)*8 
      binary_octets = ip_addr_bin[start:end]
      decimal_octets.append(str(int(binary_octets,2)))
      
    ip_addr_decimal = '.'.join(decimal_octets)
    return ip_addr_decimal

def subnet_calculator(ip_addr, mask):
  print("IP address: {}".format(ip_addr))
  print("Subnet mask: {}".format(mask))
  
  if not ip_address_valid(ip_addr):
      print("IP address is not valid")
      return
  if not mask_valid(mask):
      print("Mask is not valid")
      return
  ip_addr_binary = convert_ip_addr_decimal_to_binary(ip_addr)
  mask_binary = convert_ip_addr_decimal_to_binary(mask)
  mask_num_ones = mask_binary.count('1')
  print("Mask in slash notation: /{}".format(mask_num_ones))
  network_addr_integer = int(ip_addr_binary,2)& int(mask_binary,2)
  print("Network address: {}".format(convert_ip_addr_to_human(network_addr_integer)))
  wildcard_integer = ~ int(mask_binary,2) & 0xffffffff
  wildcard = convert_ip_addr_to_human(wildcard_integer)
  print("Wildcard mask {}".format(wildcard))
  broadcast_addr_integer = wildcard_integer | network_addr_integer
  print(bin(broadcast_addr_integer))
  broadcast_addr = convert_ip_addr_to_human(broadcast_addr_integer)
  print("Wildcard mask {}".format(broadcast_addr))
  if mask_num_ones <=30:
	  num_hosts = 2**(32-mask_num_ones)-2
  elif mask_num_ones == 31:
	  num_host = 2
  elif mas_num_ones ==32:
	  num_host = 1
  print("Number of host {}".format(num_hosts))	
  while True:
	  choice = input("Generate andom I adress from network? (y/n):")
	  if choice == 'y':
		  random_ip_addr_integer = random.randint(network_addr_integer,broadcast_addr_integer)  
		  random_ip_addr = convert_ip_addr_to_human(random_ip_addr_integer)
		  print("Random IP address : {}".format(random_ip_addr))
	  elif choice == 'n':
		  break
	  else:
		  print("Enter y or n! Please.") 
  		  
		   
def main():
  ip_addr = input("Type IP adress from network:")
  mask = input("Type mask adress from network:")
  if not ip_address_valid(ip_addr):
	  print("Your error address input",ip_addr)
	  ip_addr2 = input("Type IP adress from network again:")
	  mask2 = input("Type mask adress from network:")
	  subnet_calculator(ip_addr2,mask2)
  if not ip_address_valid(mask):	  
	  print("Your error mask input", mask)
	  mask3 = input("Type mask adress from network again:")
	  ip_addr3 = input("Type IP adress from network:")
	  subnet_calculator(ip_addr3,mask3)
  else:	
	  print("Your address input ",ip_addr)
	  print("Your mask input", mask)  
	  subnet_calculator(ip_addr,mask)
  
  

main() 
