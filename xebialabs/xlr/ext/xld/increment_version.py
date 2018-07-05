import semantic_version

read_version = current_version
print("The read version is %s" % read_version)
version = read_version.split('/')[-1]
print(version)
v = semantic_version.Version(version)
n=v.next_patch()
print(n)
next_version = read_version.replace(version,str(n))
print(next_version)


#releaseVariables[variable]=read_version.replace(version,str(n))


