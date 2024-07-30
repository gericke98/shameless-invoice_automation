#Librerías
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Credenciales
token = os.getenv('SHOPIFY_TOKEN')
shop_url = os.getenv('SHOPIFY_SHOP_URL')
clave_api = os.getenv('SHOPIFY_API')
password = os.getenv('SHOPIFY_PASSWORD')
image_path = 'logo_shameless.webp'
date_inicial = '2024-05-01' ### CAMBIAR ESTOS VALORES
date_final = '2024-07-31' ### CAMBIAR ESTOS VALORES

#Función para crear la sesión y conexión con la API de Shopify
def create_session():
    s = requests.Session()
    s.headers.update({
        "X-Shopify-Access-Token": token,
        "Content-Type": 'application/json'
    })
    return s

#Llamada a la sesión
def main():
    sess = create_session()
    resp = sess.get(shop_url+'/admin/api/2024-04/orders.json?limit=200')
    resp = resp.json()
    return resp


#Función para crear el PDF
def form(path_output,name,direccion,auxiliar_address,phone,invoice_number,date,pedido_list,ivabool,subtotalinput):
    my_canvas = canvas.Canvas(path_output, pagesize=letter)
    len_inicial_padre = 630
    len_inicial = len_inicial_padre
    #Imagen del logo
    my_canvas.drawImage(image_path, 400, len_inicial+60, width=150,height=100)
    my_canvas.setLineWidth(.3)
    my_canvas.setFont('Helvetica-Bold', 12)
    
    #Datos del cliente
    my_canvas.drawString(30, len_inicial, 'Datos del cliente')
    my_canvas.setFont('Helvetica', 10)
    len_inicial = len_inicial-15
    my_canvas.drawString(30, len_inicial, name)
    len_inicial = len_inicial-15
    my_canvas.drawString(30, len_inicial, direccion)
    len_inicial = len_inicial-15
    my_canvas.drawString(30, len_inicial, auxiliar_address)
    len_inicial = len_inicial-15
    if(phone != None):
        my_canvas.drawString(30, len_inicial,phone)
    
    #Datos de la factura
    len_inicial = len_inicial_padre
    my_canvas.setFont('Helvetica-Bold', 12)
    my_canvas.drawString(250, len_inicial, 'Nº FACTURA')
    len_inicial = len_inicial-15
    my_canvas.setFont('Helvetica', 10)
    my_canvas.drawString(250, len_inicial, invoice_number)
    len_inicial = len_inicial-15*2
    my_canvas.setFont('Helvetica-Bold', 12)
    my_canvas.drawString(250, len_inicial, 'Fecha')
    len_inicial = len_inicial-15
    my_canvas.setFont('Helvetica', 10)
    my_canvas.drawString(250, len_inicial, date)
    
    #Datos de la empresa
    len_inicial = len_inicial_padre
    my_canvas.setFont('Helvetica-Bold', 12)
    my_canvas.drawString(430, len_inicial, 'Datos')
    len_inicial = len_inicial-15
    my_canvas.setFont('Helvetica', 10)
    my_canvas.drawString(430, len_inicial, 'CORISA TEXTIL S.L.')
    len_inicial = len_inicial-15
    my_canvas.drawString(430, len_inicial, 'B02852895')
    len_inicial = len_inicial-15
    my_canvas.drawString(430, len_inicial, 'Calle Neptuno 29')
    len_inicial = len_inicial-15
    my_canvas.drawString(430, len_inicial, 'Pozuelo de Alarcón, Madrid, 28224')
    len_inicial = len_inicial-15
    my_canvas.drawString(430, len_inicial, '(+34) 608667749')
    
    my_canvas.setFont('Helvetica-Bold', 12)
    my_canvas.line(20,465,600,465)
    my_canvas.line(20,465,20,305) #Línea vertical de la izquierda de la tabla 
    my_canvas.line(600,465,600,305) #Línea vertical de la derecha de la tabla 
    my_canvas.drawString(30, 450, 'ARTÍCULOS')
    my_canvas.line(320,465,320,305) #Línea vertical divisoria
    my_canvas.drawString(330, 450, 'CANTIDAD')
    my_canvas.line(410,465,410,305) #Línea vertical divisoria
    my_canvas.drawString(420, 450, 'PRECIO')
    my_canvas.line(500,465,500,305) #Línea vertical divisoria
    my_canvas.drawString(510, 450, 'TOTAL')
    my_canvas.line(20,445,600,445) #Línea HORIZONTAL divisoria
    my_canvas.setFont('Helvetica', 10)
    
    i = 0
    subtotal= 0
    for list_order in pedido_list:
        subtotal_order = float(list_order[3][:-2])
        height = 430 -20*i
        my_canvas.drawString(30, height, list_order[0])
        my_canvas.drawString(330, height, list_order[1])
        my_canvas.drawString(420, height, list_order[2])
        my_canvas.drawString(510, height, list_order[3])
        subtotal+=subtotal_order
        i+=1
    subtotalinput = float(subtotalinput)/1.21
    subtotal = round(subtotalinput,2)
    if(ivabool == True):
        iva = round(0.21*subtotal,2)
    else:
        iva = 0
    total = subtotal + iva
    total = str(total) + ' €'
    iva = str(iva)+ ' €'
    subtotal_factura = str(subtotal)+ ' €'
    my_canvas.line(20,305,600,305) #Línea horizontal divisoria de abajo
    my_canvas.line(410,305,410,220) #Línea vertical divisoria de abajo
    my_canvas.setFont('Helvetica', 12)
    my_canvas.drawString(420, 290, 'Subtotal')
    my_canvas.line(410,280,600,280) #Línea horizontal del IVA
    my_canvas.setFont('Helvetica', 10)
    my_canvas.drawString(520, 290, subtotal_factura) #Aquí va el sumatorio
    
    my_canvas.drawString(420, 265, 'IVA')
    my_canvas.drawString(520, 265, iva)
    
    my_canvas.setFont('Helvetica-Bold', 12)
    my_canvas.drawString(420, 235, 'TOTAL')
    my_canvas.drawString(520, 235, total)
    my_canvas.line(410,255,600,255) #Línea horizontal del IVA
    my_canvas.line(600,305,600,220) #Línea vertical del TOTAL
    my_canvas.line(410,220,600,220) #Línea horizontal del IVA
    
    my_canvas.save()


