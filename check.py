import astm
print("ASTM package contents:")
print(dir(astm))
print("\nASTM package path:", astm.__file__)
print("ASTM package version:", getattr(astm, '__version__', 'Unknown'))