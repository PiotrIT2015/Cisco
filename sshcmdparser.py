import re
import paramiko
import time
import datetime
import string

IP_ADDRESS_RE = re.compile(r"^\b(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\b$")
cmd_file = './cmnds_crashinfo.txt' 
output_file = './output.txt' 
input_cmd_file = './cmd.txt'
input_cmd_file2 = './cmnds_crashinfo3.txt'
input_time_file = './time.txt'

def isint(input):
    return input.isdigit()

def isfloat(input):
    try: 
        return float(input) != None;
    except ValueError: 
        return False;

def isstr(input):
    if not isint(input) and not isfloat(input):
        return True
    return False
    
def number_of_lines():
    print "Program determines the number of lines, words and chars in a file."
#    file_name = raw_input("What is the file name to analyze? ")

    in_file = open(input_cmd_file2, 'r')
    data = in_file.read()

    words = string.split(data)

    chars = 0
    lines = 0
    for i in words:
        chars = chars + len(i)

    print chars, len(words)
    
    return len(words)

def match_delay(number1,number2):
	timestamp_list = []
	timestamp_list.append(number1)
	timestamp_list.append(number2)
	p = 0
	print timestamp_list[0].split(':')[0]
	print timestamp_list[0].split(':')[1]
	print timestamp_list[0].split(':')[2]
	print timestamp_list[1].split(':')[0]
	print timestamp_list[1].split(':')[1]
	print timestamp_list[1].split(':')[2]
	t = datetime.time(int(timestamp_list[1].split(':')[0]),int(timestamp_list[1].split(':')[1]),int(timestamp_list[1].split(':')[2]))
	print 'Hours:%d' % t.hour
	print 'Minutes:%d' % t.minute
	print 'Seconds:%d' % t.second
	l = datetime.datetime(int(timestamp_list[0].split(':')[2]),int(timestamp_list[0].split(':')[1]),int(timestamp_list[0].split(':')[0]))
	print 'Year:%d' % l.year
	print 'Month:%d' % l.month
	print 'Day:%d' % l.day
	return l.year, l.month, l.day, t.hour, t.minute, t.second 

def apply_input_parameters_on_device(whole_list_of_cmd_recv,command_recv,delay_recv,frequency_recv,ip_recv,username_recv,password_recv):
	for n in range(len(whole_list_of_cmd_recv)):
		  command = command_recv.split(',')[n]
		  commands_list = []
		  commands_list.append(command)
		  delay = delay_recv.split(',')[n]
		  delay_list = []
		  delay_list.append(delay)
		  p = 0
		  while p < len(commands_list):
			  print command_recv.split(',')
			  for s in range(len(command_recv.split(','))): 
				  print 'Input CMD:' + command_recv.split(',')[s]
				  command = command_recv.split(',')[s]
				  print type(command)
				  delay = delay_recv.split(',')[s]
				  print type(delay)
				  if isstr(command) == True:
					  if isstr(delay) == False:
						  push_everything_to_the_device_via_ssh(ip_recv,username_recv,password_recv,command,float(delay),int(frequency_recv)) 
				  r = 0
				  while r < len(delay_list):
					  print delay_recv.split(',')
					  for s in  range(len(delay_recv.split(','))):
						  print 'Delay for CMD:' + delay_recv.split(',')[s]
						  command = command_recv.split(',')[s]
						  print type(command)
						  delay = delay_recv.split(',')[s]
						  print type(delay)
						  print isstr(command)
						  print isstr(delay)
						  if isstr(command) == True:
							  if isstr(delay) == False:
								  push_everything_to_the_device_via_ssh(ip_recv,username_recv,password_recv, command,float(delay),int(frequency_recv)) 
					  r += 1
					  p += 1

def ip_address_valid(ip_addr):
  if not IP_ADDRESS_RE.match(ip_addr):
    return False
  ip_addr_octets = ip_addr.split(".")
  for octet in ip_addr_octets:
	  if (0 <= int(octet) <= 255):
		  return True


