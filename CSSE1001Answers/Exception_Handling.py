def catchException():
 
    try:
        f()
        e = 'No exception raised'
        return str(e)
    except Exception as e:
        z = e
        return str(e)
