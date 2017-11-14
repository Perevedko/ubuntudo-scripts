# -*- coding: utf-8 -*-
toni_id = 7
bani_id = 8
martin_id =  9
atoito_id = 10
sergey_id = 11
upwork_id = 12
aruba_id = 13


import sys
from common import sock_db, common, models, uid
from common import domain, url, db, port, username, password
#needed only for DB direct connections
#from common import direct_db_conn, direct_db_cur
import odoorpc

def create_db():
        
    odoo = odoorpc.ODOO(domain, port=port)
    
    if db not in odoo.db.list():
        sys.exit("DB %s not found in db list" % db)    
    else:
        odoo.db.drop(password, db)
        
    odoo.db.create(username, db, demo=False, lang='it_IT', admin_password=password) #admin is the default username, it is not possible to select another one    



def install_modules():
            
    odoo = odoorpc.ODOO(domain, port=port)
    modules_to_install = ['base_location','base_location_geonames_import','crm','l10n_it','l10n_it_base','l10n_it_vat_registries','l10n_it_base_prov', 'sale']
    # 'l10n_it_base_location_geonames_import' can't be installed
    #to avoid issues, I did not put 'l10n_it_ddt' or 'account_asset'
    modules_to_uninstall = ['l10n_us','procurement_jit']
    ####################################   MODULES   ############
    odoo.login(db, username, password)
    Module = odoo.env['ir.module.module']
    print "Installing modules", modules_to_install
    for item in modules_to_install:
        # Get the module ids by name
        module_ids = Module.search([['name', '=', item]])
        print module_ids
        # there should be 1 module in module_ids, but iterate for each module object
        for module in Module.browse(module_ids):
            if module.state == 'installed':
                # If installed, just print that it has install
                print "%s has already been installed." % module.name
            else:
                # Otherwise, install it
                sys.stdout.write("Installing %s ... " % module.name)
                module.button_immediate_install()
                print "Done."
    
    print "Uninstalling modules", modules_to_uninstall
    for item in modules_to_uninstall:
        module_ids = Module.search([['name', '=', item]])
        print module_ids
        for module in Module.browse(module_ids):
            if module.state == 'installed':
                sys.stdout.write("Uninstalling %s ... " % module.name)
                module.button_immediate_uninstall()
                print "Done."
            else:           
                print "%s Not installed." % module.name
    ########################################################                
   
if __name__ == "__main__":
    
    # create_db()
    # install_modules()
    
    #create accounts
#not working in 8.0    
#    new_journal = models.execute_kw(
#        db, uid, password,
#        'account.account', 'create', [{
#            'code' : '20010',
#            'name': 'Capitale Sociale',
#            'user_type_id': 9
#        }]) 
#    new_journal = models.execute_kw(
#        db, uid, password,
#        'account.account', 'create', [{
#            'code' : '150800',
#            'name': 'Crediti v/soci',
#            'user_type_id': 1,
#            'reconcile':True
#        }]) 
#    new_journal = models.execute_kw(
#        db, uid, password,
#        'account.account', 'create', [{
#            'code' : '150801',
#            'name': 'Crediti v/soci, Gabriella',
#            'user_type_id': 1,
#            'reconcile':True
#        }]) 
#    new_journal = models.execute_kw(
#        db, uid, password,
#        'account.account', 'create', [{
#            'code' : '150802',
#            'name': 'Crediti v/soci, Matteo',
#            'user_type_id': 1,
#            'reconcile':True
#        }]) 
    
    ##Create main Company? It seems no effect
    cid = models.execute_kw(
        db, uid, password,
        'res.company', 'write', [[1], {
            'name': 'Daphne Solutions di Matteo Polleschi S.a.s.',
            'street': 'Via dei Colli, 53',
            'city': 'La Spezia',
            'zip': '19121',
            'email': 'yes@daphne-solutions.com',
            'website': 'daphne-solutions.com',
            # 'state_id': 349,
            # admin openerp.sql_db: bad query: UPDATE "res_partner" SET "state_id"=349
            # IntegrityError: insert or update on table "res_partner" violates foreign key constraint "res_partner_state_id_fkey"
            # DETAIL: Key(state_id) = (349) is not present in table "res_country_state".
            'phone': '+39 0187 735040',
            'is_company' : True,
            'customer' : True,
            'supplier' : True
        }])
    # WARNING admin openerp.models: res.company.write() with unknown fields: customer, is_company, supplier
    print "Main Company ID:", cid
    
    ############# Clienti
    ####################################
    
    #Casa editrice
    pid = models.execute_kw(
        db, uid, password,
        'res.partner', 'create', [{
            'name': 'Casa Editrice Toni di Zana Mirella S.a.s.',
            'is_company' : True,
            'customer' : True,
            'supplier' : True
        }])
    print "Casa Editrice Toni ID:", pid
#    direct_db_cur.execute("""UPDATE res_partner SET id = """+str(toni_id)+""" WHERE res_partner.id="""+str(pid))
#    direct_db_conn.commit()
    
    #Bani
    pid = models.execute_kw(
        db, uid, password,
        'res.partner', 'create', [{
            'name': 'BDA Elettronica',
            'phone':'+3905500000',
            'is_company' : True,
            'customer' : True,
            'supplier' : False
        }])
    print "BDA Elettronica ID:", pid
    
    #Andrea Martin
    pid = models.execute_kw(
        db, uid, password,
        'res.partner', 'create', [{
            'name': 'Andrea Martin',
            'is_company' : False,
            'customer' : True,
            'supplier' : False
        }])
    print "Andrea Martin ID:", pid
    
    #Terenzio
    pid = models.execute_kw(
        db, uid, password,
        'res.partner', 'create', [{
            'name': 'Atoito SRL',
            'is_company' : True,
            'customer' : True,
            'supplier' : False
        }])
    print "Atoito SRL ID:", pid
    
    ############# Clienti
    ####################################
    
    #Sergey
    pid = models.execute_kw(
        db, uid, password,
        'res.partner', 'create', [{
            'name': 'Sergey Kozlov',
            'is_company' : False,
            'customer' : False,
            'supplier' : True
        }])
    print "Sergey Kozlov ID:", pid
    
    #Upwork
    pid = models.execute_kw(
        db, uid, password,
        'res.partner', 'create', [{
            'name': 'Upwork Inc.',
            'is_company' : True,
            'customer' : False,
            'supplier' : True
        }])
    print "Upwork Inc. ID:", pid
    
    #Aruba
    pid = models.execute_kw(
        db, uid, password,
        'res.partner', 'create', [{
            'name': 'Aruba',
            'is_company' : True,
            'customer' : False,
            'supplier' : True
        }])
    print "Aruba ID:", pid
    
    ############# Prodotti
    ####################################
    
    pid = models.execute_kw(
        db, uid, password,
        'product.product', 'create', [{
            'name': 'Consulenza software',
            'currency_id' : '1',
            'list_price': 25.0,
            'property_account_income_id': 103,
            'property_account_expense_id' : 114
        }])
    # admin openerp.models: product.product.create() with unknown fields: currency_id, property_account_expense_id, property_account_income_id
    print "Prodotto consulenza:", pid