# Llamada a la sesión
resp = main()
# Creado y exportación de facturas
for order in resp['orders']:
    if((order['created_at'][0:10]>=date_inicial)&(order['created_at'][0:10]<=date_final)&(order['financial_status']!='refunded')):
        if((order['customer']['first_name'] == 'Bluvo')|(order['name'][1:] == '32985') | (order['billing_address']['first_name'] == 'Nerety')):
            continue
        else:
            invoice_number = order['name'][1:]
            name = order['billing_address']['first_name'] + ' ' + order['billing_address']['last_name'] #Nombre completo
            if(order['billing_address']['address2']!= None): #Dirección completa
                direccion = order['billing_address']['address1'] + '-' + order['billing_address']['address2']
            else:
                direccion = order['billing_address']['address1']
            zip_code = order['billing_address']['zip']
            if(zip_code == None):
                zip_code = 'Sin información'
            city = order['billing_address']['city']
            if(city == None):
                city = 'Sin información'
            country = order['billing_address']['country']
            if(country == None):
                country = 'Sin información'
            auxiliar_address = zip_code + ',' + city + ',' + country

            phone = order['billing_address']['phone']


            date = order['created_at'][0:10]
            date_name = date[0:4]+date[5:7]+date[8:10]
            subtotal_input = order['current_subtotal_price']
            if(float(order['current_subtotal_price'])<1):
                continue
            path_output = date_name +invoice_number+'.pdf'
            pedido_list = []
            for item in order['line_items']:
                new_order = []
                pedido = str(item['name'])
                cantidad = str(item['quantity'])
                price = item['price']
                discount = item['total_discount']
                price_sin_iva = (float(price)-float(discount))/1.21
                iva = 0.21*price_sin_iva
                if((country == 'Spain') & (order['billing_address']['first_name'] != 'Ribadeo')):
                    ivabool = True
                    price_sin_iva = (float(price)-float(discount))/1
                else:
                    ivabool = False
                price_sin_iva = round(price_sin_iva,2)
                total_sin_iva = price_sin_iva*item['quantity']
                total_sin_iva = round(total_sin_iva,2)
                price_sin_iva = str(price_sin_iva)+ ' €'
                total_sin_iva = str(total_sin_iva) + ' €'
                new_order.append(pedido)
                new_order.append(cantidad)
                new_order.append(price_sin_iva)
                new_order.append(total_sin_iva)
                new_order.append(iva)
                new_order.append(iva)
                pedido_list.append(new_order)
            if(order['billing_address']['first_name'] == 'Ribadeo'):
                name = 'Pop up'
                direccion = 'Praça Ribeira 11 12, 4050-509 Porto, Portugal'
                auxiliar_address = ''
            form(path_output,name,direccion,auxiliar_address,phone,invoice_number,date,pedido_list,ivabool,subtotal_input)