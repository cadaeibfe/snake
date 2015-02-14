def enum(name, enumerators):
    enumerators = enumerators.split()
    enums = dict(zip(enumerators, range(len(enumerators))))
    return type(name, (), enums)

