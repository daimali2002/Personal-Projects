from transaction import * 

transobj = transactions()

transobj.gettoken()
print(transobj.token)
transobj.customervalidate()
print(transobj.transaction_id)
print(transobj.data_3ds_secureid)
print(transobj.initiate_payment("36ad6812-8eb8-e6cb-9596-449298f9255d"))