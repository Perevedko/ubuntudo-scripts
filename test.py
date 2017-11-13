# -*- coding: utf-8 -*-

from common import sock_db, common, models, uid
from common import url, db, username, password
from common import direct_db_conn, direct_db_cur

from init import toni_id, bani_id, martin_id, atoito_id, sergey_id, upwork_id, aruba_id

#all_base = sock_db.list()
#print "Databases: ", all_base

import odoorpc
# Prepare the connection to the server
odoo = odoorpc.ODOO('0.0.0.0', port=8069)
#odoo = odoorpc.ODOO('ubuntudoo.daphne-solutions.com', port=8069)
odoo.login(db, username, password)
# Current user
user = odoo.env.user
print(user.name)            # name of the user connected
print(user.company_id.name) # the name of its company
# Simple 'raw' query
user_data = odoo.execute('res.users', 'read', [user.id])
#print(user_data)

print "Odoo version", common.version()['server_version']

print uid


print models.execute_kw(db, uid, password,
    'res.partner', 'check_access_rights',
    ['read'], {'raise_exception': False})
print models.execute_kw(db, uid, password,
    'res.partner', 'search',
    [[['is_company', '=', True], ['customer', '=', True]]])
    
#https://github.com/odoo/odoo/blob/10.0/addons/account/models/account_invoice.py
invoice_id = models.execute_kw(
    db, uid, password,
    'account.invoice', 'create', [{
        'type' : 'out_invoice',
        'partner_id' : toni_id,
        'account_id' : 19,    #1 emessa, 2 ricevuta
        'journal_id' : 2,                #not mandatory
        'reference_type' : 'none',
        'date_invoice' : '2016-11-11'
    }])
print invoice_id
old_id = invoice_id
invoice_id = invoice_id +100 
direct_db_cur.execute("""UPDATE account_invoice SET id = """+str(invoice_id)+""" WHERE account_invoice.id="""+str(old_id))
direct_db_conn.commit()
print "record updated successfully"

invoice_line = models.execute_kw(
    db, uid, password,
    'account.invoice.line', 'create', [{
        'invoice_id' : invoice_id,
        'name': 'Automatic invoice line',
        'account_id': 1,
        'price_unit' : 25.00,
        'quantity' : 1,
        'invoice_line_tax_ids' : [[4,1,0]] #second position is tax id
    }])
print invoice_line 

#Odoo 10
models.execute_kw(db, uid, password,
    'account.invoice', 'compute_taxes', [invoice_id])
models.execute_kw(db, uid, password,
    'account.invoice', 'invoice_validate', [invoice_id])
models.execute_kw(db, uid, password,
    'account.invoice', 'action_move_create', [invoice_id])

print "journals:"
print models.execute_kw(db, uid, password, 'account.journal', 'search_read', [[]], 
                        {'fields': ['id', 'name'], 'limit': 50})

print "accounts:"
print models.execute_kw(db, uid, password, 'account.account', 'search_read', [[]], 
                        {'fields': ['id','code','name'],'limit': 8})
                        
print "invoices:"
print models.execute_kw(db, uid, password, 'account.invoice', 'search_read', 
                        [[]], 
                        {'fields': ['id', 'number', 'type', 'journal_id', 'amount_total', 'amount_tax'],'limit': 2})
                  
print "invoice lines:"
print models.execute_kw(db, uid, password, 'account.invoice.line', 'search_read', 
                        [[['invoice_id', '=', 52]]], 
                        {'fields': ['id','invoice_line_tax_ids'],'limit': 50})                  
                           
print "taxes:"               
print models.execute_kw(db, uid, password, 'account.tax', 'search_read', 
                        [[['id', '=', 2]]], 
                        {'fields': ['id','description'],'limit': 100})

print "products:"               
print models.execute_kw(db, uid, password, 'product.product', 'search_read', 
                        [[]], 
                        {'fields': ['id','name'],'limit': 100})
                                                
############  TEST AMMORTAMENTO   #################
pid = models.execute_kw(
    db, uid, password,
    'account.asset.category', 'create', [{
        'name': 'Categoria Ammortamento 1',
        'currency_id' : '1',
        'account_asset_id': 6,
        'account_depreciation_id': 1,
        'account_depreciation_expense_id' : 144,
        'journal_id' : 1
    }])
print "Categoria ammortamento:", pid

pid = models.execute_kw(
    db, uid, password,
    'account.asset.asset', 'create', [{
        'name': 'Ammortamento 1',
        'category_id' : 1,
        'value' : 100,
        'invoice_id' : 1
    }])
print "Ammortamento:", pid                        

print "Asset categories:"               
print models.execute_kw(db, uid, password, 'account.asset.category', 'search_read', 
                        [[]], 
                        {'fields': ['id', 'name', 'account_depreciation_id', 'journal_id', 'account_depreciation_expense_id', 'account_asset_id'],'limit': 1})
                        
print "Asset:"               
print models.execute_kw(db, uid, password, 'account.asset.asset', 'search_read', 
                        [[]], 
                        {'fields': ['id', 'name', 'value', 'value_residual'],'limit': 1})                        

################### TEST CRM ######################
#still TODO
leadid = models.execute_kw(
    db, uid, password,
    'crm.lead', 'create', [{
        'name': 'Promozione',
        'partner_id' : 1
    }])
print "Generato lead:", leadid