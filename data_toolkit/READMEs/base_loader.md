## --- base_loader.BASELOADER --- ##

Created to improve performance of reading excel sheets on network drive.

pd.read_excel/csv severely suffers when reading from shared network drive, so base_loader creates temp files locally and deletes after reading. Context manager (__enter__ and __exit__) used for cleanup. 

Also, by creating local files, the original data is not accessed, 
making it significantly safer in case of accidental overwrites, 
file coruption, or locking for other team members. 

# How To Use #
