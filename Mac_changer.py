import subprocess # permite correr comandos de la terminal a traves de la funcion call
import optparse # permite crear comandos para ejecutar con parametros desde consola
import re # para trabajar con expresiones regulares

"""
al pasar los comandos como cadena de texto y usar shell=True, no es seguro, puede ejecutarse agregando comandos al input mediante ;<comando>

subprocess.call("ifconfig " + interface + "down", shell=True) 
subprocess.call("ifconfig " + interface + "hw ether " + new_mac, shell=True) 
subprocess.call("ifconfig " + interface + "up", shell=True)
"""


# Funcion para obtener los argumentos
def get_arguments():
    parser = optparse.OptionParser() #vincula un comando como por ejemplo -i con una interface en este caso

    parser.add_option("-i", "--interface", dest = "interface", help = "Interface que cambiara su direccion MAC") #agrego el comando -i y su forma extendida --interface e indico que el valor se guarde en la variable interface, help para la descripcion del comando.
    parser.add_option("-m", "--mac", dest = "new_mac", help = "Nueva direccion MAC")

    (options, arguments) = parser.parse_args() # guardo en options los valores dest(interface y new_mac) y en arguments los argumentos(--interface y --mac)

    # si no ingresa una interface valida
    if not options.interface:
        parser.error("[-] Indicar una interfaz valida, usa --help para mas informacion")
    elif not options.new_mac:
        parser.error("[-] Indicar una direccion MAC valida, usa --help para mas informacion")
    return options #option contiene tanto el valor de options como el de arguments


# Funcion para cambiar la direccion MAC
def change_mac(interface, new_mac):
    
    print("[+] Cambiando la direccion MAC en " + interface + " a -> " + new_mac)
    
    #utilizo una lista para evitar el shell=True
    subprocess.call(["ifconfig", interface, "down"])  # ara cambiar la mac primero hay que apagar la interfaz.
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])  # recibe un string con la cadena de comandos a seguir separados por espacio, en este caso cambia la mac de eth0 por la indicada.
    subprocess.call(["ifconfig", interface, "up"]) # vuelvo a levantar la interfaz


# obtener direccion MAC desde el comando ifconfig
def get_current_mac(interface):

    # verifico el output del comando ifconfig para checkear los resultados.
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
  
    # expresion regular para filtrar el output de ifconfig y quedarme solo con los caracteres de la direccion MAC
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    
    if mac_address_search_result:
        return mac_address_search_result.group(0) # si encuentra mas caracteres que cumplan con el filtro de la expresion regular, estos se agrupan, por lo que indicamos group(0) para quedarnos solo con uno. 
    else:
        print("[-] Error al leer direccion MAC")


options = get_arguments() 

current_mac = get_current_mac(options.interface) #MAC actual
print("Current MAC -> " + current_mac)

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface) #MAC nueva

if current_mac == options.new_mac:
    print("[+] New MAC -> " + str(current_mac))
else:
    print("[-] No pudo cambiarse la direccion MAC")


""" al ejecutar el comando en consola ahora puedo pasarle los argumentos > mac_changer.py --interface eth0 --mac 00:11:22:33:44:66 """