def push_everything_to_the_device_via_ssh(ip,typed_username,typed_password,line_cmd,typed_sleeping_time,typed_frequency): 
    #Change exception message
    try:		
        #Define SSH parameters
        
        #Logging into device
        session = paramiko.SSHClient()
        
        ##
        session.load_system_host_keys()
		
		#For testing purposes, this allows auto-accepting unknown host keys
		#Do not use in production! The default would be RejectPolicy
        #session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.set_missing_host_key_policy(paramiko.RejectPolicy())
        
        
		#Passing the necessary parameters
        session.connect(ip,username = typed_username,password = typed_password) 
        
		#Start an interactive shell session on the router
        connection = session.invoke_shell()	
        
        #Setting terminal length for entire output - no pagination
        connection.send("terminal length 0\n")
        time.sleep(1)
        
        connection.send(line_cmd + '\n') 
        time.sleep(typed_sleeping_time)
        
        #Entering global config mode
#       connection.send("\n")
#       connection.send("configure terminal\n") 
#       time.sleep(1)
        
        #Open user selected file for reading
        selected_cmd_file2 = open(input_cmd_file2, 'r') # [Wojtek] we should 'try' this in case file is not readable or not there, this is pretty major exception
        
        #Starting from the beginning of the file
        selected_cmd_file2.seek(0)
        
        pk = number_of_lines()
        print pk
        
        #Writing each line in the file to the device
        for each_line2 in selected_cmd_file2.readlines():
			connection.send(each_line2.split(';')[2] + '\n')
			#match_delay(each_line2.split(';')[0],each_line2.split(';')[1])
			y1, m1, d1, h1, ms1, s1 = match_delay(each_line2.split(';')[0],each_line2.split(';')[1])
			tp1 = datetime.datetime(y1,m1,d1,h1,ms1,s1).timetuple()
			ts1 = time.mktime(tp1)
			y2, m2, d2, h2, ms2, s2 = match_delay(each_line2.split(';')[0],each_line2.split(';')[1])
			tp2 = datetime.datetime(y2,m2,d2,h2,ms2,s2).timetuple()
			ts2 = time.mktime(tp2)
			time.sleep(typed_sleeping_time)
			print ts1
			print ts2
			
			
				
				  
				  
        #Entering global config mode
        connection.send("\n")
        connection.send("configure terminal\n") 
        time.sleep(1)
			
		 #Open user selected file for reading
        selected_cmd_file = open(cmd_file, 'r') # [Wojtek] we should 'try' this in case file is not readable or not there, this is pretty major exception
            
        #Starting from the beginning of the file
        selected_cmd_file.seek(0)
        
        
        
        #Writing each line in the file to the device
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(typed_sleeping_time)
			#time.sleep((datetime.datetime.now()).total_seconds()-ts)
		
		 
		
	    #Checking command output for IOS syntax errors
        output = connection.recv(65535)
        
        #Closing the command file 
        selected_cmd_file.close()
        
        if re.search(r"% Invalid input detected at", output):
            print("* There was at least one IOS syntax error on device %s" % ip)
        else:
			print("\nDONE for device %s" % ip)
			
			
		
   
        #Test for reading command output
        with open(output_file,"wb") as result: 
			for item in output:
				result.write(item)
			#print output + "\n"
          
    except paramiko.AuthenticationException:
        print("* Invalid username or password. \n* Please check the username/password file or the device configuration!")
        print("* Closing program...\n")
    except (OSError, IOError):
		print("Wrong file or file path")
    finally:
		#Closing the connection
        session.close() 

def main():
  ip_addr = raw_input("Type IP adress from network ex.192.168.2.152:") 
  username = raw_input("Type username of network device ex.Darek:") 
  password = raw_input("Type IP adress of network device ex.root123:") 
  command_all = raw_input("Type commands which would you like to try ex.show interface,show ip:") 
  delay_all = raw_input("Type delay for each command ex.3,2:")  
  frequency = raw_input("Type frequency of commands on network device ex.2:") 
  input_cmd = []
  input_cmd.append(command_all.split(','))  
  
  while not ip_address_valid(ip_addr):
	  print("Your error address input",ip_addr)
	  ip_addr = raw_input("Type IP adress from network again:")	
	  #Calling the SSH function
	  apply_input_parameters_on_device(input_cmd,command_all,delay_all,frequency,ip_addr2,username,password)
  else:
	  apply_input_parameters_on_device(input_cmd,command_all,delay_all,frequency,ip_addr,username,password)
	  
	  
	  
	  

if __name__ == "__main__":
    main()		  
	  


